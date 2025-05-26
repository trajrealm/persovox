# chroma_store.py
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from config.config import CHROMA_DB_PATH, OPENAI_API_KEY, OPENAI_EMBED_MODEL_NAME

def get_vectorstore():
    embeddings = OpenAIEmbeddings(model=OPENAI_EMBED_MODEL_NAME, openai_api_key=OPENAI_API_KEY)
    return Chroma(persist_directory=CHROMA_DB_PATH, embedding_function=embeddings)
