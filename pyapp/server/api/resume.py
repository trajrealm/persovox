from fastapi import APIRouter, UploadFile, File, HTTPException, Query
from fastapi.responses import JSONResponse, FileResponse, StreamingResponse
from pydantic import BaseModel
from pathlib import Path
from supabase import create_client, Client

from config.config import SUPABASE_URL, SUPABASE_KEY, BUCKET_NAME, RESUME_DIR, LOCAL_DWNLD_DIR

router = APIRouter()

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

class DeleteResumeRequest(BaseModel):
    username: str
    filename: str


@router.post("/upload_resume")
async def upload_resume(username: str, file: UploadFile = File(...)):

    # Generate a unique filename to avoid collisions
    original_filename = file.filename
    supabase_path = f"{RESUME_DIR}/{username}/{original_filename}"

    file_content = await file.read()

    # Upload to Supabase storage
    response = supabase.storage.from_(BUCKET_NAME).upload(
        path=supabase_path,
        file=file_content,
        file_options={"content-type": file.content_type, "cache-control": "3600"}
    )

    if not response.path or not response.full_path:
        return {
            "error": f"Failed to upload {file.filename} to Supabase storage.",
            "storage_path": None
        }

    return {
        "message": f"Uploaded {file.filename} successfully.",
        "storage_path": supabase_path
    }


@router.get("/list_resumes")
def list_resumes(username: str = Query(...)):
    folder_path = f"{RESUME_DIR}/{username}/"

    response = supabase.storage.from_(BUCKET_NAME).list(path=folder_path)

    # Filter only PDFs
    pdf_files = [file["name"] for file in response if file["name"].lower().endswith(".pdf")]

    return {"resumes": pdf_files}


@router.delete("/delete_resume")
async def delete_resume(req: DeleteResumeRequest):
    file_path = f"{RESUME_DIR}/{req.username}/{req.filename}"

    # Attempt to remove from Supabase bucket
    response = supabase.storage.from_(BUCKET_NAME).remove([file_path])

    return {"message": f"File '{req.filename}' deleted successfully."}


@router.get("/download_resume")
async def download_resume(username: str = Query(...), filename: str = Query(...)):
    file_path = f"{RESUME_DIR}/{username}/{filename}"
    print(f"Downloading file: {file_path}")

    with open(f"{LOCAL_DWNLD_DIR}/{RESUME_DIR}/{username}{filename}", "wb+") as f:
        response = supabase.storage.from_(BUCKET_NAME).download(file_path)
        f.write(response)

    return FileResponse(
        path=f"{LOCAL_DWNLD_DIR}/{RESUME_DIR}/{username}/{filename}",
        filename=filename,
        media_type='application/pdf'
    )

# @router.post("/upload_resume")
# def upload_resume(username: str, file: UploadFile = File(...)):
#     upload_dir = Path(f"./data/{username}/resumes")
#     upload_dir.mkdir(parents=True, exist_ok=True)

#     file_path = upload_dir / file.filename
#     with file_path.open("wb") as buffer:
#         shutil.copyfileobj(file.file, buffer)

#     return {"message": f"Uploaded {file.filename} successfully."}

# @router.get("/list_resumes")
# def list_resumes(username: str = Query(...)):
#     user_folder = os.path.join("data", username, "resumes")
#     if not os.path.exists(user_folder):
#         return JSONResponse(content={"resumes": []})

#     resumes = [
#         f for f in os.listdir(user_folder)
#         if os.path.isfile(os.path.join(user_folder, f)) and f.lower().endswith(".pdf")
#     ]
#     return {"resumes": resumes}



# @router.delete("/delete_resume")
# async def delete_resume(req: DeleteResumeRequest):
#     user_folder = os.path.join("./data", req.username, "resumes")
#     file_path = os.path.join(user_folder, req.filename)

#     if not os.path.exists(file_path):
#         raise HTTPException(status_code=404, detail="File not found")

#     try:
#         os.remove(file_path)
#         return {"message": f"File '{req.filename}' deleted successfully."}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Failed to delete file: {str(e)}")



# @router.get("/download_resume")
# async def download_resume(username: str, filename: str):
#     file_path = os.path.join("./data", username, "resumes", filename)

#     if not os.path.exists(file_path):
#         raise HTTPException(status_code=404, detail="File not found")

#     return FileResponse(
#         path=file_path,
#         filename=filename,
#         media_type='application/pdf'
#     )

