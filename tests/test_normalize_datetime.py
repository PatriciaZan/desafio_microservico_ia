import pytest
from src.services.normalize_datetime import normalize_datetime

# Criando uma versão de teste utilizando classe para ver como fica

class TestNormalizeDatetimeValidFormats:
    @pytest.mark.parametrize(
        "input_date,expected",
        [
            ("2026-09-22", "2026-09-22T00:00:00"),
            ("2026-09-22T15:30:00", "2026-09-22T15:30:00"),
            ("22/09/2026", "2026-09-22T00:00:00"),
            ("2026/09/22", "2026-09-22T00:00:00"),
        ],
    )
    def test_valid_formats(self, input_date, expected):
        assert normalize_datetime(input_date) == expected


class TestNormalizeDatetimeEdgeCases:
    def test_none_value(self):
        assert normalize_datetime(None) is None

    def test_empty_string(self):
        assert normalize_datetime("") is None

    def test_invalid_date(self):
        with pytest.raises(ValueError, match="invalid_datetime"):
            normalize_datetime("2026-99-99")

