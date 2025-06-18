# config.py
import os
from dotenv import load_dotenv

# Load environment variables from .env at the project root
load_dotenv()


# Set OpenAI Key via env
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH")
RESUME_DIR = os.getenv("RESUME_DIR")
# EMBEDDING_MODEL = "openai"  # or "local"
# OPENAI_EMBED_MODEL_NAME = "text-embedding-3-small"
# OPENAI_MODEL = "gpt-4o-mini"  # or "gpt-4o-mini"
