import json
import sqlite3


def init_database(db_path: str) -> None:

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cached_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            endpoint TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            parametros TEXT NOT NULL,
            resultado TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_endpoint_timestamp
        ON cached_results(endpoint, timestamp DESC)
    """)

    conn.commit()
    conn.close()

def save(
    db_path: str,
    endpoint: str,
    timestamp: str,
    parametros: dict,
    resultado: dict,
) -> None:

    conn = sqlite3.connect(db_path)

    conn.execute("""
        INSERT INTO cached_results
        (endpoint, timestamp, parametros, resultado)
        VALUES (?, ?, ?, ?)
    """, (
        endpoint,
        timestamp,
        json.dumps(parametros, ensure_ascii=False),
        json.dumps(resultado, ensure_ascii=False),
    ))

    conn.commit()
    conn.close()

def load_latest(
    db_path: str,
    endpoint: str,
) -> dict | None:

    conn = sqlite3.connect(db_path)

    cursor = conn.execute("""
        SELECT endpoint, timestamp, parametros, resultado
        FROM cached_results
        WHERE endpoint = ?
        ORDER BY timestamp DESC
        LIMIT 1
    """, (endpoint,))

    row = cursor.fetchone()

    conn.close()

    if not row:
        return None

    return {
        "endpoint": row[0],
        "timestamp": row[1],
        "parametros": json.loads(row[2]),
        "resultado": json.loads(row[3]),
    }

def load_history(
    db_path: str,
    endpoint: str,
    limit: int = 10,
) -> list[dict]:

    conn = sqlite3.connect(db_path)

    cursor = conn.execute("""
        SELECT endpoint, timestamp, parametros, resultado
        FROM cached_results
        WHERE endpoint = ?
        ORDER BY timestamp DESC
        LIMIT ?
    """, (endpoint, limit))

    rows = cursor.fetchall()

    conn.close()

    return [
        {
            "endpoint": row[0],
            "timestamp": row[1],
            "parametros": json.loads(row[2]),
            "resultado": json.loads(row[3]),
        }
        for row in rows
    ]


def clear(
    db_path: str,
    endpoint: str | None = None,
) -> None:

    conn = sqlite3.connect(db_path)

    if endpoint:
        conn.execute(
            "DELETE FROM cached_results WHERE endpoint = ?",
            (endpoint,),
        )
    else:
        conn.execute("DELETE FROM cached_results")

    conn.commit()
    conn.close()

def get_stats(db_path: str) -> dict:

    conn = sqlite3.connect(db_path)

    cursor = conn.execute("""
        SELECT endpoint, COUNT(*) as count
        FROM cached_results
        GROUP BY endpoint
        ORDER BY count DESC
    """)

    stats = {
        row[0]: row[1]
        for row in cursor.fetchall()
    }

    conn.close()

    return stats

























