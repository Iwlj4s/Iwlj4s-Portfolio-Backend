import time
from dateutil.parser import isoparse
from celery_stuff.celery_app import app
from DAO.project_dao import ProjectDAO
from database.database import SyncSessionLocal

from helpers import github_helper

# TODO: Add loggs using logger

@app.task(bind=True, max_retries=3, default_retry_delay=60)
def update_projects_github_data(self, projects_data):
    db = SyncSessionLocal()
    try:
        for p in projects_data:
            try:
                project_id = p["id"]
                owner_name = p["owner_name"]
                repo_name = p["repo_name"]
                repo_updated_at_str = p.get("repo_updated_at")

                print(f"Project {project_id} DB repo_updated_at: {repo_updated_at_str}")

                github_data = github_helper.sync_get_gitgub_repository(
                    repo_owner=owner_name,
                    repo_name=repo_name
                )

                if not github_data:
                    print(f"Project {project_id}: no github data, skipping")
                    continue

                github_updated_at_str = github_data.get("updated_at")
                print(f"Project {project_id} GITHUB repo_updated_at: {github_updated_at_str}")

                if not github_updated_at_str:
                    print(f"Project {project_id}: no updated_at in github data, skipping")
                    continue

                db_updated_at = isoparse(repo_updated_at_str).replace(tzinfo=None) if repo_updated_at_str else None
                github_updated_at = isoparse(github_updated_at_str).replace(tzinfo=None)

                print(f"Project {project_id} DB updated_at: {db_updated_at}")
                print(f"Project {project_id} GITHUB updated_at: {github_updated_at}")

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

            except Exception as project_exc:
                print(f"Error processing project {p.get('id')}: {project_exc}")
                # Можно сделать self.retry() для конкретной задачи, но осторожно с повторениями

    except Exception as e:
        print(f"Fatal error in update_projects_github_data: {e}")
        raise self.retry(exc=e)
    finally:
        db.close()
