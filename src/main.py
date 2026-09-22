from src.services.cleaning import clean_responses
from src.services.ingestion import load_responses

from pathlib import Path

FILE_NAME = "respostas-exemplo.json"

ROOT_DIR = Path(__file__).parent.parent
FILES_PATH = ROOT_DIR / "data" / FILE_NAME

def main():
    records = load_responses(FILES_PATH)
    responses = clean_responses(records)
    print(responses)

    # ! remover depois, caso eu ainda queira visualizar no desenvolvimento
    #print(f"Registros recebidos: {len(records)}")
    #print(
    #   f"Registros após limpeza: "
    #   f"{len(responses)}"
    #)
   # for response in responses:
     #   print(response.model_dump())


if __name__ == "__main__":
    main()