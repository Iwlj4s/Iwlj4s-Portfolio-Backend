import asyncio
import time
from dateutil.parser import isoparse
from celery_stuff.celery_app import app
from DAO.project_dao import ProjectDAO
from database.database import SyncSessionLocal

from helpers import github_helper
import json


@app.task(bind=True, max_retries=3, default_retry_delay=60)
def update_projects_github_data(self, projects_data):
    db = SyncSessionLocal()

    try:
        for p in projects_data:
            project_id = p["id"]
            owner_name = p["owner_name"]
            repo_name = p["repo_name"]
            repo_updated_at_str = p.get("repo_updated_at")

            print("DB repo_updated_at_str: \n", repo_updated_at_str)

            github_data = github_helper.sync_get_gitgub_repository(repo_owner=owner_name, 
                                                                   repo_name=repo_name)     
                   
            if not github_data:
                continue

            github_updated_at_str = github_data.get("updated_at")
            print("GITHUB repo_updated_at_str: \n", github_updated_at_str)

            if not github_updated_at_str:
                continue
                
            db_updated_at = isoparse(repo_updated_at_str).replace(tzinfo=None) if repo_updated_at_str else None
            github_updated_at = isoparse(github_updated_at_str).replace(tzinfo=None)
            print("DB repo_updated_at (converted): \n", db_updated_at)
            print("GITHUB repo_updated_at (converted): \n", github_updated_at)
            
            if db_updated_at != github_updated_at:
                print(f"Updating project {project_id} because dates differ")
                ProjectDAO.sync_update_project(
                    db=db, 
                    project_id=project_id, 
                    repo_name=repo_name,
                    github_data=github_data
                )
            else:
                print(f"Skipping project {project_id} - dates are the same")

    except Exception as e:
        return f"error: {e}"
    finally:
        db.close()