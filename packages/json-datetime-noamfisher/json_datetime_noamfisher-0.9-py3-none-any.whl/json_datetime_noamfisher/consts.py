import datetime
from typing import Union, Type

DATETIME_CLS = datetime.datetime
DATE_CLS = datetime.date
TIME_CLS = datetime.time
SUPPORTED_TIME_CLASSES = Union[DATETIME_CLS, DATE_CLS, TIME_CLS]
SUPPORTED_TIME_CLASSES_TYPES = Union[Type[DATE_CLS], Type[DATETIME_CLS], Type[TIME_CLS]]
TYPE_KEY = '__type__'
VALUE_KEY = '__value__'
