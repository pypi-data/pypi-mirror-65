import json
from typing import Dict, Optional

from json_datetime_noamfisher.consts import (VALUE_KEY, TYPE_KEY, SUPPORTED_TIME_CLASSES, SUPPORTED_TIME_CLASSES_TYPES)


class JsonDatetimeDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        super(JsonDatetimeDecoder, self).__init__(*args, object_hook=self._object_hook, **kwargs)

    def _object_hook(self, obj: Dict):
        obj_type = obj.get(TYPE_KEY)
        value = obj.get(VALUE_KEY)

        obj_cls = self._get_obj_datetime_cls(obj_type)
        if obj_cls is not None and isinstance(value, str) and len(obj) == 2:
            try:
                return obj_cls.fromisoformat(value)
            except ValueError:
                pass

        return obj

    def _get_obj_datetime_cls(self, obj_type: str) -> Optional[SUPPORTED_TIME_CLASSES_TYPES]:
        for cls in SUPPORTED_TIME_CLASSES.__args__:
            if cls.__name__ == obj_type:
                return cls

    def _dead_code(self):
        print(123)