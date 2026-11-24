
"""Modul zapisu i odczytu historii predykcji w bazie PostgreSQL."""

import json
import os

import psycopg2
import psycopg2.extras

SQL_UTWORZ_TABELE = """
CREATE TABLE IF NOT EXISTS predykcje (
    id SERIAL PRIMARY KEY,
    utworzono TIMESTAMPTZ NOT NULL DEFAULT now(),
    cechy JSONB NOT NULL,
    wynik INTEGER NOT NULL
);
"""

def pobierz_dsn() -> str | None:
    return os.getenv("DATABASE_URL")

def inicjalizuj_baze(dsn: str) -> None:
    polaczenie = psycopg2.connect(dsn)
    try:
        with polaczenie, polaczenie.cursor() as kursor:
            kursor.execute(SQL_UTWORZ_TABELE)
    finally:
        polaczenie.close()

def zapisz_predykcje(
    dsn: str, cechy: list[float], wynik: int
) -> None:
    polaczenie = psycopg2.connect(dsn)
    try:
        with polaczenie, polaczenie.cursor() as kursor:
            kursor.execute(
                "INSERT INTO predykcje (cechy, wynik) VALUES (%s, %s)",
                (json.dumps(cechy), wynik),
            )
    finally:
        polaczenie.close()

def pobierz_historie(dsn: str, limit: int = 10) -> list[dict]:
    polaczenie = psycopg2.connect(dsn)
    try:
        with polaczenie, polaczenie.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor
        ) as kursor:
            kursor.execute(
                "SELECT id, utworzono, cechy, wynik "
                "FROM predykcje ORDER BY id DESC LIMIT %s",
                (limit,),
            )
            rekordy = kursor.fetchall()
    finally:
        polaczenie.close()

    for rekord in rekordy:
        rekord["utworzono"] = rekord["utworzono"].isoformat()

    return rekordy