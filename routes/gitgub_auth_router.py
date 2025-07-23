from fastapi import APIRouter, Response, Depends, HTTPException
from fastapi.responses import RedirectResponse

from sqlalchemy.ext.asyncio import AsyncSession

from helpers.github_helper import github_auth_flow
from helpers.admin_helper import take_access_token_for_admin

from database.database import get_db

from config import settings

auth_router = APIRouter(prefix="/auth", tags=["Auth"])


@auth_router.get("/github")
async def auth_github():
    return RedirectResponse(
        f"{settings.GITHUB_AUTH_URL}client_id={settings.GITHUB_CLIENT_ID}"
    )


@auth_router.get("/github/callback")
async def github_callback(code: str, response: Response, db: AsyncSession = Depends(get_db)):
    try:
        data = await github_auth_flow(code, response, db)
        return data
    except HTTPException as e:
        return {"error": e.detail}


@auth_router.post("/login")
async def login(response: Response, 
                db: AsyncSession = Depends(get_db),):
    
    return await take_access_token_for_admin(db=db, response=response)