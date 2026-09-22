

def normalize_platform(platform: str) -> str:
    normalized = platform.strip().lower()

    PLATFORM_ALIASES = {
        # Variações do ChatGPT
        "chatgpt": "ChatGPT",
        "chat-gpt": "ChatGPT",
        "chat gpt": "ChatGPT",
        "CHATGPT": "ChatGPT",

        # Variações do Gemini
        "gemini": "Gemini",
        "GEMINI": "Gemini",

        # Variações do Perplexity
        "perplexity": "Perplexity",
        "PERPLEXITY": "Perplexity",
    }

    return PLATFORM_ALIASES.get(normalized, platform.strip())