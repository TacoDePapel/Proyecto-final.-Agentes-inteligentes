from typing import Optional, Dict, Any
from recordatorios import agregar_recordatorio, listar_recordatorios, marcar_completado


def tool_add_recordatorio(texto: str, fecha: Optional[str] = None) -> Dict[str, Any]:
    agregar_recordatorio(texto, fecha)
    if fecha:
        return {"mensaje": f"Recordatorio guardado: {texto} (para: {fecha})"}
    return {"mensaje": f"Recordatorio guardado: {texto}"}


def tool_list_recordatorios() -> Dict[str, Any]:
    return {"tareas": listar_recordatorios()}


def tool_completar_recordatorio(texto: str) -> Dict[str, Any]:
    marcar_completado(texto)
    return {"mensaje": f"Marcado como completado: {texto}"}
