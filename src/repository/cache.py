import json
from datetime import datetime, UTC
from pathlib import Path

from src.repository import json_cache
from src.repository import sqlite_cache


DEFAULT_CACHE_DIR = "results"
DEFAULT_DB_PATH = "results/cache.db"


def initialize(
    cache_dir: str = DEFAULT_CACHE_DIR,
    db_path: str = DEFAULT_DB_PATH,
) -> None:

    cache_path = Path(cache_dir)
    cache_path.mkdir(exist_ok=True)
    sqlite_cache.init_database(db_path)


def save(
    endpoint: str,
    resultado: dict,
    parametros: dict | None = None,
    cache_dir: str = DEFAULT_CACHE_DIR,
    db_path: str = DEFAULT_DB_PATH,
) -> None:

    timestamp = datetime.now(UTC).isoformat()
    parametros = parametros or {}
    cache_data = {
        "endpoint": endpoint,
        "timestamp": timestamp,
        "parametros": parametros,
        "resultado": resultado,
    }

    json_cache.save(
        Path(cache_dir),
        endpoint,
        cache_data,
    )

    sqlite_cache.save(
        db_path,
        endpoint,
        timestamp,
        parametros,
        resultado,
    )

def load(
    endpoint: str,
    cache_dir: str = DEFAULT_CACHE_DIR,
    db_path: str = DEFAULT_DB_PATH,
) -> dict | None:

    result = json_cache.load(
        Path(cache_dir),
        endpoint,
    )

    if result is not None:
        return result

    return sqlite_cache.load_latest(
        db_path,
        endpoint,
    )

def load_history(
    endpoint: str,
    limit: int = 10,
    cache_dir: str = DEFAULT_CACHE_DIR,
    db_path: str = DEFAULT_DB_PATH,
) -> list[dict]:

    history = json_cache.load_history(
        Path(cache_dir),
        endpoint,
    )

    if history:
        return list(reversed(history))[:limit]

    return sqlite_cache.load_history(
        db_path,
        endpoint,
        limit,
    )

def clear(
    endpoint: str | None = None,
    cache_dir: str = DEFAULT_CACHE_DIR,
    db_path: str = DEFAULT_DB_PATH,
) -> None:

    json_cache.clear(
        Path(cache_dir),
        endpoint,
    )

    sqlite_cache.clear(
        db_path,
        endpoint,
    )

def get_stats(
    db_path: str = DEFAULT_DB_PATH,
) -> dict:

    return sqlite_cache.get_stats(db_path)