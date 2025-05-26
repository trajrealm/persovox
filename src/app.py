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

import os

# Initial indexing
index_resumes()

def generate_resume(job_url, output_format="docx"):
    try:
        jd = extract_job_description(job_url)
        resume, cover = generate_resume_coverletter(jd)

        styled_resume = style_resume_for_display(resume)
        docx_path = save_docx(resume, filename="generated_resume.docx")
        # write_output(resume, "generated_resume." + output_format, output_format)
        # write_output(cover, "generated_cover_letter." + output_format, output_format)

        # return f"Resume and cover letter generated in {output_format.upper()} format!"

        return styled_resume, docx_path
    except Exception as e:
        return f"Error: {str(e)}"

with gr.Blocks() as demo:
    gr.Markdown("# 🤖 PersoVox: AI-Tailored Resume Generator")

    with gr.Row():
        job_link_input = gr.Textbox(label="Paste Job Link", placeholder="https://example.com/job-posting")
        generate_btn = gr.Button("Generate Resume")

    resume_preview = gr.Markdown(label="Preview Resume")
    resume_file_output = gr.File(label="Download .docx")

    generate_btn.click(
        fn=generate_resume,
        inputs=[job_link_input],
        outputs=[resume_preview, resume_file_output]
    )

# iface = gr.Interface(
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
