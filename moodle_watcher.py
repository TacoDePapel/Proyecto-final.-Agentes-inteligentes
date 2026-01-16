from datetime import datetime
from recordatorios import agregar_recordatorio
from plyer import notification

# Simulación de tareas detectadas en Moodle
# (en real, aquí iría API / scraping)
TAREAS_MOODLE = [
    {
        "curso": "Agentes Inteligentes",
        "tarea": "Entrega práctica 3",
        "fecha": "2026-01-16 23:59:00"
    },
    {
        "curso": "Inglés",
        "tarea": "Essay Unit 2",
        "fecha": "2026-01-17 20:00:00"
    }
]

_vistas = set()


def revisar_moodle():
    for t in TAREAS_MOODLE:
        clave = f"{t['curso']}|{t['tarea']}"
        if clave in _vistas:
            continue

        agregar_recordatorio(
            texto=f"{t['curso']}: {t['tarea']}",
            fecha_objetivo=t["fecha"]
        )

        notification.notify(
            title="📘 Nueva tarea en Moodle",
            message=f"{t['curso']} — {t['tarea']}",
            timeout=10
        )

        _vistas.add(clave)
