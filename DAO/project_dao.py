import json
from dateutil.parser import isoparse
from datetime import datetime
from fastapi import HTTPException
from sqlalchemy import select, update, delete, and_, func

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

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

        created_at = isoparse(github_data["created_at"]) if github_data.get("created_at") else None
        updated_at = isoparse(github_data["updated_at"]) if github_data.get("updated_at") else None
        
        new_project = models.Project(
            repo_name=repo_name,
            owner_name=owner_name,
            full_readme=github_data.get("readme", ""), 
            repo_created_at=created_at,
            repo_updated_at=updated_at,
            github_data=json.dumps(github_data)  # Сериализуем словарь в JSON строку
        )
        
        db.add(new_project)
        await db.commit()
        await db.refresh(new_project)
        
        return new_project
    
    @classmethod
    async def update_project(cls,
                            db: AsyncSession,
                            project_id: int,
                            repo_name: str,
                            github_data: dict):
        created_at = isoparse(github_data["created_at"]) if github_data.get("created_at") else None
        updated_at = isoparse(github_data["updated_at"]) if github_data.get("updated_at") else None
        query = update(models.Project).where(models.Project.id == project_id).values(
            repo_name=repo_name,
            full_readme=github_data.get("readme", ""), 
            repo_created_at=created_at,
            repo_updated_at=updated_at,
            github_data=json.dumps(github_data) 
        )

        await db.execute(query)
        await db.commit()
        

    @classmethod
    async def get_all_projects(cls, db: AsyncSession):
        query = select(models.Project)

        projects = await db.execute(query)

        return projects.scalars().all()
    
    
    # SYNC METHODS #
    @classmethod
    def sync_get_all_projects_for_update(cls, db: Session, updated_at: str):
            query = select(models.Project).where(models.Project.repo_updated_at != updated_at)

            projects = db.execute(query)

            return projects.all()
    
    @classmethod
    def sync_get_project(cls, 
                         db: Session, 
                         project_id: int):
        return db.query(models.Project).filter(models.Project.id == project_id).first()
    
    @classmethod
    def sync_get_all_projects(cls, 
                         db: Session):
        return db.query(models.Project).all()
    
    @classmethod
    def sync_get_project_for_updates(cls, 
                         db: Session, 
                         updated_at: str):
        query = select(models.Project).where(models.Project.repo_updated_at != updated_at)

        project = db.execute(query)

        return db.query(models.Project).filter(models.Project.repo_updated_at != updated_at).first()

    @classmethod
    def sync_update_project(cls, 
                            db: Session, 
                            project_id: int, 
                            repo_name: str, 
                            github_data: dict):
        project = cls.sync_get_project(db=db, project_id=project_id)
        if not project:
            return None

        created_at = isoparse(github_data["created_at"]) if github_data.get("created_at") else None
        updated_at = isoparse(github_data["updated_at"]) if github_data.get("updated_at") else None
        
        project.repo_name = repo_name
        project.full_readme = github_data.get("readme", "")
        project.repo_created_at = created_at
        project.repo_updated_at = updated_at
        project.github_data = json.dumps(github_data)

        db.commit()
        db.refresh(project)

        return project


