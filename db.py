import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "recordatorios.db")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    cur = conn.cursor()

    # Crear tabla base si no existe
    cur.execute("""
        CREATE TABLE IF NOT EXISTS recordatorios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            texto TEXT NOT NULL,
            fecha_creacion TEXT NOT NULL,
            fecha_objetivo TEXT
        )
    """)

    # --- MIGRACIONES SEGURAS ---
    cur.execute("PRAGMA table_info(recordatorios)")
    columnas = [row["name"] for row in cur.fetchall()]

    if "completado" not in columnas:
        cur.execute("ALTER TABLE recordatorios ADD COLUMN completado INTEGER DEFAULT 0")

    conn.commit()
    conn.close()
