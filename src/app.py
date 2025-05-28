# app.py
import gradio as gr
from src.rag_engine.job_scraper import extract_job_description
from src.rag_engine.rag_engine import generate_resume_coverletter
from src.rag_engine.output_writer import write_output
from src.rag_engine.resume_processor import index_resumes
from src.rag_engine.utils.file_saver import save_docx
import gradio as gr
from src.rag_engine.resume_generator import generate_resume
from src.rag_engine.utils.formatting import style_resume_for_display
from src.rag_engine.utils.user_utils import get_available_users

import os

# Initial indexing
users = get_available_users()

def generate_resume(job_url, user_id, output_format="docx"):
    try:
        jd = extract_job_description(job_url)
        resume, cover = generate_resume_coverletter(jd, user_id=user_id)

        styled_resume = style_resume_for_display(resume)
        docx_path = save_docx(resume, filename=f"{user_id}_generated_resume.docx")

        return styled_resume, docx_path
    except Exception as e:
        return f"Error: {str(e)}", None

def process_and_generate_resume(user_id, job_link):
    index_resumes(user_id)  # dynamically index based on user
    resume_text, file_path = generate_resume(job_link, user_id=user_id)  # pass user
    return resume_text, file_path


with gr.Blocks() as demo:
    gr.Markdown("# 🤖 PersoVox: AI-Tailored Resume Generator")

    with gr.Row():
        user_dropdown = gr.Dropdown(choices=users, label="Select User")
        job_link_input = gr.Textbox(label="Paste Job Link", placeholder="https://example.com/job-posting")
        generate_btn = gr.Button("Generate Resume")

    resume_preview = gr.Markdown(label="Preview Resume")
    resume_file_output = gr.File(label="Download.docx")

    generate_btn.click(
        fn=process_and_generate_resume,
        inputs=[user_dropdown, job_link_input],
        outputs=[resume_preview, resume_file_output]
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
