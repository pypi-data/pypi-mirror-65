import threading

from remo_app.remo.api.constants import TaskType
from remo_app.remo.models import Annotation, AnnotationObject
from remo_app.remo.models.annotation import NewAnnotation, AnnotationClassRel

lock = threading.Lock()


def update_new_annotation(annotation: Annotation):
    with lock:
        if annotation is None:
            return

        new_annotation = NewAnnotation()
        qs = NewAnnotation.objects.filter(image=annotation.image, annotation_set=annotation.annotation_set)
        if qs:
            new_annotation = qs.first()
        new_annotation.annotation_set = annotation.annotation_set
        new_annotation.image = annotation.image
        new_annotation.dataset = annotation.image.dataset
        new_annotation.tags = [obj.name for obj in annotation.tags.distinct()]
        new_annotation.task = annotation.annotation_set.task.type
        new_annotation.status = annotation.status

        objs = AnnotationObject.objects.filter(annotation=annotation)
        objects = []
        classes = set()
        if new_annotation.task == TaskType.image_classification.name:
            annotation_classes = AnnotationClassRel.objects.filter(annotation=annotation)
            obj_classes = [rel.annotation_class.name for rel in annotation_classes]
            objects.append({
                'classes': obj_classes
            })
            classes = classes.union(obj_classes)
        else:
            for obj in objs:
                obj_classes = [c.name for c in obj.classes.all()]
                objects.append({
                    'name': obj.name,
                    'coordinates': obj.coordinates,
                    'classes': obj_classes
                })
                classes = classes.union(obj_classes)
        new_annotation.classes = list(classes)
        new_annotation.data = {'objects': objects}
        new_annotation.save()
