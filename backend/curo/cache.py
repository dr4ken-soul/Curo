"""SQLite cache for completed FortyGuard requests and demo sites."""

import hashlib
import json
import sqlite3
import time
from pathlib import Path
from typing import Any


class CacheStore:
    """Persist API responses forever during the hackathon."""

    def __init__(self, database_path: str) -> None:
        """Create the store and initialise its tables."""

        self.database_path = database_path
        Path(database_path).parent.mkdir(parents=True, exist_ok=True)
        self._initialise()

    def _connection(self) -> sqlite3.Connection:
        """Open a connection configured for row access."""

        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        return connection

    def _initialise(self) -> None:
        """Create the cache and site tables if needed."""

        with self._connection() as connection:
            connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS api_cache (
                    key TEXT PRIMARY KEY,
                    payload TEXT NOT NULL,
                    fetched_at INTEGER NOT NULL
                );
                CREATE TABLE IF NOT EXISTS sites (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    lat REAL NOT NULL,
                    lon REAL NOT NULL,
                    thickness REAL NOT NULL DEFAULT 8,
                    mass INTEGER NOT NULL DEFAULT 0,
                    pour_cost REAL NOT NULL DEFAULT 12000,
                    re_pour_co2 REAL NOT NULL DEFAULT 0.9
                );
                """
            )
            connection.execute(
                """
                INSERT OR IGNORE INTO sites
                (id, name, lat, lon, thickness, mass, pour_cost, re_pour_co2)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                ("site-01", "downtown Phoenix", 33.4484, -112.0740, 8.0, 0, 12000.0, 0.9),
            )

    @staticmethod
    def key_for(namespace: str, payload: dict[str, Any]) -> str:
        """Return a stable cache key for a request namespace and payload."""

        serialised = json.dumps(payload, sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(f"{namespace}:{serialised}".encode("utf-8")).hexdigest()

    def get(self, key: str) -> tuple[dict[str, Any], int] | None:
        """Return a cached JSON payload and its fetch timestamp."""

        with self._connection() as connection:
            row = connection.execute("SELECT payload, fetched_at FROM api_cache WHERE key = ?", (key,)).fetchone()
        if row is None:
            return None
        return json.loads(row["payload"]), int(row["fetched_at"])

    def set(self, key: str, payload: dict[str, Any], fetched_at: int | None = None) -> None:
        """Store a JSON payload under a stable key."""

        timestamp = fetched_at or int(time.time())
        with self._connection() as connection:
            connection.execute(
                "INSERT OR REPLACE INTO api_cache (key, payload, fetched_at) VALUES (?, ?, ?)",
                (key, json.dumps(payload), timestamp),
            )

    def newest(self) -> tuple[dict[str, Any], int] | None:
        """Return the newest cached provider payload."""

        with self._connection() as connection:
            row = connection.execute("SELECT payload, fetched_at FROM api_cache ORDER BY fetched_at DESC LIMIT 1").fetchone()
        if row is None:
            return None
        return json.loads(row["payload"]), int(row["fetched_at"])

    def list_sites(self) -> list[dict[str, Any]]:
        """Return all configured sites as dictionaries."""

        with self._connection() as connection:
            rows = connection.execute("SELECT * FROM sites ORDER BY id").fetchall()
        return [dict(row) for row in rows]

    def get_site(self, site_id: str) -> dict[str, Any] | None:
        """Return one configured site or None."""

        with self._connection() as connection:
            row = connection.execute("SELECT * FROM sites WHERE id = ?", (site_id,)).fetchone()
        return None if row is None else dict(row)

    def upsert_site(self, site: dict[str, Any]) -> dict[str, Any]:
        """Insert or update a configured site."""

        with self._connection() as connection:
            connection.execute(
                """
                INSERT OR REPLACE INTO sites
                (id, name, lat, lon, thickness, mass, pour_cost, re_pour_co2)
                VALUES (:id, :name, :lat, :lon, :thickness, :mass, :pour_cost, :re_pour_co2)
                """,
                site,
            )
        return site
