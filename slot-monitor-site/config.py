import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "change-me")
    API_TOKEN = os.environ.get("API_TOKEN", "your-api-token")
    DATABASE_URI = os.path.join(os.path.dirname(__file__), "db.sqlite")
    LOG_FILE = os.path.join(os.path.dirname(__file__), "slot_jackpot_log.txt")
    REBATE_PERCENTAGE = float(os.environ.get("REBATE_PERCENTAGE", 0.01))
    BRAND_NAME = os.environ.get("BRAND_NAME", "PALACE CASINO")
    DEFAULT_LANGUAGE = os.environ.get("DEFAULT_LANGUAGE", "en")
