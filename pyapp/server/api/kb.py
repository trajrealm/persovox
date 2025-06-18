from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List
import os
import subprocess
import sys
import traceback
import json

from pyapp.db.models import UserResumeSelections
from pyapp.db.database import get_db

router = APIRouter()

class KnowledgeBaseRequest(BaseModel):
    username: str
    selected_resumes: List[str]

class ResumeSelectionRequest(BaseModel):
    username: str
    selected_resumes: List[str]

@router.post("/regenerate_knowledgebase")
async def regenerate_knowledgebase(req: KnowledgeBaseRequest):
    try:
        success = regenerate_kb(req.username, req.selected_resumes)
        if success:
            return {"message": "Reference Resumes refreshed successfully."}
        else:
            raise HTTPException(status_code=500, detail="Failed to regenerate knowledge base")
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

def regenerate_kb(username: str, files: list) -> bool:
    script_path = os.path.join("src", "services", "resume_processor.py")
    root_path = os.path.abspath(".")
    env = os.environ.copy()
    env["PYTHONPATH"] = f"{root_path}:{env.get('PYTHONPATH', '')}"
    try:
        result = subprocess.run(
            [
                sys.executable,
                script_path,
                username,
                str(files)
            ],
            env=env,
            check=True,
            capture_output=True,
            text=True
        )
        print("Subprocess Output:", result.stdout)
        print("Subprocess stderr:", result.stderr)
        return True
    except subprocess.CalledProcessError as e:
        traceback.print_exc()
        print("Subprocess Error:", e.stderr)
        return False

@router.get("/get_resume_selections")
def get_resume_selections(username: str, db: Session = Depends(get_db)):
    selections = db.query(UserResumeSelections.resume_filename).filter(
        UserResumeSelections.username == username,
        UserResumeSelections.selected == True
    ).all()
    return [s[0] for s in selections]

@router.post("/save_resume_selections")
def save_resume_selections(data: ResumeSelectionRequest, db: Session = Depends(get_db)):
    username = data.username
    selected_files = set(data.selected_resumes)

    existing = db.query(UserResumeSelections).filter_by(username=username).all()
    existing_files = {e.resume_filename: e for e in existing}

    for filename in selected_files:
        if filename in existing_files:
            existing_files[filename].selected = True
        else:
            db.add(UserResumeSelections(
                username=username,
                resume_filename=filename,
                selected=True
            ))

    for filename, obj in existing_files.items():
        if filename not in selected_files:
            obj.selected = False

    db.commit()
    return {"message": "Selections saved successfully."}
