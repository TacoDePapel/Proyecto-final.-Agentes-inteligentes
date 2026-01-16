from datetime import datetime
from plyer import notification
from recordatorios import listar_recordatorios

_ultimo_minuto = None

def enviar_resumen():
    global _ultimo_minuto

    ahora = datetime.now()
    minuto_actual = ahora.strftime("%Y-%m-%d %H:%M")

    # evita spam: 1 resumen por minuto
    if _ultimo_minuto == minuto_actual:
        return
    _ultimo_minuto = minuto_actual

    tareas = listar_recordatorios()
    pendientes = [t for t in tareas if not t.get("completado")]
    vencidos = [t for t in pendientes if t.get("vencido")]

    # vence hoy
    hoy = ahora.strftime("%Y-%m-%d")
    vence_hoy = []
    for t in pendientes:
        fo = t.get("fecha_objetivo")
        if fo and fo.startswith(hoy):
            vence_hoy.append(t)

    msg = f"Pendientes: {len(pendientes)} | Vencidos: {len(vencidos)} | Vence hoy: {len(vence_hoy)}"

    notification.notify(
        title="📌 Resumen del agente",
        message=msg,
        timeout=8
    )
