# resume_processor.py
import os
import glob
from langchain.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter
from src.rag_engine.chroma_store import get_vectorstore

def load_resumes(user_id, base_dir="data"):
    user_resume_path = os.path.join(base_dir, user_id, "resumes")
    if not os.path.exists(user_resume_path):
        raise ValueError(f"Resume directory not found: {user_resume_path}")
    
    pdf_files = glob.glob(user_resume_path+"/*", recursive=True)
    documents = []
    for pdf_file in pdf_files:
        loader = PyPDFLoader(pdf_file)
        docs = loader.load()
        for doc in docs:
            doc.metadata["doc_type"] = "resume"
            doc.metadata["user_id"] = user_id
            documents.append(doc)
    return documents

def index_resumes(user_id):
    documents = load_resumes(user_id)
    splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs = splitter.split_documents(documents)
    db = get_vectorstore()
    db.add_documents(docs)
