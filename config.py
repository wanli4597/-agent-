import os

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:7b")
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "180"))
OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY", "")

APP_NAME = "Nova AI Assistant"
APP_LEVEL = "Nova Final Edition"

MEMORY_CHAR_LIMIT = 2500
MAX_FILENAME_LENGTH = 50
MAX_SUBTASKS = 6