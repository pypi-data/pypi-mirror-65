import os
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import json
import logging
from typing import List

import requests
from uuid import uuid4

from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.db import IntegrityError, transaction
from django.db.models import Q
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from django.conf import settings
from remo_app.remo.api.constants import JobType, TaskType, AnnotationSetType
from remo_app.remo.api.views.mixins import UpdateDatasetModelMixin, DestroyDatasetModelMixin
from remo_app.remo.api.serializers import (
    ListDatasetSerializer,
    DatasetSerializer
)
from remo_app.remo.use_cases.annotation import update_new_annotation
from remo_app.remo.use_cases.annotation.class_encoding.class_encoding import ClassEncodingType, CustomClassEncoding
from remo_app.remo.use_cases.annotation.class_encoding.csv_parser import parse_csv_class_encoding, \
    parse_raw_csv_class_encoding
from remo_app.remo.use_cases.annotation.class_encoding.factory import class_encoding_factory
from remo_app.remo.use_cases.annotation_tasks import parse_annotation_task
from remo_app.remo.use_cases.jobs.dataset import LocalDatasetUploader, \
    upload_local_files, RemoteDatasetUploader, is_annotation_file # job_upload_dataset, process_files
from remo_app.remo.models import Dataset, ImageFolder, AnnotationSet, Task
from remo_app.remo import utils
# from remo_app.remo.use_cases.jobs.jobs import enqueue_dataset_job
# from remo_app.remo.use_cases import is_remo_local
from remo_app.remo.use_cases.jobs.update_annotation_set_statistics import update_annotation_set_statistics
from remo_app.remo.use_cases.jobs.update_dataset_statistics import update_dataset_statistics

logger = logging.getLogger('remo_app')


