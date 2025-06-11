# app.py
from src.services.job_scraper import extract_job_description
from src.services.rag_engine import generate_resume_coverletter
from src.services.output_writer import write_output
from src.services.resume_processor import index_resumes, index_user_json_resume
from src.utils.file_saver import save_docx
from src.services.resume_generator import generate_resume
from src.utils.formatting import style_resume_for_display
from src.utils.user_utils import get_available_users

import gradio as gr

import os

# Initial indexing
users = get_available_users()

def generate_resume(job_url, user_id, output_format="docx"):
    
    try:
        jd = extract_job_description(job_url)
        resume, cover = generate_resume_coverletter(jd, user_id=user_id)

        styled_resume = style_resume_for_display(resume)
        styled_cover = style_resume_for_display(cover)

        if output_format == "docx":
            resume_path = save_docx(resume, filename=f"{user_id}_generated_resume.docx")
            cover_path = save_docx(cover, filename=f"{user_id}_generated_cover_letter.docx")

        return styled_resume, styled_cover, resume_path, cover_path
    except Exception as e:
        return f"Error: {str(e)}", None

def process_and_generate_resume(user_id, job_link):
    index_user_json_resume(user_id)
    resume_text, cover_text, resume_file, cover_file = generate_resume(job_link, user_id=user_id)
    return resume_text, cover_text, resume_file, cover_file

# def process_and_generate_resume(user_id, job_link):
#     index_resumes(user_id)
#     resume_text, cover_text, resume_file, cover_file = generate_resume(job_link, user_id=user_id)
#     return resume_text, cover_text, resume_file, cover_file


with gr.Blocks() as demo:
    gr.Markdown("# 🤖 PersoVox: AI-Tailored Resume & Cover Letter Generator")

    with gr.Row():
        user_dropdown = gr.Dropdown(choices=users, label="Select User")
        job_link_input = gr.Textbox(label="Paste Job Link", placeholder="https://example.com/job-posting")
        generate_btn = gr.Button("Generate Resume & Cover Letter")

    with gr.Tab("Resume"):
        resume_preview = gr.Markdown(label="Preview Resume")
        resume_file_output = gr.File(label="Download Resume")

    with gr.Tab("Cover Letter"):
        cover_preview = gr.Markdown(label="Preview Cover Letter")
        cover_file_output = gr.File(label="Download Cover Letter")

    generate_btn.click(
        fn=process_and_generate_resume,
        inputs=[user_dropdown, job_link_input],
        outputs=[
            resume_preview,
            cover_preview,
            resume_file_output,
            cover_file_output
        ]
    )

    
if __name__ == "__main__":
    demo.launch()# iface = gr.Interface(
#     fn=generate,
#     inputs=[
#         gr.Textbox(label="Job Description URL"),
#         gr.Dropdown(["docx", "txt"], label="Output Format", value="docx")
#     ],
#     outputs="text",
#     title="Persovox",
#     description="Paste a job URL to generate a personalized resume & cover letter using your knowledge base.",
# )

if __name__ == "__main__":
    demo.launch()
