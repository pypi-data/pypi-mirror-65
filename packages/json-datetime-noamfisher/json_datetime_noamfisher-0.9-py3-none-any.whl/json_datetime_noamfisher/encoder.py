import json
from typing import Union, Any

from json_datetime_noamfisher.consts import (SUPPORTED_TIME_CLASSES, VALUE_KEY, TYPE_KEY)


class JsonDatetimeEncoder(json.JSONEncoder):
    def default(self, o: Union[Any, SUPPORTED_TIME_CLASSES]):
        if isinstance(o, SUPPORTED_TIME_CLASSES.__args__):
            return {
                TYPE_KEY: type(o).__name__,
                VALUE_KEY: o.isoformat()
            }
        return super(JsonDatetimeEncoder, self).default(o)
