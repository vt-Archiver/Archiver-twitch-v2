import sqlite3
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def get_connection(db_path: Path) -> sqlite3.Connection:
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    return conn


def init_db_schema(db_path: Path):
    conn = get_connection(db_path)
    cur = conn.cursor()

    cur.execute(
        """
    CREATE TABLE IF NOT EXISTS vods (
        vod_id TEXT PRIMARY KEY,
        stream_id TEXT,
        channel_name TEXT,
        folder_name TEXT,
        vod_original_title TEXT,
        created_at TEXT
    );
    """
    )
    conn.commit()
    conn.close()


def insert_vod_record(
    db_path: Path,
    vod_id: str,
    stream_id: str,
    channel_name: str,
    folder_name: str,
    vod_original_title: str,
    created_at: str,
):
    conn = get_connection(db_path)
    cur = conn.cursor()

    init_db_schema(db_path)

    sql = """
    INSERT OR REPLACE INTO vods
    (vod_id, stream_id, channel_name, folder_name, vod_original_title, created_at)
    VALUES
    (?, ?, ?, ?, ?, ?);
    """
    params = (
        vod_id,
        stream_id,
        channel_name,
        folder_name,
        vod_original_title,
        created_at,
    )

    cur.execute(sql, params)
    conn.commit()
    conn.close()

    logger.info(f"VOD record inserted: {vod_id}")
