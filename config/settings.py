import os
from google.genai import types
# ==========================================
# Environment & retry config
# ==========================================

DEFAULT_GOOGLE_API_KEY=""
os.environ["GOOGLE_API_KEY"] = os.environ.get("GOOGLE_API_KEY", DEFAULT_GOOGLE_API_KEY)

APP_NAME = "agents"
USER_ID = "cryptoUser"
SESSION_ID = "cryptoSession"
LLM = "gemini-2.5-flash-lite"

retry_config = types.HttpRetryOptions(
    attempts=5,
    exp_base=7,
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],
)