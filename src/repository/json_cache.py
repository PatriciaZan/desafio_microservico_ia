import json
from pathlib import Path


def get_cache_path(cache_dir: Path, endpoint: str) -> Path:
    filename = endpoint.strip("/").replace("/", "-") + ".json"
    return cache_dir / filename


def get_history_path(cache_dir: Path, endpoint: str) -> Path:
    filename = endpoint.strip("/").replace("/", "-") + "-history.json"
    return cache_dir / filename


def save_cache(
    cache_dir: Path,
    endpoint: str,
    cache_data: dict,
) -> None:

    cache_path = get_cache_path(cache_dir, endpoint)

    with open(cache_path, "w", encoding="utf-8") as file:
        json.dump(
            cache_data,
            file,
            indent=2,
            ensure_ascii=False,
        )


def save_history(
    cache_dir: Path,
    endpoint: str,
    cache_data: dict,
) -> None:

    history_path = get_history_path(cache_dir, endpoint)

    history = load_history(cache_dir, endpoint)

    history.append(cache_data)

    with open(history_path, "w", encoding="utf-8") as file:
        json.dump(
            history,
            file,
            indent=2,
            ensure_ascii=False,
        )


def save(
    cache_dir: Path,
    endpoint: str,
    cache_data: dict,
) -> None:

    save_cache(
        cache_dir,
        endpoint,
        cache_data,
    )

    save_history(
        cache_dir,
        endpoint,
        cache_data,
    )


def load(
    cache_dir: Path,
    endpoint: str,
) -> dict | None:

    cache_path = get_cache_path(cache_dir, endpoint)

    if not cache_path.exists():
        return None

    try:
        with open(cache_path, "r", encoding="utf-8") as file:
            return json.load(file)

    except (json.JSONDecodeError, IOError):
        return None


def load_history(
    cache_dir: Path,
    endpoint: str,
) -> list[dict]:

    history_path = get_history_path(cache_dir, endpoint)

    if not history_path.exists():
        return []

    try:
        with open(history_path, "r", encoding="utf-8") as file:
            return json.load(file)

    except (json.JSONDecodeError, IOError):
        return []


def clear(
    cache_dir: Path,
    endpoint: str | None = None,
) -> None:

    if endpoint:
        cache_path = get_cache_path(cache_dir, endpoint)
        history_path = get_history_path(cache_dir, endpoint)

        if cache_path.exists():
            cache_path.unlink()

        if history_path.exists():
            history_path.unlink()

        return

    for cache_file in cache_dir.glob("*.json"):
        cache_file.unlink()