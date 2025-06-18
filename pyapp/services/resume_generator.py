# rag_engine/resume_generator.py

from pyapp.utils.file_saver import save_docx
from pyapp.utils.formatting import style_resume_for_display
from pyapp.services.job_scraper import extract_job_description  # Assuming you have this
from pyapp.services.rag_engine import generate_resume_coverletter

def generate_resume(job_link: str):
    job_description = extract_job_description(job_link)

    resume_raw_text, cover_raw_text = generate_resume_coverletter(job_description)  # existing method
    styled_resume = style_resume_for_display(resume_raw_text)
    docx_path = save_docx(resume_raw_text, filename="generated_resume.docx")
    docx_cover_path = save_docx(cover_raw_text, filename="generated_coverletter.docx")  

    return styled_resume, docx_path
