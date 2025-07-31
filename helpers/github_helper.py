import time
from fastapi import HTTPException, status, Response
import httpx
import base64

from sqlalchemy.ext.asyncio import AsyncSession
from DAO.user_dao import UserDAO
from config import settings
from database import models, schema
from helpers.jwt_helper import create_access_token

project_token = settings.GITHUB_PROJECT_TOKEN
headers = {
    "Accept": "application/vnd.github.v3+json",
    "Authorization": f"token {project_token}"
}

async def get_github_user_data(code: str) -> dict:
    """Taking access_token and user data from GitHub"""
    async with httpx.AsyncClient() as client:
        # Take token
        token_response = await client.post(
            settings.GITHUB_TOKEN_URL,
            headers={"Accept": "application/json"},
            data={
                "client_id": settings.GITHUB_CLIENT_ID,
                "client_secret": settings.GITHUB_CLIENT_SECRET,
                "code": code,
            },
        )
        token_data = token_response.json()
        access_token = token_data.get("access_token")

        if not access_token:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Не удалось получить токен от GitHub",
            )

        # Take user data
        user_response = await client.get(
            settings.GITHUB_USER_URL,
            headers={"Authorization": f"Bearer {access_token}"},
        )
        user_data = user_response.json()
        return user_data


async def github_auth_flow(code: str, 
                           response: Response,
                           db: AsyncSession) -> dict:
    github_user = await get_github_user_data(code)

    if str(github_user["id"]) != settings.ALLOWED_GITHUB_ID:
        raise HTTPException(status_code=403, detail="Access denied")
    
    user = await UserDAO.get_user_by_github_id(db, str(github_user["id"]))
    if not user:
        user = models.User(
            github_id=str(github_user["id"]),
            github_login=github_user["login"],
            name=github_user.get("name") or github_user["login"],  
            avatar_url=github_user["avatar_url"],
            email="iwlj4s@inbox.ru",
            telegram="@Iwlj4s"  
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)

    access_token = create_access_token({"sub": str(user.id)})

    response.set_cookie(
        key="user_access_token",
        value=access_token,
        httponly=True,
        secure=True,  
        samesite="lax",
    )

    return {
        "access_token": access_token,
        "user": {
            "id": user.id,
            "github_id": user.github_id,
            "github_login": user.github_login,
            "name": user.name,
            "avatar_url": user.avatar_url,
            "email": user.email
        }
    }


async def get_gitgub_repository(repo_owner: str,
                                repo_name: str) -> dict:
    
    """
        Taking repo from https://api.github.com/repos/ 
    """
    async with httpx.AsyncClient() as client:

        repo_response = await client.get(
            f"https://api.github.com/repos/{repo_owner}/{repo_name}",
            headers=headers
        )

        if repo_response.status_code != 200:
            raise HTTPException(
                status_code=repo_response.status_code,
                detail="Не удалось получить репозиторий"
            )
        
        readme_content = ""  
        readme_html_url = None
        readme_data = {}
        readme_response = await client.get(
            f"https://api.github.com/repos/{repo_owner}/{repo_name}/readme",
            headers=headers
        )
        if readme_response.status_code == 200:
            readme_data = readme_response.json()
            readme_content = base64.b64decode(readme_data['content']).decode('utf-8')
    
        repo_response_json = repo_response.json()

        repo_data = {
            "full_name": repo_response_json.get("full_name"),
            "description": repo_response_json.get("description"),
            "html_url": repo_response_json.get("html_url"),
            "language": repo_response_json.get("language"), 
            "created_at": repo_response_json.get("created_at"),
            "updated_at": repo_response_json.get("updated_at"),
            "readme_html_url": readme_data.get("html_url") if readme_data else None,
            "readme": readme_content,
            "description": repo_response_json.get("description", "")
        }

        print("REPO DATA: \n", repo_data)

        return repo_data
    


def sync_get_gitgub_repository(repo_owner: str,
                                repo_name: str) -> dict:
    
    """
        SYNC FUNC FOR CELERY 
        Taking repo from https://api.github.com/repos/ 
    """
    time.sleep(1)
    with httpx.Client() as client:

        repo_response = client.get(
            f"https://api.github.com/repos/{repo_owner}/{repo_name}",
            headers=headers
        )

        print("GitHub request headers:", headers)

        if repo_response.status_code != 200:
            raise HTTPException(
                status_code=repo_response.status_code,
                detail="Не удалось получить репозиторий"
            )
        
        readme_content = ""  
        readme_html_url = None
        readme_data = {}
        time.sleep(0.5)
        readme_response = client.get(
            f"https://api.github.com/repos/{repo_owner}/{repo_name}/readme",
            headers=headers
        )
        if readme_response.status_code == 200:
            readme_data = readme_response.json()
            readme_content = base64.b64decode(readme_data['content']).decode('utf-8')
    
        repo_response_json = repo_response.json()

        repo_data = {
            "full_name": repo_response_json.get("full_name"),
            "description": repo_response_json.get("description"),
            "html_url": repo_response_json.get("html_url"),
            "language": repo_response_json.get("language"), 
            "created_at": repo_response_json.get("created_at"),
            "updated_at": repo_response_json.get("updated_at"),
            "readme_html_url": readme_data.get("html_url") if readme_data else None,
            "readme": readme_content,
            "description": repo_response_json.get("description", "")
        }

        print("REPO DATA: \n", repo_data)

        return repo_data
    