from pytest import fixture
import pytest
from odata_request_parser.main import OdataFilterParser


@fixture
def parser():
    return OdataFilterParser()


@pytest.mark.parametrize(
    "value,expected",
    [
        ([{"_eq": {"left": "right"}}], "left eq 'right'"),
        ([{"_has": {"val1": "val2"}}], "val1 has 'val2'"),
        (
            [{"_has": {"val1": "val2"}}, {"_lt": {"val3": "val4"}}],
            "val1 has 'val2' and val3 lt 'val4'",
        ),
    ],
)
def test_simple_filter(value, expected, parser):
    """ Some simple filter definitions """
    res = parser.parse(value)
    assert res == expected


def test_or_filter(parser):
    """ A simple use of the or operator """
    filter = [
        {
            "_or": [
                {"_has": {"val1": "val2"}},
                {"_lt": {"val3": "val4"}},
            ]
        }
    ]
    expected = "(val1 has 'val2' or val3 lt 'val4')"

    res = parser.parse(filter)
    assert res == expected


def test_complex_or_filter(parser):
    """ We are using a slightly more complex or statement here"""
    filter = [
        {"_le": {"left": "right"}},
        {
            "_or": [
                {"_has": {"val1": "val2"}},
                {"_lt": {"val3": "val4"}},
            ]
        },
        {"_gt": {"left": "right"}},
    ]
    expected = (
        "left le 'right' and (val1 has 'val2' or val3 lt 'val4') and left gt 'right'"
    )

    res = parser.parse(filter)
    assert res == expected


def test_nested_or_filter(parser):
    """ This or statement is nested one layer deeper """
    filter = [
        {"_has": {"some": "thing"}},
        {
            "_or": [
                {"_and": [{"_ge": {"val_5": "val_6"}}, {"_le": {"val_7": "val_8"}}]},
                {"_has": {"val1": "val2"}},
                {"_or": [{"_eq": {"odata": "parser"}}, {"_lt": {"select": "filter"}}]},
            ]
        },
    ]
    expected = (
        "some has 'thing' and ("
        "(val_5 ge 'val_6' and val_7 le 'val_8') or "
        "val1 has 'val2' or "
        "(odata eq 'parser' or select lt 'filter')"
        ")"
    )
    res = parser.parse(filter)
    assert res == expected


@pytest.mark.parametrize(
    "value,expected_exception",
    [
        ({"_eq": {"left": "right"}}, AssertionError),  # Should be a list of dicts
        ([{"_or": {"left": "right"}}], AssertionError),  # _or and _and operators should contain a list
        ([{"_and": {"left": "right"}}], AssertionError),
        ([{"_eq": ("left", "right")}], AssertionError),  # the dict value should be another dict
        ([{"_eq": {"left": "right"}, "eq": {"up": "down"}}], AssertionError),  # The outer dict should have length 1
        ([{"_eq": {"left": "right", "up": "down"}}], AssertionError),  # The inner dict should have length 1
        ([{"_gibberish": {"left": "right"}}], NotImplementedError),  # The operator should be implemented
    ],
)
def test_simple_filter(value, expected_exception, parser):
    with pytest.raises(expected_exception):
        parser.parse(value)
