from fastapi import HTTPException
from starlette.responses import Response

from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from helpers.github_helper import github_auth_flow


async def take_access_token_for_admin(db: AsyncSession, 
                                      response: Response, 
                                      github_code: str):
    return await github_auth_flow(github_code, response, db)