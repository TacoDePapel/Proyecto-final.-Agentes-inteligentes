from db import get_db

def limpiar_duplicados():
    conn = get_db()
    cur = conn.cursor()

    # Borra duplicados, deja el más reciente
    cur.execute("""
        DELETE FROM recordatorios
        WHERE id NOT IN (
            SELECT MAX(id)
            FROM recordatorios
            GROUP BY texto, fecha_objetivo
        )
    """)

    conn.commit()
    conn.close()
