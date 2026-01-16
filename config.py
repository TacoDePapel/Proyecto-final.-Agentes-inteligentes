import os
from dotenv import load_dotenv

load_dotenv()

def env(name: str, default: str = "") -> str:
    return os.getenv(name, default).strip()

LLM_PROVIDER = env("LLM_PROVIDER", "ollama").lower()

OLLAMA_URL = env("OLLAMA_URL", "http://127.0.0.1:11434")
OLLAMA_MODEL = env("OLLAMA_MODEL", "llama3.1:8b")

OPENAI_API_KEY = env("OPENAI_API_KEY", "")
OPENAI_MODEL = env("OPENAI_MODEL", "gpt-4o-mini")

MOODLE_BASE_URL = env("MOODLE_BASE_URL", "")
MOODLE_TOKEN = env("MOODLE_TOKEN", "")

SERVER_HOST = env("SERVER_HOST", "0.0.0.0")
SERVER_PORT = int(env("SERVER_PORT", "8080"))
