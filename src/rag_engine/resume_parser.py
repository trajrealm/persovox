import os
import json
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv
import fitz  # PyMuPDF

load_dotenv()
client = OpenAI()

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text.strip()

def parse_resume_to_json(resume_text: str) -> dict:
    system_msg = {"role": "system", "content": "You are an expert in resume parsing. Extract the data in structured JSON format."}
    user_msg = {
        "role": "user",
        "content": f"""
From the text below, extract a structured JSON with these fields:

- name
- email
- phone
- address
- summary (look for sections titled "Summary", "About Me", "Profile", or an introductory paragraph near the top)
- highlights (look for sections titled "Highlights", "Achievements", "Accomplishments")
- experiences: list of objects {{
    job_title, 
    company, 
    location, 
    start_date, 
    end_date, 
    description: list of bullet point strings
    }}
- education: list of objects {{degree, university, location, graduation_year}}
- skills: list of strings
- certifications: list of objects {{name, issuer, year}}

Rules:
- Use only information present in the text.
- Do not invent anything.
- Return only a valid JSON — no explanations.
- Ensure that the `description` field in each experience is a list of bullet points (strings).
- DO NOT wrap the output in markdown blocks like ```json or ```.

Resume Text:
\"\"\"
{resume_text}
\"\"\"        
"""
    }

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[system_msg, user_msg],
        temperature=0.2
    )

    try:
        raw_json = response.choices[0].message.content.strip()
        # Clean extra formatting if any
        if raw_json.startswith("```json"):
            raw_json = raw_json[7:]
        if raw_json.endswith("```"):
            raw_json = raw_json[:-3]
        return json.loads(raw_json)
    except Exception as e:
        print(f"Error parsing LLM response: {e}")
        return {}

def batch_parse_resumes(input_folder, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    pdf_files = list(Path(input_folder).glob("*.pdf"))
    
    for pdf in pdf_files:
        print(f"Processing: {pdf.name}")
        text = extract_text_from_pdf(str(pdf))
        structured = parse_resume_to_json(text)

        if structured:
            out_path = Path(output_folder) / f"{pdf.stem}.json"
            with open(out_path, "w") as f:
                json.dump(structured, f, indent=2)
            print(f"Saved JSON: {out_path}")
        else:
            print(f"Failed to parse: {pdf.name}")


if __name__ == "__main__":
    for user in ["triloke", "qureena"]:
        input_folder = f"data/{user}/resumes"
        output_folder = f"data/{user}/resumes/parsed"
        batch_parse_resumes(input_folder, output_folder)