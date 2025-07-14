import json
from fastapi import HTTPException
from sqlalchemy import select, update, delete, and_, func

from sqlalchemy.ext.asyncio import AsyncSession

from database import models, schema
from database.models import User


class ProjectDAO:
    @classmethod
    async def add_project(cls,
                        db: AsyncSession,
                        repo_name: str,
                        owner_name: str,
                        github_data: dict) -> models.Project:
        print(f"Type of github_data: {type(github_data)}")
        print(f"Content sample: {str(github_data)[:200]}...")
        print(f"JSON serialized: {json.dumps(github_data, default=str)[:200]}...")
        
        new_project = models.Project(
            repo_name=repo_name,
            owner_name=owner_name,
            full_readme=github_data.get("readme", ""), 
            github_data=json.dumps(github_data)  # Сериализуем словарь в JSON строку
        )
        
        db.add(new_project)
        await db.commit()
        await db.refresh(new_project)
        
        return new_project
    
    @classmethod
    async def get_project(cls, 
                          db: AsyncSession, 
                          project_id: int) -> models.Project:
        project = await db.get(models.Project, project_id)
        if project:
            project.github_data = json.loads(project.github_data)
        return project
   