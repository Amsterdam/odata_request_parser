from pytest import fixture
import pytest
from odata_request_parser.main import OdataSelectParser


@fixture
def parser():
    return OdataSelectParser()


@pytest.mark.parametrize(
    "value,expected",
    [
        (["field_1"], "field_1"),
        (["field_2", "field_3"], "field_2,field_3"),
        (["field 4", "field 5", "field 6"], "field 4,field 5,field 6"),
    ],
)
def test_parse_single_input(value, expected, parser):
    parser.add_fields(value)
    res = parser.parse()
    assert res == expected


@pytest.mark.parametrize("value", ["field_1", 123, {"field_1"}])
def test_parse_non_list_input(value, parser):
    with pytest.raises(AssertionError):
        parser.add_fields(value)


def test_parse_multiple_input(parser):
    values = [
        ["field 1", "field 2"],
        ["field 3"],
        ["field 4", "field 5"]
    ]
    for val in values:
        parser.add_fields(val)
    res = parser.parse()
    assert res == "field 1,field 2,field 3,field 4,field 5"
