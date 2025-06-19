# config.py
import os
from dotenv import load_dotenv

# Load environment variables from .env at the project root
load_dotenv()


# Set OpenAI Key via env
OPENAI_API_KEY          = os.getenv("OPENAI_API_KEY")
CHROMA_DB_PATH          = os.getenv("CHROMA_DB_PATH")
RESUME_DIR              = os.getenv("RESUME_DIR")
OPENAI_EMBED_MODEL_NAME = os.getenv("OPENAI_EMBED_MODEL_NAME")
OPENAI_MODEL            = os.getenv("OPENAI_MODEL")
DATABASE_URL            = os.getenv("DATABASE_URL")
SUPABASE_URL            = os.getenv("SUPABASE_URL")
SUPABASE_KEY            = os.getenv("SUPABASE_KEY")
BUCKET_NAME             = os.getenv("BUCKET_NAME")
LOCAL_DWNLD_DIR         = os.getenv("LOCAL_DWNLD_DIR")