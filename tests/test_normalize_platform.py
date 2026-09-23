import pytest

from src.services.normalize_platform import normalize_platform
# Aqui estamos testando tanto os aliases que você definiu quanto o comportamento para plataformas desconhecidas. Sua implementação usa strip().lower() para procurar o alias e, se não encontrar, retorna a versão com espaços externos removidos.

@pytest.mark.parametrize(
    "value, expected",
    [
        ("chatgpt", "ChatGPT"),
        ("CHATGPT", "ChatGPT"),
        ("chat-gpt", "ChatGPT"),
        ("chat gpt", "ChatGPT"),
        ("gemini", "Gemini"),
        ("GEMINI", "Gemini"),
        ("perplexity", "Perplexity"),
        ("PERPLEXITY", "Perplexity"),
    ],
)
def test_normalize_platform_aliases(value, expected):
    assert normalize_platform(value) == expected


def test_normalize_platform_removes_spaces():
    assert normalize_platform("  chatgpt  ") == "ChatGPT"


def test_normalize_platform_unknown_value():
    assert normalize_platform("Claude") == "Claude"