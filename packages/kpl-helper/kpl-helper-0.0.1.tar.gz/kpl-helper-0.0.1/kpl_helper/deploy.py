
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

    def __init__(self, class_id, class_name=None):
        self.class_id = class_id
        self.class_name = class_name

    def dumps(self):
        return {
            "type": type(self)._response_type,
            "class_id": self.class_id,
            "class_name": self.class_name,
        }

