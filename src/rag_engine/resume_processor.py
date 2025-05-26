# resume_processor.py
import os
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from src.rag_engine.chroma_store import get_vectorstore

def load_resumes(resume_dir):
    documents = []
    for file in os.listdir(resume_dir):
        if file.endswith(".pdf"):
            loader = PyPDFLoader(os.path.join(resume_dir, file))
            docs = loader.load()
            documents.extend(docs)
    return documents

def index_resumes():
    documents = load_resumes("data/resumes")
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, 
                                            chunk_overlap=200,
                                            separators=["\n\n", "\n", ".", ",", " "],
                                              )
    docs = splitter.split_documents(documents)
    db = get_vectorstore()
    db.add_documents(docs)
