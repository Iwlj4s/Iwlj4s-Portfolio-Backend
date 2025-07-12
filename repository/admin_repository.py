from fastapi import Depends, Response

from sqlalchemy.ext.asyncio import AsyncSession

from DAO.user_dao import UserDAO
from database.database import get_db
from database import models, schema
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
    await db.refresh(user)

    return user


async def get_user(db: AsyncSession = Depends(get_db)):
    user = await UserDAO.get_user_by_id(db=db,
                                  user_id=1)
    
    return user


async def change_bio(request: schema.ChangeBio,
                     response: Response,
                     user: schema.User,
                     db: AsyncSession = Depends(get_db)):
    
    if request.bio == None:
        return {"message": "Bio has been not changed"}
    
    await UserDAO.change_bio(db=db,
                             user_github_id=user.github_id,
                             new_bio=request.bio)
    
    return{
        'message': 'Информация изменена',
        'new_bio': request.bio
    }