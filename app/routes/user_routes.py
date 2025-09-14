from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from typing import Optional
from app.services.user_service import create_user, get_all_users
from app.routes.admin_routes import get_current_admin

router = APIRouter()

# Pydantic schemas
class UserCreate(BaseModel):
    name: str
    status: int
    count: Optional[int] = None
    message: Optional[str] = None

class User(BaseModel):
    id: str = Field(alias="_id")
    name: str
    status: int
    count: Optional[int] = None
    message: Optional[str] = None
    
    class Config:
        populate_by_name = True

class UserResponse(BaseModel):
    inserted_id: str
    user: UserCreate

@router.post("/users/", response_model=UserResponse)
async def add_user(user: UserCreate):
    user_dict = user.dict()
    inserted_id = await create_user(user_dict)
    return {"inserted_id": inserted_id, "user": user_dict}

@router.get("/users/", response_model=list[User])
async def list_users(current_admin: dict = Depends(get_current_admin)):
    """Get all users - requires admin authentication"""
    return await get_all_users()
