# Receber uma resposta limpa e descobrir quais marcas monitoradas aparecem nela.
import re

from src.models.mention import Mention


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


def detect_mentions(
    text: str,
) -> list[Mention]:

    mentions: list[Mention] = []

    occupied_ranges: list[tuple[int, int]] = []

    for brand, aliases in BRAND_ALIASES.items():

        aliases = sorted(
            aliases,
            key=len,
            reverse=True,
        )

        for alias in aliases:
            pattern = re.escape(alias)
            for match in re.finditer(
                pattern,
                text,
                flags=re.IGNORECASE,
            ):

                start = match.start()
                end = match.end()
                overlaps = any(
                    start < existing_end
                    and end > existing_start
                    for existing_start, existing_end
                    in occupied_ranges
                )

                if overlaps:
                    continue

                mentions.append(
                    Mention(
                        brand=brand,
                        matched_text=match.group(),
                    )
                )

                occupied_ranges.append(
                    (start, end)
                )

    return mentions