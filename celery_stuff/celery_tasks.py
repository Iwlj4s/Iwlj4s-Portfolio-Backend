import time
from dateutil.parser import isoparse
from celery_stuff.celery_app import app
from DAO.project_dao import ProjectDAO
from database.database import SyncSessionLocal

from helpers import github_helper
from datetime import datetime


# TODO: Add loggs using logger

@app.task(bind=True, max_retries=3, default_retry_delay=60)
def update_projects_github_data(self, projects_data):
    db = SyncSessionLocal()
    updated = 0
    try:
        total = len(projects_data)
        
        for i, p in enumerate(projects_data):
            project_id = p["id"]
            owner_name = p["owner_name"]
            repo_name = p["repo_name"]
            db_updated_at_str = p.get("repo_updated_at")

            github_data = github_helper.sync_get_gitgub_repository(
                repo_owner=owner_name,
                repo_name=repo_name
            )

            if not github_data:
                continue

            github_updated_at_str = github_data.get("updated_at")
            
            db_updated_at = None
            if db_updated_at_str:
                db_updated_at = datetime.strptime(db_updated_at_str, "%Y-%m-%d %H:%M:%S.%f")
            
            github_updated_at = None
            if github_updated_at_str:
                github_updated_at = isoparse(github_updated_at_str).replace(tzinfo=None)
            
            needs_update = False
            if db_updated_at and github_updated_at:
                needs_update = db_updated_at < github_updated_at
            else:
                needs_update = True

            if needs_update:
                ProjectDAO.sync_update_project(
                    db=db,
                    project_id=project_id,
                    repo_name=repo_name,
                    github_data=github_data
                )
                updated += 1

            self.update_state(
                state='PROGRESS',
                meta={
                    'current': i + 1,
                    'total': total,
                    'updated': updated,
                    'current_project': {
                        'owner_name': owner_name,
                        'repo_name': repo_name
                    }
                }
            )

        return {'status': 'completed', 'updated': updated, 'total': total}

    except Exception as e:
        print(f"Fatal error: {e}")
        raise self.retry(exc=e)
    finally:
        db.close()