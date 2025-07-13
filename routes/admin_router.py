from fastapi import Depends, APIRouter, Response

from sqlalchemy.ext.asyncio import AsyncSession

from database.database import get_db
from database.schema import User
from database import schema, models
from helpers.general_helper import CheckHTTP404NotFound

from DAO.general_dao import GeneralDAO
from repository import admin_repository
from repository.admin_repository import get_current_admin

admin_router = APIRouter(
    prefix="/admin",
    tags=["admin"]
)

@admin_router.post("/logout", tags=["admin"])
async def logout(response: Response):
    response.delete_cookie(key='user_access_token')
    return {'message': 'Пользователь успешно вышел из системы'}


@admin_router.get("/me", status_code=200, tags=["admin"])
async def get_me(response: Response,
                 user_data: User = Depends(get_current_admin)):
    return user_data


@admin_router.get("/profile", status_code=200, tags=["admin"])
async def get_me(response: Response, 
                 db: AsyncSession = Depends(get_db),
                 user_data: User = Depends(get_current_admin)):
    user = await admin_repository.get_user(db=db)

    if not user:
        return {"status": 404, 
                "message": "User not found"}
    
    user_github_data = {
        "github_login": user.github_login,
        "name": user.name,
        "avatar_url": user.avatar_url
    }

    user_data = { 
        "id": user.id,
        "email": user.email,
        "telegram": user.telegram
    }

    return {
    "user_github_data": user_github_data,
    "user_data": user_data,
    "user_bio": user.bio
}


@admin_router.patch("/change_bio", status_code=200, tags=["admin"])
async def change_bio(response: Response,
                     request: schema.ChangeBio,
                     user_data: User = Depends(get_current_admin),
                     db: AsyncSession = Depends(get_db)):
    
    return await admin_repository.change_bio(request=request, 
                                       response=response, 
                                       user=user_data, 
                                       db=db)

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
