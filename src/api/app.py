from fastapi import FastAPI, HTTPException, UploadFile, File
from starlette.middleware.cors import CORSMiddleware

from src.services.analyze_response import analyze_responses
from src.services.cleaning import clean_responses
from src.services.ingestion import load_responses
from src.services.report import build_analysis_result


app = FastAPI(
    title="Brand Monitoring API",
    description="API para análise de menções de marcas em respostas geradas por IA.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/health")
def health_check():
    return {
        "status": "ok"
    }


@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    # como agora pode vir qualquer tipo de arquivo eu tenho que validar primeiro
    if file.content_type != "application/json" and not file.filename.endswith(".json"):
        raise HTTPException(
            status_code=400,
            detail="O arquivo deve ter o formato .json"
        )
    try:
        file_content = await file.read()

        #records = load_responses("data/respostas-exemplo.json")
        records = load_responses(file_content)

        ingestion_result = clean_responses(records)

        analyzed_responses = analyze_responses(ingestion_result.responses)

        return build_analysis_result(
            ingestion_result,
            analyzed_responses,
        )

    except FileNotFoundError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error),
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )