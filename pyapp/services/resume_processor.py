# resume_processor.py
from pyapp.db.chroma_store import create_vectorstore, recreate_vectorstore
from pyapp.services.resume_parser import batch_parse_resumes
from pyapp.services.resume_merger import create_merged_json
from config.config import SUPABASE_URL, SUPABASE_KEY, BUCKET_NAME, LOCAL_DWNLD_DIR, RESUME_DIR

import ast
import os
import glob
import json
import sys
from langchain_community.document_loaders import PyMuPDFLoader, DirectoryLoader
from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter
from supabase import create_client, Client


def load_merged_resume(user_id: str) -> list[Document]:
    merged_path = f"data/{user_id}/resumes/parsed/merged.json"
    if not os.path.exists(merged_path):
        raise FileNotFoundError(f"Merged JSON not found for user {user_id}")

    with open(merged_path, "r") as f:
        resume_data = json.load(f)

    # Turn structured JSON into plain text for RAG
    text_blocks = []

    personal_info = resume_data.get("personal_info", {})
    contact_block = f"""Contact Information:
    Name: {personal_info.get("name", "")}
    Email: {personal_info.get("email", "")}
    Phone: {personal_info.get("phone", "")}
    Location: {personal_info.get("location", "")}
    LinkedIn: {personal_info.get("linkedin", "")}
    """
    text_blocks.append(contact_block)

    if resume_data.get("summary"):
        text_blocks.append(f"Summary: {resume_data['summary']}")

    for exp in resume_data.get("experiences", []):
        block = f"""Experience:
- Job Title: {exp.get('job_title')}
- Company: {exp.get('company')}
- Location: {exp.get('location')}
- Duration: {exp.get('start_date')} to {exp.get('end_date')}
- Description: {'; '.join(exp.get('description', []))}
"""
        text_blocks.append(block)

    for edu in resume_data.get("education", []):
        block = f"""Education:
- Degree: {edu.get('degree')}
- University: {edu.get('university')}
- Location: {edu.get('location')}
- Graduation Year: {edu.get('graduation_year')}
"""
        text_blocks.append(block)

    skills = resume_data.get("skills", [])
    if skills:
        text_blocks.append(f"Skills: {', '.join(skills)}")

    certs = resume_data.get("certifications", [])
    if certs:
        cert_block = "\n".join([f"- {c['name']} ({c.get('issuer', '')})" for c in certs])
        text_blocks.append(f"Certifications:\n{cert_block}")

    combined_text = "\n\n".join(text_blocks)

    return [Document(page_content=combined_text, metadata={"user_id": user_id})]


def index_user_json_resume(user_id: str, reindex=False):
    docs = load_merged_resume(user_id)

    splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_documents(docs)
    db = create_vectorstore(user_id=user_id) if not reindex else recreate_vectorstore(username=user_id)

    db.add_documents(chunks)


def load_resumes(user_id, base_dir="data"):
    user_resume_path = os.path.join(base_dir, user_id, "resumes")
    if not os.path.exists(user_resume_path):
        raise ValueError(f"Resume directory not found: {user_resume_path}")
    
    pdf_files = glob.glob(user_resume_path+"/*", recursive=True)
    documents = []
    for pdf_file in pdf_files:
        loader = PyMuPDFLoader(pdf_file)
        docs = loader.load()
        for doc in docs:
            doc.metadata["doc_type"] = "resume"
            doc.metadata["user_id"] = user_id
            documents.append(doc)
    return documents

def index_resumes(user_id):
    documents = load_resumes(user_id)
    splitter = RecursiveCharacterTextSplitter(chunk_size=1200, chunk_overlap=200, separators=["\n\n", "\n", " ", "", "."])
    docs = splitter.split_documents(documents)
    db = create_vectorstore()
    db.add_documents(docs)


def download_resumes(username: str, files: str):
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    print(f"files are: {files}, {type(files)}")
    file_list = ast.literal_eval(files)
    user_dir = f"{LOCAL_DWNLD_DIR}/{username}/{RESUME_DIR}" 
    
    if not os.path.exists(user_dir):
        os.makedirs(user_dir, exist_ok=True)

    for filename in file_list:
        file_path = f"{RESUME_DIR}/{username}/{filename}"
        print(f"Downloading file: {file_path}")
        with open(f"{LOCAL_DWNLD_DIR}/{username}/{RESUME_DIR}/{filename}", "wb+") as f:
            response = supabase.storage.from_(BUCKET_NAME).download(file_path)
            f.write(response)


def regenerate_kb(username: str, files: list):
    print(f"Regenerating knowledge base for user: {username} and files: {files}")
    download_resumes(username, files)
    batch_parse_resumes(f"{LOCAL_DWNLD_DIR}/{username}/{RESUME_DIR}", f"{LOCAL_DWNLD_DIR}/{username}/{RESUME_DIR}/parsed", files)
    create_merged_json(username, files)
    index_user_json_resume(username, reindex=True)



import sys
if __name__ == "__main__":
    username = sys.argv[1]
    files = sys.argv[2]
    print("I am files_json ===> :", files)
    regenerate_kb(username, files)
    print("✅ Regeneration completed.")
