# llm.py
import os
import requests
from typing import Dict, List

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://127.0.0.1:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:1b")

SYSTEM_PROMPT = """
Eres un asistente de recordatorios.

REGLAS DE SALIDA (OBLIGATORIO):
- Si el usuario quiere AGREGAR un recordatorio, responde EXACTAMENTE en una sola línea:
TOOL:add_recordatorio|texto=...|fecha=...

- Si el usuario quiere LISTAR recordatorios, responde EXACTAMENTE:
TOOL:list_recordatorios

- Si falta información (por ejemplo fecha), pregunta SOLO lo mínimo.
- No inventes fechas.
- No agregues texto extra si vas a usar TOOL:...
""".strip()


def call_llm(messages: List[Dict[str, str]]) -> Dict:
    payload = {
        "model": OLLAMA_MODEL,
        "messages": messages,
        "stream": False,
        "options": {"temperature": 0.1},
    }
    r = requests.post(f"{OLLAMA_URL}/api/chat", json=payload, timeout=120)
    r.raise_for_status()
    data = r.json()
    content = (data.get("message") or {}).get("content") or ""
    return {"response": content}
