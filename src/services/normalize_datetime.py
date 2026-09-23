from datetime import datetime

# Eu quero que tudo retorne um padrão normal do timestamp aqui
DATE_FORMATS = [
    "%Y-%m-%dT%H:%M:%S",
    "%Y-%m-%d",
    "%d/%m/%Y",
    "%Y/%m/%d",
]


def normalize_datetime(value: str | None) -> str | None:
    if not value or not isinstance(value, str):
        return None

    if not isinstance(value, str):
        raise ValueError("invalid_datetime")

    value = value.strip()

    if not value:
        return None

    for date_format in DATE_FORMATS:
        try:
            dt = datetime.strptime(value, date_format)
            return dt.isoformat()
        except ValueError:
            continue
    raise ValueError("invalid_datetime")
    #return None