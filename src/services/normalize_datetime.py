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

    value = value.strip()
    if not value:
        return None

    for date_format in DATE_FORMATS:
        try:
            dt = datetime.strptime(value, date_format)
            # Retorna padronizado como string ISO (ex: "2026-01-15T00:00:00")
            print(dt.isoformat())
            return dt.isoformat()
        except ValueError:
            continue

    # Caso queira que retorne None em vez de crashar a aplicação com dados sujos do scraping:
    return None