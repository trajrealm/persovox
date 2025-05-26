# rag_engine/resume_generator.py

from src.rag_engine.utils.file_saver import save_docx
from src.rag_engine.utils.formatting import style_resume_for_display
from src.rag_engine.job_scraper import extract_job_description  # Assuming you have this
from src.rag_engine.rag_engine import generate_resume_coverletter

def generate_resume(job_link: str):
    job_description = extract_job_description(job_link)

    resume_raw_text = generate_resume_coverletter(job_description)  # existing method
    styled_resume = style_resume_for_display(resume_raw_text)
    docx_path = save_docx(resume_raw_text, filename="generated_resume.docx")

    return styled_resume, docx_path
