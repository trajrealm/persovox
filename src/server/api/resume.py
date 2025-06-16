from fastapi import APIRouter, UploadFile, File, HTTPException, Query
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel
from pathlib import Path
import os
import shutil

router = APIRouter()

class DeleteResumeRequest(BaseModel):
    username: str
    filename: str

@router.post("/upload_resume")
def upload_resume(username: str, file: UploadFile = File(...)):
    upload_dir = Path(f"./data/{username}/resumes")
    upload_dir.mkdir(parents=True, exist_ok=True)

    file_path = upload_dir / file.filename
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"message": f"Uploaded {file.filename} successfully."}

@router.get("/list_resumes")
def list_resumes(username: str = Query(...)):
    user_folder = os.path.join("data", username, "resumes")
    if not os.path.exists(user_folder):
        return JSONResponse(content={"resumes": []})

    resumes = [
        f for f in os.listdir(user_folder)
        if os.path.isfile(os.path.join(user_folder, f)) and f.lower().endswith(".pdf")
    ]
    return {"resumes": resumes}

@router.delete("/delete_resume")
async def delete_resume(req: DeleteResumeRequest):
    user_folder = os.path.join("./data", req.username, "resumes")
    file_path = os.path.join(user_folder, req.filename)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    try:
        os.remove(file_path)
        return {"message": f"File '{req.filename}' deleted successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete file: {str(e)}")

@router.get("/download_resume")
async def download_resume(username: str, filename: str):
    file_path = os.path.join("./data", username, "resumes", filename)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(
        path=file_path,
        filename=filename,
        media_type='application/pdf'
    )
