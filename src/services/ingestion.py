import json
from pathlib import Path

# Carrega o arquivo em /data/

def load_responses(file_path: str | Path) -> list[dict]:
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError("Arquivo não encontrado: {}".format(path))

    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    if not isinstance(data, list):
        raise ValueError("O arquivo JSON deve conter uma lista de respostas.")

    return data