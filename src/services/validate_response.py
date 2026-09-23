from src.models.response import Response

'''
def validate_response(response: Response):
    if not response.pergunta.strip():
        raise ValueError("A pergunta não pode estar vazia.")

    if not response.resposta_texto.strip():
        raise ValueError("A resposta não pode estar vazia.")
'''

from datetime import datetime
from src.models.response import Response

VALID_SENTIMENTS = {"positivo", "neutro", "negativo", None}
VALID_PLATFORMS = {"ChatGPT", "Gemini", "Perplexity", "chat-gpt", "chatgpt", "gemini"}


def validate_response(response: Response | dict, existing_ids: set = None) -> None:
    if existing_ids is None:
        existing_ids = set()

    if isinstance(response, dict):
        response = Response(**response)

    # Validar ID
    if not response.id or not str(response.id).strip():
        raise ValueError("ID da resposta não pode estar vazio.")

    if response.id in existing_ids:
        raise ValueError(f"A resposta com ID '{response.id}' já existe.")

    # Validar pergunta
    if not response.pergunta or not str(response.pergunta).strip():
        raise ValueError("Pergunta não pode estar vazia.")

    # Validar plataforma
    if not response.plataforma or not str(response.plataforma).strip():
        raise ValueError("Plataforma não pode estar vazia.")

    # Validar data/hora
    if response.data_hora is not None:
        try:
            if isinstance(response.data_hora, str):
                # Tenta diversos formatos comuns
                formatos = [
                    "%Y-%m-%dT%H:%M:%S",
                    "%d/%m/%Y",
                    "%Y/%m/%d",
                    "%Y-%m-%d",
                ]
                data_valida = False
                for fmt in formatos:
                    try:
                        datetime.strptime(response.data_hora, fmt)
                        data_valida = True
                        break
                    except ValueError:
                        continue

                if not data_valida:
                    raise ValueError(
                        f"Formato de data/hora inválido: '{response.data_hora}'. "
                        "Use ISO (YYYY-MM-DDTHH:MM:SS) ou DD/MM/YYYY."
                    )
        except Exception as e:
            if "Formato de data/hora" not in str(e):
                raise ValueError(f"Erro ao validar data/hora: {str(e)}")
            raise

    # Validar sentimento
    if response.sentimento is not None:
        if response.sentimento not in VALID_SENTIMENTS:
            raise ValueError(
                f"Sentimento inválido: '{response.sentimento}'. "
                f"Valores permitidos: {', '.join(str(s) for s in VALID_SENTIMENTS if s is not None)}, ou null."
            )

    # Modelo pode ser nulo, sem validação necessária