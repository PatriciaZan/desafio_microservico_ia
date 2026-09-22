from fastapi import FastAPI, HTTPException, UploadFile, File, Query
from starlette.middleware.cors import CORSMiddleware

from src.services.validate_response import validate_response
from src.models.response import Response
from src.services.metrics import calculate_share_of_voice, get_top_citations
from src.services.analyze_response import analyze_responses
from src.services.cleaning import clean_responses
from src.services.ingestion import load_responses, load_responses_local, add_response
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


# Para testar com o uplaod de arquivos
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

@app.get("/share-of-voice")
def share_of_voice(
    marca: str = Query(..., min_length=1)
):
    try:
        records = load_responses_local()
        ingestion_result = clean_responses(records)
        analyzed_responses = analyze_responses(ingestion_result.responses)
        return calculate_share_of_voice(
            analyzed_responses,
            marca,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )

@app.get("/top-citacoes")
def top_citations(
    n: int = Query(
        5,
        ge=1,
        le=100,
    )
):
    try:
        records = load_responses_local()

        ingestion_result = clean_responses(records)
        analyzed_responses = analyze_responses(ingestion_result.responses)

        return {
            "limit": n,
            "results": get_top_citations(
                analyzed_responses,
                n,
            ),
        }

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )

@app.post("/respostas")
def create_response(
    response: Response,
):
    try:
        validate_response(response)

        add_response(
            response.model_dump(
                mode="json"
            )
        )

        return {
            "message": "Resposta adicionada com sucesso.",
            "id": response.id,
        }

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )