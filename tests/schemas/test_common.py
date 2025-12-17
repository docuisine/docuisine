from pytest import raises

from docuisine.schemas.common import _has_only_digits, _has_two_dots


def test_has_two_dots_valid():
    ## No validation errors should be raised
    assert _has_two_dots("1.0.0") == "1.0.0"
    assert _has_two_dots("10.20.30") == "10.20.30"


def test_has_two_dots_invalid():
    ## Validation errors should be raised
    with raises(ValueError, match="Version must have two dots"):
        _has_two_dots("1.0")
    with raises(ValueError, match="Version must have two dots"):
        _has_two_dots("1.0.1.1")


def test_has_only_digits_valid():
    ## No validation errors should be raised
    assert _has_only_digits("1.0.0") == "1.0.0"
    assert _has_only_digits("10.20.30") == "10.20.30"


def test_has_only_digits_invalid():
    ## Validation errors should be raised
    with raises(ValueError, match="Version parts must be numeric"):
        _has_only_digits("1.a.0")
    with raises(ValueError, match="Version parts must be numeric"):
        _has_only_digits("1.0.b")
