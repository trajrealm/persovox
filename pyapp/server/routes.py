import sys
import os
import traceback
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from sqlalchemy.orm import Session

from pyapp.utils.regenerate_kb import run_regenerate_kb
from pyapp.utils.user_utils import get_available_users
from pyapp.services.resume_processor import index_user_json_resume
from pyapp.db.database import Base, engine
from pyapp.db.database import get_db
from pyapp.db.models import UserResumeSelections, User




from pyapp.server.api.auth import router as auth_router
from pyapp.server.api.resume import router as resume_router
from pyapp.server.api.kb import router as kb_router
from pyapp.server.api.generation import router as gen_router
from pyapp.server.api.user import router as user_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    db_gen = get_db()  # get generator
    db = next(db_gen)  # get Session instance
    try:
        users = db.query(User).all()
        print("Available users:", users)
        for user in users:
            selections = db.query(UserResumeSelections.resume_filename).filter(
                UserResumeSelections.username == user.username,
                UserResumeSelections.selected == True
            ).all()
            run_regenerate_kb(user.username, [s[0] for s in selections])
    except:
        traceback.print_exc()
    finally:
        db_gen.close()  # clean up session
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
