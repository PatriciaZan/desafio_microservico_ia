import re
import unicodedata

# Ajuda da IA para construir essa BRAND_ALIASES e o unicodedata abaixo
BRAND_ALIASES = {
    "Acme": [
        "acme",
        "a.c.m.e.",
        "acme corp",
    ],
    "Zenith": [
        "zenith",
    ],
    "Nimbus": [
        "nimbus",
    ],
}

def normalize_for_brands(text: str) -> str:
    text = text.lower()
    text = unicodedata.normalize(
        "NFKD",
        text,
    )

    text = "".join(
        char
        for char in text
        if not unicodedata.combining(char)
    )

    text = re.sub(
        r"[^a-z0-9]+",
        "",
        text,
    )

    return text