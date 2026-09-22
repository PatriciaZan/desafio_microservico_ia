from datetime import datetime, timezone
from fastapi import FastAPI, HTTPException, UploadFile, File, Query, status
from starlette.middleware.cors import CORSMiddleware

from src.services.get_analyzed_responses import get_analysis_data
from src.services.analyze_response import analyze_responses
from src.services.cleaning import clean_responses
from src.services.ingestion import load_responses
from src.services.report import build_analysis_result

from src.models.response import Response

from src.metrics.metric_share_of_voice import calculate_share_of_voice
from src.metrics.metric_top_citation import get_top_citations

# Decidi manter os "tratamentos" de erros aqui mesmo, evitando criar muitos arquivos e deixando esta lógica mais contida.

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



@app.get("/health", status_code=status.HTTP_200_OK, summary="Verifica a saúde da API")
def health_check():
    return {
        "status": "ok"
    }


# Para testar com o uplaod de arquivos
@app.post("/analyze",  status_code=status.HTTP_200_OK, summary="Analisa um arquivo separado/diferente de respostas fornecido pelo usuário.")
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
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        )

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        )

@app.get("/share-of-voice" , status_code=status.HTTP_200_OK, summary="Calcula o Share of Voice de uma marca")
def share_of_voice(
    marca: str = Query(..., min_length=1, description="Nome da marca monitorada (Acme | Zenith | Nimbus)")
):
    try:
        _, analyzed_responses = get_analysis_data()

        return calculate_share_of_voice(
            analyzed_responses,
            marca,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        )

@app.get("/top-citacoes" , status_code=status.HTTP_200_OK, summary="Retorna as principais citações em hanking")
def top_citations(
    n: int = Query(
        5,
        ge=1,
        le=100,
        description="Número de registros a retornar"
    )
):

    try:
        _, analyzed_responses = get_analysis_data()
        return {
            "limit": n,
            "results": get_top_citations(
                analyzed_responses,
                n,
            ),
        }

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        )

@app.post("/respostas", status_code=status.HTTP_201_CREATED, summary="Adiciona uma nova resposta ao arquivo local respostas-exemplo.json")
def create_response(
    response: Response,
):
    try:
        response.model_dump(mode="json")

        return {
            "message": "Resposta adicionada com sucesso.",
            "id": response.id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        )