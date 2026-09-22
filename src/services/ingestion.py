import json


def load_responses(file_content: bytes) -> list[dict]:
    try:
        data = json.loads(file_content.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValueError("Arquivo JSON inválido {} :".format(error))

    if not isinstance(data, list):
        raise ValueError("O arquivo JSON deve conter uma lista de respostas.")

    return data

'''
from pathlib import Path
# Carrega o arquivo em /data/
# antigo para testar
# pegava o arquivo localmente
def load_responses(file_path: str | Path) -> list[dict]:
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError("Arquivo não encontrado: {}".format(path))

    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    if not isinstance(data, list):
        raise ValueError("O arquivo JSON deve conter uma lista de respostas.")

    return data

'''