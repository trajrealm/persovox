from fastapi import APIRouter
from src.db.vectorstore_singleton import get_all_vectorstore_users

router = APIRouter()

@router.get("/users")
def get_users():
    users = get_all_vectorstore_users()
    return {"users": users}
