import pytest

from src.services.normalize_datetime import normalize_datetime


@pytest.mark.parametrize(
    "value, expected",
    [
        (
            "2026-09-22",
            "2026-09-22T00:00:00",
        ),
        (
            "2026-09-22T15:30:00",
            "2026-09-22T15:30:00",
        ),
        (
            "22/09/2026",
            "2026-09-22T00:00:00",
        ),
        (
            "2026/09/22",
            "2026-09-22T00:00:00",
        ),
    ],
)
def test_normalize_datetime_valid_formats(value, expected):
    assert normalize_datetime(value) == expected


def test_normalize_datetime_returns_none_for_none():
    assert normalize_datetime(None) is None


def test_normalize_datetime_returns_none_for_empty_string():
    assert normalize_datetime("") is None


def test_normalize_datetime_returns_none_for_invalid_date():
    assert normalize_datetime("2026-99-99") is None