from fastapi import APIRouter, Response, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from helpers import github_helper
from database.database import get_db

from config import settings



github_router = APIRouter(prefix="/github", tags=["Github"])


@github_router.get("/repo/{repo_owner}/{repo_name}")
async def get_repo_info(repo_owner: str, 
                        repo_name: str):
    return await github_helper.get_gitgub_repository(repo_owner=repo_owner, repo_name=repo_name)
