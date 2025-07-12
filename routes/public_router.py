from fastapi import Depends, APIRouter, Response

from sqlalchemy.ext.asyncio import AsyncSession

from database.database import get_db

from repository import admin_repository

public_router = APIRouter(
    prefix="/public",
    tags=["public_router"])


@public_router.get("/profile", status_code=200, tags=["public_profile"])
async def get_public_profile(response: Response, 
                 db: AsyncSession = Depends(get_db)):
    user = await admin_repository.get_user(db=db)

    if not user:
        return {"status": 404, 
                "message": "User not found"}
    
    user_github_data = {
        "github_login": user.github_login,
        "name": user.name,
        "avatar_url": user.avatar_url
    }

    user_data = { 
        "id": user.id,
        "email": user.email,
        "telegram": user.telegram
    }
    

    return {
    "user_github_data": user_github_data,
    "user_data": user_data,
    "user_bio": user.bio
}
