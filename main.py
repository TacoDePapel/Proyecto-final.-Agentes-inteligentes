from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import re
import dateparser
from datetime import datetime, timedelta

from db import init_db
from recordatorios import listar_recordatorios
from tools import tool_add_recordatorio, tool_completar_recordatorio
from notificador import iniciar

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


class Mensaje(BaseModel):
    mensaje: str


@app.on_event("startup")
def startup():
    init_db()
    iniciar()


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/recordatorios/pendientes")
def pendientes():
    return {"tareas": listar_recordatorios()}


def limpiar_prefijo(texto: str) -> str:
    return re.sub(
        r"^(recuérdame|recuerdame|recordarme)\s*",
        "",
        texto,
        flags=re.IGNORECASE
    ).strip()


def detectar_tiempo_relativo(texto: str):
    """
    Detecta frases tipo:
    - en 5 segundos
    - en 1 minuto
    - en 10 minutos
    """
    m = re.search(r"en\s+(\d+)\s*(segundo|segundos|minuto|minutos)", texto)
    if not m:
        return None

    cantidad = int(m.group(1))
    unidad = m.group(2)

    ahora = datetime.now()
    if "segundo" in unidad:
        return ahora + timedelta(seconds=cantidad)
    if "minuto" in unidad:
        return ahora + timedelta(minutes=cantidad)

    return None


def separar_texto(texto: str):
    patrones = [
        r"en\s+\d+\s*(segundos|minutos)",
        r"hoy.*", r"mañana.*", r"pasado mañana.*",
        r"el lunes.*", r"el martes.*", r"el miércoles.*",
        r"el jueves.*", r"el viernes.*",
        r"\d{1,2}:\d{2}", r"\d{1,2}\s*(am|pm)"
    ]
    for p in patrones:
        m = re.search(p, texto.lower())
        if m:
            return texto[:m.start()].strip(), m.group().strip()
    return texto, None


@app.post("/asistente")
def asistente(data: Mensaje):
    texto = data.mensaje.strip()

    # marcar completado
    if texto.lower().startswith("completado"):
        tarea = texto.replace("completado", "").strip()
        return tool_completar_recordatorio(tarea)

    if texto.lower().startswith(("recuérdame", "recuerdame", "recordarme")):
        contenido = limpiar_prefijo(texto)
        texto_limpio, tiempo_txt = separar_texto(contenido)

        fecha_objetivo = None

        # 🔥 PRIORIDAD: tiempo relativo
        dt_relativo = detectar_tiempo_relativo(contenido)
        if dt_relativo:
            fecha_objetivo = dt_relativo.strftime("%Y-%m-%d %H:%M:%S")
        elif tiempo_txt:
            dt = dateparser.parse(
                tiempo_txt,
                languages=["es"],
                settings={"PREFER_DATES_FROM": "future"}
            )
            if dt:
                fecha_objetivo = dt.strftime("%Y-%m-%d %H:%M:%S")

        return tool_add_recordatorio(texto_limpio, fecha_objetivo)

    return {"mensaje": "Usa: Recuérdame ... o Completado ..."}
