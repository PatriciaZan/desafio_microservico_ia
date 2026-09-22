from collections import Counter

from src.models.analyzed_response import AnalyzedResponse
from src.models.ingestion import IngestionResult


def build_report_terminal(
    ingestion: IngestionResult,
    analyzed: list[AnalyzedResponse],
) -> str:

    total_mentions = sum(
        len(response.mentions)
        for response in analyzed
    )

    brand_counter = Counter()

    for response in analyzed:
        for mention in response.mentions:
            brand_counter[mention.brand] += 1

    # ajuda da IA para montar o formato bonitinho
    lines = [
        "",
        "==============================",
        "      INGESTION REPORT",
        "==============================",
        "",
        f"Recebidos:   {ingestion.total_received}",
        f"Processados: {ingestion.total_processed}",
        f"Duplicados:  {ingestion.total_duplicates}",
        f"Rejeitados:  {ingestion.total_rejected}",
        "",
        "------------------------------",
        "       MENTION REPORT",
        "------------------------------",
        "",
        f"Total de menções: {total_mentions}",
        "",
        "Menções por marca:",
    ]

    for brand, count in brand_counter.items():
        lines.append(
            f"  - {brand}: {count}"
        )

    lines.extend([
        "",
        "------------------------------",
        "        DETALHAMENTO",
        "------------------------------",
        "",
    ])

    for item in analyzed:
        response = item.response
        lines.append(
            f"[{response.id}] "
            f"{response.plataforma}"
        )

        if item.mentions:
            for mention in item.mentions:
                lines.append(
                    f"    → {mention.brand} "
                    f"({mention.matched_text})"
                )

        else:
            lines.append( "    → nenhuma marca encontrada")

        lines.append("")
    return "\n".join(lines)