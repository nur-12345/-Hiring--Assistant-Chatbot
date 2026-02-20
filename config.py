import os
from dotenv import load_dotenv

load_dotenv()

GROK_API_KEY = os.getenv("GROK_API_KEY")

EXIT_KEYWORDS = ["exit", "quit", "bye", "goodbye", "end"]
