import json

from pathlib import Path

from src.services.validate_response import validate_response


def load_responses(file_content: bytes) -> list[dict]:
    try:
        data = json.loads(file_content.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValueError("Arquivo JSON inválido {} :".format(error))

    if not isinstance(data, list):
        raise ValueError("O arquivo JSON deve conter uma lista de respostas.")

    return data



FILE_NAME = "respostas-exemplo.json"
ROOT_DIR = Path(__file__).parent.parent.parent
FILE_PATH = ROOT_DIR / "data" / FILE_NAME

def load_responses_local() -> list[dict]:
    path = FILE_PATH

    if not path.exists():
        raise FileNotFoundError("Arquivo não encontrado: {}".format(path))

    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    if not isinstance(data, list):
        raise ValueError("O arquivo JSON deve conter uma lista de respostas.")

    return data

# mantém o conjunto de respostas
# separar depois ou não?
def save_responses(
    responses: list[dict],
) -> None:

    with FILE_PATH.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            responses,
            file,
            ensure_ascii=False,
            indent=2,
        )

def add_response(
    response: dict,
) -> None:

    responses = load_responses_local()

    existing_ids = {
        item.get("id")
        for item in responses
    }

    # Validar com IDs existentes
    validate_response(response, existing_ids=existing_ids)

    responses.append(response)
    save_responses(responses)