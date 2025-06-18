# rag_engine/utils/file_saver.py

from docx import Document
from pathlib import Path

def save_docx(content: str, filename: str = "resume.docx") -> str:
    doc = Document()
    for line in content.strip().split("\n"):
        doc.add_paragraph(line)
    output_path = Path("output") / filename
    output_path.parent.mkdir(exist_ok=True)
    doc.save(output_path)
    return str(output_path)