class DatasetViewSet(UpdateDatasetModelMixin,
                     DestroyDatasetModelMixin,
                     viewsets.ModelViewSet):
    filter_backends = (DjangoFilterBackend,)
    throttle_scope = 'uploads'

    def get_serializer_class(self):
        if self.action == 'list':
            return ListDatasetSerializer
        return DatasetSerializer

    def get_queryset(self):
        # TODO: restrict to team when it will be implemented, #272
        return Dataset.objects.filter(Q(user=self.request.user) | Q(is_public=True),
                                      is_archived=False)

    def create(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
        except json.decoder.JSONDecodeError:
            data = {}

        name = data.get('name', 'Dataset')
        is_public = data.get('is_public', False)
        if not request.user.is_superuser:
            is_public = False

        dataset = Dataset.objects.create(name=name,
                                         is_public=is_public,
                                         user=self.request.user)
        return Response(self.get_serializer(dataset).data)

    @action(['post'], detail=True, url_path='duplicate')
    def duplicate(self, request, pk=None):
        new_dataset = self.get_dataset(pk)
        new_dataset.pk = None
        new_dataset.is_public = False  # New dataset is always private
        new_dataset.user = request.user
        new_dataset.created_at = timezone.now()
        new_dataset.quantity = 0
        new_dataset.size_in_bytes = 0

        new_dataset.save()
        new_dataset.clone_relations_from(self.get_dataset(pk))
        # new_dataset.users_shared.set([])
        new_dataset.save()

        update_dataset_statistics(new_dataset)
        for annotation_set in new_dataset.annotation_sets.all():
            update_annotation_set_statistics(annotation_set)
            for annotation in annotation_set.annotations.all():
                # TODO: fix issue with not coping skip status
                update_new_annotation(annotation)

        return Response(self.get_serializer(new_dataset).data)

    def get_dataset(self, pk):
        return self.get_queryset().filter(id=pk).first()

    def _validate_annotation_set_id(self, request, dataset):
        annotation_set_id = request.query_params.get('annotation_set_id', None)
        if annotation_set_id:
            try:
                annotation_set_id = int(annotation_set_id)
            except ValueError:
                return None, Response({
                    'error': 'Annotation_set_id should be integer value.'
                }, status=status.HTTP_400_BAD_REQUEST)

            anotation_set = AnnotationSet.objects.filter(id=annotation_set_id).first()
            if not anotation_set:
                return None, Response({
                    'error': f'Annotation set #{annotation_set_id} was not found.'
                }, status=status.HTTP_404_NOT_FOUND)

            if anotation_set.dataset != dataset:
                return None, Response({
                    'error': f'Annotation set #{annotation_set_id} was not found in Dataset #{dataset.id}'
                }, status=status.HTTP_404_NOT_FOUND)

        return annotation_set_id, None

    @action(['post'], detail=True, url_path='upload')
    def upload(self, request, pk):
        dataset = Dataset.objects.filter(id=pk, user=request.user).first()

        annotation_set_id, resp = self._validate_annotation_set_id(request, dataset)
        if resp:
            return resp

        if not dataset or dataset.is_public and not request.user.is_superuser:
            return Response({
                'error': 'Only admin can edit public datasets.'
            }, status=status.HTTP_403_FORBIDDEN)

        if request.content_type.startswith('application/json') or request.content_type.startswith(
            'application/x-www-form-urlencoded'):
            return self._upload_from_url(request, dataset, annotation_set_id=annotation_set_id)
        elif request.content_type.startswith('multipart/form-data'):
            return self._upload_from_request(request, dataset, annotation_set_id=annotation_set_id)

        return Response({
            'error': True,
            'detail': f"Not supported payload format: {request.content_type}",
        }, status=400)

    def _store_file(self, file, dir_path):
        if not self._is_valid_file(file):
            return 0

        file_path = os.path.join(dir_path, file.name)
        with open(file_path, "wb") as output:
            for chunk in file.chunks():
                output.write(chunk)
        logger.debug(f'File saved to: {file_path}')

        if is_annotation_file(file_path):
            time.sleep(1)

        return 1

    @staticmethod
    def _is_valid_file(file):
        mime = utils.guess_mime(file)
        if file.size > settings.MAX_FILE_SIZE:
            logger.warning(
                f'File {file.name}: size {utils.human_size(file.size)} exceed max file size for upload')
            return False

        if (mime not in settings.IMAGE_MIME_TYPES
            and mime not in settings.ARCHIVE_MIME_TYPES
            and mime not in settings.ANNOTATION_MIME_TYPES):
            logger.warning(f'File {file.name}: content type {file.content_type} not supported')
            return False

        return True

    def _store_files(self, request):
        files = request.data.getlist('files')
        dir_path = os.path.join(settings.TMP_DIR, 'requests', str(uuid4()))
        utils.make_dir(dir_path)

        with ThreadPoolExecutor(settings.IMAGE_UPLOADING_THREADS) as ex:
            counts = ex.map(lambda file: self._store_file(file, dir_path), files)
        return sum(counts), dir_path

    @staticmethod
    def _parse_folder_id(request):
        folder_id = request.query_params.get('folder_id')
        if not folder_id:
            return None

        try:
            folder_id = int(folder_id)
        except ValueError:
            return None

        return folder_id

    @staticmethod
    def _is_valid_folder_id(folder_id: int, dataset):
        if folder_id <= 0:
            return False

        exists = ImageFolder.objects.filter(pk=folder_id, dataset=dataset).first()
        return bool(exists)

    @staticmethod
    def get_folder(folder_id: int, dataset: Dataset):
        if folder_id is not None:
            try:
                return ImageFolder.objects.get(pk=max(folder_id, 0), dataset=dataset)
            except (ValueError, ImageFolder.DoesNotExist):
                logger.error(f'Folder with id {folder_id} was not found')

    def _upload_from_request(self, request, dataset: Dataset, annotation_set_id=None):
        folder_id = self._parse_folder_id(request)
        if folder_id and not self._is_valid_folder_id(folder_id, dataset):
            return Response({
                'error': True,
                'detail': "wrong 'folder_id' query parameter",
                'next': None,
                'previous': None,
                'results': [],
                'count': 0
            }, status=400)

        folder = self.get_folder(folder_id, dataset)

        start = datetime.now()
        logger.debug(f'Start upload images and annotations from request for dataset {dataset}')
        annotation_task = parse_annotation_task(request.data.get('annotation_task'))
        resp = self._validate_annotation_set_task(annotation_task, annotation_set_id)
        if resp:
            return resp

        annotation_set_name = request.data.get('annotation_set_name', None)
        annotation_set, resp = self._create_new_annotation_set(dataset, annotation_set_name, annotation_task,
                                                               annotation_set_id, request.user.id)
        if resp:
            return resp

        if annotation_set:
            annotation_set_id = annotation_set.id

        encoding_params = {
            'type': request.data.get('class_encoding_type', 'autodetect')
        }
        raw_class_encoding = request.data.get('class_encoding_raw_content')
        if isinstance(raw_class_encoding, str):
            raw_class_encoding = raw_class_encoding.split('\n')
            encoding_params['raw_content'] = raw_class_encoding
            encoding_params['type'] = 'custom'

        class_encoding = self._parse_class_encoding(encoding_params)

        skip_new_classes = request.data.get('skip_new_classes', False)
        if skip_new_classes in ['true', 'True']:
            skip_new_classes = True

        if annotation_set_id and not annotation_task:
            s = AnnotationSet.objects.get(id=annotation_set_id)
            annotation_task = TaskType(s.task.name)

        # if is_remo_local():
        local_imgs, local_annotations, local_errs = self._upload_local_files(request.user,
                                                                             request.data.getlist('local_files'),
                                                                             dataset,
                                                                             folder, annotation_task,
                                                                             annotation_set_id=annotation_set_id,
                                                                             class_encoding=class_encoding,
                                                                             skip_new_classes=skip_new_classes)
        count, dir_path = self._store_files(request)
        try:
            upload_imgs, upload_annotations, upload_errs = (LocalDatasetUploader(request.user, dataset, dir_path,
                                                                                 annotation_task=annotation_task,
                                                                                 folder=folder,
                                                                                 annotation_set_id=annotation_set_id,
                                                                                 class_encoding=class_encoding,
                                                                                 skip_new_classes=skip_new_classes).upload())
        finally:
            utils.remove_dir(dir_path)

        imgs = local_imgs + upload_imgs
        annotations = local_annotations + upload_annotations
        errs = local_errs + upload_errs

        return Response({'files uploaded': imgs, 'annotations': annotations, 'errors': errs})

        # count, dir_path = self._store_files(request)
        # uploader = LocalDatasetUploader(request.user, dataset, dir_path, annotation_task=annotation_task, folder=folder,
        #                                 annotation_set_id=annotation_set_id, class_encoding=class_encoding, skip_new_classes=skip_new_classes)
        # count, errors = uploader.upload_images()
        # uploader.drop_images()
        # files_need_to_process = uploader.count_files()
        # if files_need_to_process:
        #     enqueue_dataset_job(dataset, JobType.upload_dataset,
        #                         process_files, dir_path, request.user, dataset, annotation_task, folder,
        #                         annotation_set_id, class_encoding, skip_new_classes,
        #                         info=dir_path)
        # logger.debug(f'Uploaded {count} files, dataset {dataset}, elapsed {datetime.now() - start}')
        # return Response({'status': f'uploaded {count} files', 'errors': errors})

    def _validate_annotation_set_task(self, annotation_task, annotation_set_id):
        if annotation_set_id and annotation_task:
            s = AnnotationSet.objects.get(id=annotation_set_id)
            annotation_set_task = TaskType(s.task.name)
            if annotation_set_task != annotation_task:
                return Response({
                    'error': f'Annotation set #{annotation_set_id} task ({annotation_set_task}) does not match with giving task - {annotation_task}'},
                    status=status.HTTP_400_BAD_REQUEST)

    def _create_new_annotation_set(self, dataset, annotation_set_name, annotation_task, annotation_set_id, user_id):
        if isinstance(annotation_set_name, str):
            annotation_set_name = annotation_set_name.strip()
        else:
            return None, None

        if not annotation_set_name:
            return None, None

        if annotation_set_id:
            return None, Response({
                'error': f'You can not create new annotation set with giving id #{annotation_set_id}'},
                status=status.HTTP_400_BAD_REQUEST)

        if not annotation_task:
            return None, None

        s = AnnotationSet.objects.filter(dataset=dataset, name=annotation_set_name).first()
        if s:
            t = TaskType(s.task.name)
            if t != annotation_task:
                return None, Response({
                    'error': f'Annotation set with giving name "{annotation_set_name}" has different task: {t}'},
                    status=status.HTTP_400_BAD_REQUEST)
            else:
                return s, None

        try:
            with transaction.atomic():
                task = Task.objects.get(type=annotation_task.name)
                s = AnnotationSet.objects.create(
                    name=annotation_set_name,
                    type=AnnotationSetType.image.value,
                    task=task,
                    user_id=user_id,
                    dataset=dataset
                )
        except IntegrityError:
            s = AnnotationSet.objects.filter(dataset=dataset, name=annotation_set_name).first()
            if not s:
                return None, Response({
                    'error': f'Failed to create and retrieve annotation set with giving name "{annotation_set_name}".'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return s, None

    def _parse_class_encoding(self, class_encoding):
        """
        class_encoding = {
            'type': autodetect | custom | WordNet | GoogleKnowledgeGraph,
            'classes': {'label': 'class_name'} | 'local_path': '<path>' | 'raw_content': [..lines..]
        }
        """
        if not class_encoding:
            class_encoding = {'type': 'autodetect'}

        encoding_type = class_encoding.get('type')
        if encoding_type == ClassEncodingType.autodetect:
            return None

        if encoding_type == ClassEncodingType.custom:
            classes = class_encoding.get('classes')
            if classes:
                return CustomClassEncoding(classes)

            local_path = class_encoding.get('local_path')
            if local_path:
                return parse_csv_class_encoding(local_path)

            raw_content = class_encoding.get('raw_content')
            if raw_content:
                return parse_raw_csv_class_encoding(raw_content)

        if encoding_type in [ClassEncodingType.word_net, ClassEncodingType.google_knowledge_graph]:
            return class_encoding_factory.get(encoding_type)

        return None

    def _upload_from_url(self, request, dataset: Dataset, annotation_set_id=None):
        data = json.loads(request.body)
        annotation_task = parse_annotation_task(data.get('annotation_task'))
        resp = self._validate_annotation_set_task(annotation_task, annotation_set_id)
        if resp:
            return resp

        if annotation_set_id and not annotation_task:
            s = AnnotationSet.objects.get(id=annotation_set_id)
            annotation_task = TaskType(s.task.name)

        annotation_set_name = data.get('annotation_set_name', None)
        annotation_set, resp = self._create_new_annotation_set(dataset, annotation_set_name, annotation_task,
                                                               annotation_set_id, request.user.id)
        if resp:
            return resp

        if annotation_set:
            annotation_set_id = annotation_set.id

        class_encoding = self._parse_class_encoding(data.get('class_encoding'))

        skip_new_classes = data.get('skip_new_classes', False)
        if skip_new_classes in ['true', 'True']:
            skip_new_classes = True

        urls = data.get('urls', [])
        folder_id = data.get('folder_id')
        folder = self.get_folder(folder_id, dataset)

        for url in urls:
            ok, error = self._validate_url(url)
            if not ok:
                return Response({'error': error}, status=status.HTTP_400_BAD_REQUEST)

        # if is_remo_local():
        img_count, annotation_count, errs = self._upload_local_files(request.user, data.get('local_files'), dataset,
                                                                     folder, annotation_task,
                                                                     annotation_set_id=annotation_set_id,
                                                                     class_encoding=class_encoding,
                                                                     skip_new_classes=skip_new_classes)
        for url in urls:
            extract_dir = os.path.join(settings.TMP_DIR, 'url', str(uuid4()))
            images_count, annotations_count, errors = RemoteDatasetUploader(url, request.user, dataset,
                                                                            annotation_task,
                                                                            folder,
                                                                            annotation_set_id=annotation_set_id,
                                                                            class_encoding=class_encoding,
                                                                            skip_new_classes=skip_new_classes
                                                                            ).upload(extract_dir)
            img_count += images_count
            annotation_count += annotations_count
            errs += errors
        return Response({'files uploaded': img_count, 'annotations': annotation_count, 'errors': errs})

        # jobs = []
        # for url in urls:
        #     job = enqueue_dataset_job(dataset, JobType.upload_dataset,
        #                               job_upload_dataset, url, request.user, dataset, annotation_task, folder,
        #                               annotation_set_id, class_encoding, skip_new_classes,
        #                               info=url)
        #     jobs.append((job.id, job.get_status()))
        # if not jobs:
        #     return Response()
        # return Response({'jobs': [{'job_id': job_id, 'status': job_status} for job_id, job_status in jobs]})

    def _upload_local_files(self, user, local_files: List[str], dataset: Dataset, folder: ImageFolder,
                            annotation_task: TaskType = None, annotation_set_id=None, class_encoding=None, skip_new_classes=False) -> (
        int, int, []):
        if local_files:
            return upload_local_files(user, local_files, dataset, folder, annotation_task,
                                      annotation_set_id=annotation_set_id, class_encoding=class_encoding, skip_new_classes=skip_new_classes)
        return 0, 0, []

    @staticmethod
    def _validate_url(url):
        try:
            validate = URLValidator()
            validate(url)
        except ValidationError:
            return False, 'invalid URL'

        error = None
        try:
            resp = requests.get(url, stream=True)
            if resp.status_code != 200:
                error = 'invalid URL'
            resp.close()
        except Exception as err:
            error = str(err)

        return error is None, error
