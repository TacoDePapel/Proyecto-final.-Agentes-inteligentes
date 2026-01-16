from datetime import datetime
from typing import Optional
from db import get_db


def agregar_recordatorio(texto: str, fecha_objetivo: Optional[str] = None):
    conn = get_db()
    cur = conn.cursor()

    fecha_creacion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # evitar duplicados exactos
    cur.execute(
        "SELECT id FROM recordatorios WHERE texto=? AND fecha_objetivo IS ?",
        (texto, fecha_objetivo)
    )
    if cur.fetchone():
        conn.close()
        return

    cur.execute(
        "INSERT INTO recordatorios (texto, fecha_creacion, fecha_objetivo) VALUES (?, ?, ?)",
        (texto, fecha_creacion, fecha_objetivo)
    )

    conn.commit()
    conn.close()


def marcar_completado(texto: str):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("UPDATE recordatorios SET completado=1 WHERE texto=?", (texto,))
    conn.commit()
    conn.close()


def listar_recordatorios():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT texto, fecha_creacion, fecha_objetivo, completado
        FROM recordatorios
        ORDER BY id DESC
    """)
    filas = cur.fetchall()
    conn.close()

    ahora = datetime.now()
    tareas = []

    for r in filas:
        vencido = False
        if r["fecha_objetivo"]:
            try:
                dt = datetime.strptime(r["fecha_objetivo"], "%Y-%m-%d %H:%M:%S")
                vencido = dt < ahora and not r["completado"]
            except Exception:
                pass

        tareas.append({
            "tarea": r["texto"],
            "fecha_creacion": r["fecha_creacion"],
            "fecha_objetivo": r["fecha_objetivo"],
            "completado": bool(r["completado"]),
            "vencido": vencido
        })

    return tareas
