# chroma_store.py
from config.config import CHROMA_DB_PATH, OPENAI_API_KEY, OPENAI_EMBED_MODEL_NAME

from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

import shutil
import os


def create_vectorstore():
    embeddings = OpenAIEmbeddings(model=OPENAI_EMBED_MODEL_NAME, openai_api_key=OPENAI_API_KEY)
    return Chroma(persist_directory=CHROMA_DB_PATH, embedding_function=embeddings)


def create_vectorstore(user_id=None) -> Chroma:
    persist_directory = f"{CHROMA_DB_PATH}/{user_id}" if user_id else "{CHROMA_DB_PATH}/default"
    embeddings = OpenAIEmbeddings(model=OPENAI_EMBED_MODEL_NAME, openai_api_key=OPENAI_API_KEY)
    vs = Chroma(persist_directory=persist_directory, embedding_function=embeddings)
    return vs


def recreate_vectorstore(username=None) -> Chroma:
    persist_directory = f"{CHROMA_DB_PATH}/{username}" if username else "{CHROMA_DB_PATH}/default"
    if os.path.exists(persist_directory):
        print(f"Deleting existing Chroma DB at {persist_directory}")
        shutil.rmtree(persist_directory)
    os.makedirs(persist_directory, exist_ok=True)
    return create_vectorstore(username)
