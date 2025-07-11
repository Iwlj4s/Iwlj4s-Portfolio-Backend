from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from database.database import get_db
from database import models
from helpers.token_helper import get_token, verify_token

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

    return user

