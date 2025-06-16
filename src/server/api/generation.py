from fastapi import APIRouter
from pydantic import BaseModel
from src.services.job_scraper import extract_job_description
from src.services.rag_engine import generate_resume_coverletter

router = APIRouter()

class GenRequest(BaseModel):
    user: str
    job_link: str = ''
    job_text: str = ''

@router.post("/generate")
def generate(req: GenRequest):
    jd = req.job_text or extract_job_description(req.job_link)
    resume, cover = generate_resume_coverletter(jd, user_id=req.user)
    resume = resume.replace("```", "")
    cover = cover.replace("```", "")
    return {"resume": resume, "cover_letter": cover}
