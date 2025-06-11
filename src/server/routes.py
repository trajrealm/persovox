from src.services.rag_engine import generate_resume_coverletter  # Connect this to your logic
from src.services.job_scraper import extract_job_description
from src.utils.user_utils import get_available_users
from src.db.chroma_store import create_vectorstore
from src.db.vectorstore_singleton import add_vectorstore, get_all_vectorstore_users

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from contextlib import asynccontextmanager



@asynccontextmanager
async def lifespan(app: FastAPI):
    users = get_available_users()
    print(f"Available users: {users}")
    for user in users:
        vs = create_vectorstore(user_id=user)
        add_vectorstore(user_id=user, vstore=vs)
    yield

app = FastAPI(lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


class GenRequest(BaseModel):
    user: str
    job_link: str = ''
    job_text: str = ''

@app.get("/users")
def get_users():
    users = get_all_vectorstore_users()
    return {"users": users}

@app.post("/generate")
def generate(req: GenRequest):
    # Your logic to extract JD and generate both
    jd = req.job_text or extract_job_description(req.job_link)
    resume, cover = generate_resume_coverletter(jd, user_id=req.user)
    resume = resume.replace("```", "")
    cover = cover.replace("```", "")
    return {"resume": resume, "cover_letter": cover}
