from fastapi import Depends, HTTPException, Response
from fastapi.responses import JSONResponse

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from DAO.project_dao import ProjectDAO
from DAO.user_dao import UserDAO
from database.database import get_db, get_sync_db
from database import models, schema
from helpers.token_helper import get_token, verify_token
from celery_stuff.celery_tasks import update_project_github_data, update_projects_github_data
from helpers import github_helper

from DAO.general_dao import GeneralDAO


async def get_current_admin(db: AsyncSession = Depends(get_db),
                           token: str = Depends(get_token)):
    user_id = verify_token(token=token)
    print("user_id in get current user: ", user_id)
    if not user_id:
        return {
            'message': "Token not found",
            'status_code': 401,
        }
    user = await GeneralDAO.get_item_by_id(db=db, item=models.User, item_id=int(user_id))
    await db.refresh(user)

    return user


async def get_user(db: AsyncSession = Depends(get_db)):
    user = await UserDAO.get_user_by_id(db=db,
                                  user_id=1)
    
    return user


async def change_bio(request: schema.ChangeBio,
                     response: Response,
                     user: schema.User,
                     db: AsyncSession = Depends(get_db)):
    
    if request.bio == None:
        return {"message": "Bio has been not changed"}
    
    await UserDAO.change_bio(db=db,
                             user_github_id=user.github_id,
                             new_bio=request.bio)
    
    return{
        'message': 'Информация изменена',
        'new_bio': request.bio
    }

async def get_tasks_status(task):
    try:        
        if not task:
            return JSONResponse(
                status_code=200,
                content={
                    "status": "NOT_FOUND",
                    "state": "NOT_FOUND",
                    "message": "Task not found or expired"
                }
            )
        
        if task.state == 'PENDING':
            return {
                "status": "PENDING",
                "state": task.state,
                "result": None
            }
        
        if task.state == 'PROGRESS':
            return {
                "status": "PROGRESS",
                "state": task.state,
                "result": task.info
            }
        
        if task.state == 'SUCCESS':
            task.forget()
            return {
                "status": "SUCCESS",
                "state": task.state,
                "result": task.result
            }
        
        if task.state == 'FAILURE':
            task.forget()
            return {
                "status": "FAILURE",
                "state": task.state,
                "result": str(task.result)
            }
        
        return {
            "status": task.state,
            "state": task.state,
            "result": None
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail={
                "status": "ERROR",
                "message": str(e)
            }
        )

def update_projects(response: Response,
                    db: Session = Depends(get_sync_db)):

    projects = ProjectDAO.sync_get_all_projects(db=db)

    projects_data = [
        {
            "id": p.id,
            "owner_name": p.owner_name,
            "repo_name": p.repo_name,
            "description": p.description,
            "repo_updated_at": p.repo_updated_at.strftime("%Y-%m-%d %H:%M:%S.%f") if p.repo_updated_at else None
        }
        for p in projects
    ]


    task = update_projects_github_data.delay(projects_data=projects_data)

    return {'task_id': task.id}

def update_project(response: Response,
                  project_id: int,
                  db: Session = Depends(get_sync_db)):
    
    project = ProjectDAO.sync_get_project(db=db, project_id=project_id)
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    project_data = {
        "id": project.id,
        "owner_name": project.owner_name,
        "repo_name": project.repo_name,
        "repo_updated_at": project.repo_updated_at.strftime("%Y-%m-%d %H:%M:%S.%f") if project.repo_updated_at else None
    }

    task = update_project_github_data.delay(project=project_data)

    return {'task_id': task.id}
