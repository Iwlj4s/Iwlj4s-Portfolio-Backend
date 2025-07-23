from fastapi import Depends, APIRouter, Response

from sqlalchemy.ext.asyncio import AsyncSession

from DAO.project_dao import ProjectDAO
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

@public_router.get("/projects", status_code=200, tags=["public_projects"])
async def get_projects(response: Response,
                       db: AsyncSession = Depends(get_db)):
    projects = await ProjectDAO.get_all_projects(db=db)

    return[
        {
            "id": p.id,
            "repo_name": p.repo_name,
            "owner_name": p.owner_name,
            "full_readme": p.full_readme,
            "repo_created_at": p.repo_created_at,
            "repo_updated_at": p.repo_updated_at

        }
        for p in projects
    ]
