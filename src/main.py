from services.analyze_response import analyze_responses
from services.report_terminal import build_report_terminal
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

    analyzed_responses = analyze_responses(responses.responses)

    report = build_report_terminal(
        responses,
        analyzed_responses,
    )

    print(report)

if __name__ == "__main__":
    main()