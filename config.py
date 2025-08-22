from dotenv import load_dotenv
import os
from datetime import timedelta

load_dotenv()

# .env
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
LLM_MODEL = os.getenv("LLM_MODEL")
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "2048"))

# rate limiting
MAX_EXTENSION_REQUESTS = 4     # per extension per window
MAX_GLOBAL_REQUESTS = 64     # total across all extensions per window
WINDOW = timedelta(minutes=2)

# logging
LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "server.log")
LOG_LEVEL = "DEBUG"
LOG_MAX_BYTES = 5_000_000  # 5 MB
LOG_BACKUP_COUNT = 3