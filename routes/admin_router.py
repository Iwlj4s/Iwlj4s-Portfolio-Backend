import json
import celery
from fastapi import Depends, APIRouter, HTTPException, Response
from celery.result import AsyncResult
from fastapi.responses import JSONResponse

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from database.database import get_db, get_sync_db
from database.schema import User
from database import schema, models
from helpers import github_helper
from helpers.general_helper import CheckHTTP404NotFound

from DAO.general_dao import GeneralDAO
from DAO.project_dao import ProjectDAO
from repository import admin_repository
from repository.admin_repository import get_current_admin

admin_router = APIRouter(
    prefix="/admin",
    tags=["admin"]
)

@admin_router.post("/logout", tags=["admin"])
async def logout(response: Response):
    response.delete_cookie(key='user_access_token')
    return {'message': 'Пользователь успешно вышел из системы'}


@admin_router.get("/me", status_code=200, tags=["admin"])
async def get_me(response: Response,
                 user_data: User = Depends(get_current_admin)):
    return user_data


@admin_router.get("/profile", status_code=200, tags=["admin"])
async def get_me(response: Response, 
                 db: AsyncSession = Depends(get_db),
                 user_data: User = Depends(get_current_admin)):
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


@admin_router.patch("/change_bio", status_code=200, tags=["admin"])
async def change_bio(response: Response,
                     request: schema.ChangeBio,
                     user_data: User = Depends(get_current_admin),
                     db: AsyncSession = Depends(get_db)):
    
    return await admin_repository.change_bio(request=request, 
                                       response=response, 
                                       user=user_data, 
                                       db=db)

# PROJECTS #
@admin_router.post("/projects/add", status_code=200, tags=["admin"])
async def add_project(response: Response,
                    request: schema.AddProject,
                    user_data: User = Depends(get_current_admin),
                    db: AsyncSession = Depends(get_db)):
    
    
    user = await admin_repository.get_user(db=db)
    print("USER", user)
    github_data = await github_helper.get_gitgub_repository(repo_owner=user.github_login,
                                                            repo_name=request.repository_name)
    print("User data")

    print(f"Type of github_data: {type(github_data)}")
    print(f"Content sample: {str(github_data)[:200]}...")
    print(f"JSON serialized: {json.dumps(github_data, default=str)[:200]}...")

    await ProjectDAO.add_project(db=db,
                                repo_name=request.repository_name,
                                owner_name=user.github_login,
                                github_data=github_data)
    
    
    return {'status': "created"}

@admin_router.post("/projects/update", status_code=200, tags=["admin"])
async def update_projects(response: Response,
                          user_data: User = Depends(get_current_admin), 
                          db: Session = Depends(get_sync_db)):
    result = admin_repository.update_projects(db=db, response=response)
    return result

@admin_router.post("/projects/update/{project_id}", status_code=200, tags=["admin"])
async def update_project(response: Response,
                         project_id: int,
                         user_data: User = Depends(get_current_admin),
                         db: Session = Depends(get_sync_db)):
    
    result = admin_repository.update_project(db=db, response=response, project_id=project_id)

    return result


@admin_router.get("/tasks/{task_id}/status", tags=["admin"])
async def get_task_status(task_id: str):
    task = AsyncResult(task_id)

    return await admin_repository.get_tasks_status(task=task)
        

@admin_router.delete("/projects/delete/{project_id}", status_code=200, tags=["admin"])
async def delete_project(response: Response,
                         project_id: int,
                         user_data: User = Depends(get_current_admin), 
                         db: AsyncSession = Depends(get_db)):
    await ProjectDAO.delete_project(db=db, project_id=project_id)

    return{
        "Project Deleted"
    }

@admin_router.get("/projects", status_code=200, tags=["admin"])
async def get_projects(response: Response,
                       user_data: User = Depends(get_current_admin), 
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

# @user_router.get("/me/somethings", status_code=200, tags=["users"])
# async def get_current_user_somethings(current_user: schema.User = Depends(get_current_user),
#                                       db: AsyncSession = Depends(get_db)):
#     return await user_repository.get_current_user_somethings(current_user=current_user, db=db)


# @user_router.get("/me/{something_id}", status_code=200, tags=["users"])
# async def get_current_user_somethings(something_id: int,
#                                       response: Response,
#                                       current_user: schema.User = Depends(get_current_user),
#                                       db: AsyncSession = Depends(get_db)):
#     return await user_repository.get_current_user_something(something_id=something_id,
#                                                             current_user=current_user,
#                                                             response=response,
#                                                             db=db)
