import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from src.utils.user_utils import get_available_users
from src.services.resume_processor import index_user_json_resume
from src.db.database import Base, engine

from src.server.api.auth import router as auth_router
from src.server.api.resume import router as resume_router
from src.server.api.kb import router as kb_router
from src.server.api.generation import router as gen_router
from src.server.api.user import router as user_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    users = get_available_users()
    print(f"Available users: {users}")
    for user in users:
        index_user_json_resume(user)
    yield

app = FastAPI(lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# Create tables
Base.metadata.create_all(bind=engine)

# Include route modules
app.include_router(auth_router)
app.include_router(resume_router)
app.include_router(kb_router)
app.include_router(gen_router)
app.include_router(user_router)
