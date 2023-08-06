import datetime
import json
import os

import pytest

from json_datetime_noamfisher.consts import DATETIME_CLS, DATE_CLS, TIME_CLS
from json_datetime_noamfisher.decoder import JsonDatetimeDecoder
from json_datetime_noamfisher.encoder import JsonDatetimeEncoder


@pytest.mark.parametrize(
    'the_json',
    [
        {'a': DATETIME_CLS(2020, 3, 24, 11, 52, 34, 123456)},
        {'a': DATE_CLS(2020, 3, 24)},
        {'a': TIME_CLS(12, 34, 56, 789012)},
        [DATETIME_CLS(2020, 3, 24, 11, 52, 34, 123456), DATE_CLS(2020, 3, 24), TIME_CLS(12, 34, 56, 789012)],
        {'a': [DATETIME_CLS(2020, 3, 24, 11, 52, 34, 123456), DATE_CLS(2020, 3, 24), TIME_CLS(12, 34, 56, 789012)]}
    ])
def test_encode_decode(the_json):
    encoded = json.dumps(the_json, cls=JsonDatetimeEncoder)
    decoded = json.loads(encoded, cls=JsonDatetimeDecoder)
    assert the_json == decoded


class A:
    pass


@pytest.mark.parametrize(
    'the_json',
    [
        {'a': A()}
    ]
)
def test_not_serializable_object(the_json):
    with pytest.raises(TypeError):
        json.dumps(the_json, cls=JsonDatetimeEncoder)


@pytest.mark.parametrize(
    'encoded, expected_decoded',
    [
        (
                """{"a": {"__type__": "datetime", "__value__": "not_a_valid_datetime_value"}}""",
                {"a": {"__type__": "datetime", "__value__": "not_a_valid_datetime_value"}}
        )
    ]
)
def test_not_deserializable_json(encoded: str, expected_decoded):
    decoded = json.loads(encoded, cls=JsonDatetimeDecoder)
    assert decoded == expected_decoded


@pytest.mark.skipif(os.environ.get('COVID_19_DATA_PATH') is None,
                    reason="missing COVID_19_DATA_PATH environment variable")
def test_data_file():
    path = os.environ['COVID_19_DATA_PATH']
    patients = json.load(open(path), cls=JsonDatetimeDecoder)
    for patient in patients:
        assert isinstance(patient['infection_time'], datetime.datetime)
