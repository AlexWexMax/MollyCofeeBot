from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
BARISTA_PASSWORD = os.getenv("BARISTA_PASSWORD")

if not BOT_TOKEN or not BARISTA_PASSWORD:
    raise RuntimeError("Please set BOT_TOKEN and BARISTA_PASSWORD in .env")
