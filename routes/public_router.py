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

    return {
    "status": 200,
    "user": {
        "id": user.id,
        "github_id": user.github_id,
        "github_login": user.github_login,
        "name": user.name,
        "avatar_url": user.avatar_url,
        "email": user.email
    }
}