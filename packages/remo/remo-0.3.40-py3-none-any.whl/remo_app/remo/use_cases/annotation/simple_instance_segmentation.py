import csv
import io

from remo_app.remo.api.constants import TaskType
from remo_app.remo.models.annotation import NewAnnotation
from remo_app.remo.use_cases.annotation.json import BaseExporter


class PlainCsvInstanceSegmentation(BaseExporter):
    task = TaskType.instance_segmentation

    def export_annotations(self, annotation_set, export_coordinates='pixel', full_path=False, export_classes=False):
        """
        Exports annotations in CSV format
        """
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['file_name', 'classes', 'coordinates'])

        for annotation in NewAnnotation.objects.filter(annotation_set=annotation_set):
            file_name = annotation.image.original_name

            if full_path and annotation.image.image_object.local_image:
                file_name = annotation.image.image_object.local_image

            width, height = annotation.image.dimensions()

            for obj in annotation.data.get('objects', []):
                coordinates = obj.get('coordinates', [])
                points = []
                for p in coordinates:
                    if export_coordinates == 'pixel':
                        points.append(int(p['x']))
                        points.append(int(p['y']))
                    elif export_coordinates == 'percent':
                        points.append(float(p['x']) / width)
                        points.append(float(p['y']) / height)

                classes = obj.get('classes', [])
                encoded = self.encode_classes(classes)
                classes_csv = "; ".join(encoded)
                points_csv = "; ".join(map(str, points))
                writer.writerow([file_name, classes_csv, points_csv])

        return output.getvalue()
