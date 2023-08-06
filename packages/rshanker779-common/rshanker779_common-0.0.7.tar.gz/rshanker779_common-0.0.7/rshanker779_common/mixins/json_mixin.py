import json


class JSONMixin:
    def to_json(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        return self.__convert_item(self.__dict__)

    def __convert_item(self, value):
        if isinstance(value, JSONMixin):
            return {value.__class__.__name__: value.to_dict()}

        elif isinstance(value, dict):
            return {i: self.__convert_item(v) for i, v in value.items()}
        elif isinstance(value, (list, tuple, set)):
            return [self.__convert_item(i) for i in value]
        return value
