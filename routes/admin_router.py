from fastapi import Depends, APIRouter, Response

from sqlalchemy.ext.asyncio import AsyncSession

from database.database import get_db
from database.schema import User
from database import schema, models
from helpers.general_helper import CheckHTTP404NotFound

from DAO.general_dao import GeneralDAO
from repository.admin_repository import get_current_admin

admin_router = APIRouter(
    prefix="/admin",
    tags=["admin"]
)

@admin_router.post("/logout", tags=["admin"])
async def logout(response: Response):
    response.delete_cookie(key='user_access_token')
    return {'message': 'Пользователь успешно вышел из системы'}


@admin_router.get("/me/", status_code=200, tags=["admin"])
async def get_me(response: Response,
                 user_data: User = Depends(get_current_admin)):
    return user_data


# @user_router.get("/me/somethings", status_code=200, tags=["users"])
# async def get_current_user_somethings(current_user: schema.User = Depends(get_current_user),
#                                       db: AsyncSession = Depends(get_db)):
#     return await user_repository.get_current_user_somethings(current_user=current_user, db=db)


# @user_router.get("/me/{something_id}", status_code=200, tags=["users"])
# async def get_current_user_somethings(something_id: int,
#                                       response: Response,
#                                       current_user: schema.User = Depends(get_current_user),
#                                       db: AsyncSession = Depends(get_db)):
#     return await user_repository.get_current_user_something(something_id=something_id,
#                                                             current_user=current_user,
#                                                             response=response,
#                                                             db=db)
