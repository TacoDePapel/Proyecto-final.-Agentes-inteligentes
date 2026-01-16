from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from plyer import notification
from recordatorios import listar_recordatorios
from moodle_watcher import revisar_moodle
from resumen import enviar_resumen
from limpieza import limpiar_duplicados

scheduler = BackgroundScheduler()
_notificados = set()


def revisar_recordatorios():
    ahora = datetime.now()
    tareas = listar_recordatorios()

    for t in tareas:
        if t.get("completado"):
            continue

        fecha = t.get("fecha_objetivo")
        if not fecha:
            continue

        try:
            dt = datetime.strptime(fecha, "%Y-%m-%d %H:%M:%S")
        except Exception:
            continue

        if abs((dt - ahora).total_seconds()) <= 30:
            clave = f"{t['tarea']}|{fecha}"
            if clave in _notificados:
                continue

            notification.notify(
                title="⏰ Recordatorio",
                message=t["tarea"],
                timeout=10
            )
            _notificados.add(clave)


def iniciar():
    scheduler.add_job(revisar_recordatorios, "interval", seconds=20)
    scheduler.add_job(revisar_moodle, "interval", minutes=1)
    scheduler.add_job(enviar_resumen, "interval", minutes=1)  # 🔥 resumen proactivo
    scheduler.add_job(limpiar_duplicados, "interval", minutes=5)  # 🧹 limpieza automática
    scheduler.start()
