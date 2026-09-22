from pydantic import BaseModel

# Modelo para definir o padrão da resposta
# NONE para quando ausente/nulo, como acontece em r004 etc...

class Response(BaseModel):
    id: str
    pergunta: str
    plataforma: str
    modelo: str | None
    resposta_texto: str
    data_hora: str | None
    sentimento: str | None