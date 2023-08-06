from kpl_helper.base import get_config


class RectangleBoxObjectDetectionResponse:
    _response_type = "rectangle_box_detection"

    def __init__(self, height, width, depth):
        self.height = height
        self.width = width
        self.depth = depth
        self.objects = []

    def add_object(self, name, xmin, ymin, xmax, ymax, score):
        self.objects.append({
            "name": name,
            "score": float(score),
            "xmin": int(xmin),
            "ymin": int(ymin),
            "xmax": int(xmax),
            "ymax": int(ymax)
        })

    def dumps(self):
        return {
            "type": type(self)._response_type,
            "height": self.height,
            "width": self.width,
            "depth": self.depth,
            "objects": self.objects
        }


class ClassificationResponse:
    _response_type = "classification"

    @staticmethod
    def dumps(height, width, depth, class_id, class_name=None):
        return {
            "type": ClassificationResponse._response_type,
            "height": height,
            "width": width,
            "depth": depth,
            "class_id":class_id,
            "class_name": class_name,
        }


class SegmentationResponse:
    _response_type = "segmentation"

    @staticmethod
    def dumps(height, width, depth, mask):
        return {
            "type": SegmentationResponse._response_type,
            "height": height,
            "width": width,
            "depth": depth,
            "mask": mask,
        }

