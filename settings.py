import os

# -------- load secrets from .env (never commit .env!) ----------
_ENV_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
if os.path.exists(_ENV_FILE):
    with open(_ENV_FILE, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))

# -------- window / colours ----------
WIDTH, HEIGHT = 960, 540
FPS = 60
FONT_PATH = None          # use Pygame default font
FONT_SIZE = 25
BG_COLOR   = (30, 30, 40)
TEXT_COLOR = (0, 0, 0)

# -------- Azure Speech (STT & TTS) ---
AZURE_SPEECH_KEY    = os.getenv("AZURE_SPEECH_KEY", "")
AZURE_SPEECH_REGION = os.getenv("AZURE_SPEECH_REGION", "westeurope")
TTS_VOICE = "en-US-AvaNeural"

# -------- Azure OpenAI ---------------
AZURE_OPENAI_KEY        = os.getenv("AZURE_OPENAI_KEY", "")
AZURE_OPENAI_ENDPOINT   = os.getenv("AZURE_OPENAI_ENDPOINT", "")
AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT", "chat")
AZURE_OPENAI_API_VER    = "2024-02-15-preview"

# -------- feature flags --------------
USE_TTS      = True
USE_STT      = True
USE_ENV_PRED = True

LOCAL_ENV_JSON = "StreamingAssets/EnvPredictions/today.env.json"

# -------- Copernicus API (Sentinel-5P) --------
#  Vilnius example; replace with your city
CDSE_USER = os.getenv("CDSE_USER", "")
CDSE_PASS = os.getenv("CDSE_PASS", "")
CDSE_BBOX = (25.1, 54.6, 25.4, 54.8)
SENTINEL_CLIENT_ID     = os.getenv("SENTINEL_CLIENT_ID", "")
SENTINEL_CLIENT_SECRET = os.getenv("SENTINEL_CLIENT_SECRET", "")
SENTINEL_INSTANCE_ID   = os.getenv("SENTINEL_INSTANCE_ID", "")
SENTINEL_AOI_BBOX      = (25.1, 54.6, 25.4, 54.8)  # Example: Vilnius

# Layer IDs exactly as shown in the dashboard
LAYER_IDS = {
    "NO2":   "NO2",                       # or NITROGEN-DIOXIDE etc.
    "O3":    "O3",
    "CO":    "CO",
    "AI340": "AER_AI_340_380"
}
