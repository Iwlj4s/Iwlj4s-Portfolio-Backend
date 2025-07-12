from sqlalchemy import select, update, delete, and_, func

from sqlalchemy.ext.asyncio import AsyncSession

from database import models, schema
from database.models import User


class UserDAO:
    @classmethod
    async def get_user_email(cls, db: AsyncSession, user_email: str):
        query = select(User).where(User.email == str(user_email))
        email = await db.execute(query)

        return email.scalars().first()


    @classmethod
    async def get_user_by_id(cls, db: AsyncSession, user_id: int):
        query = select(User).where(User.id == user_id)
        user = await db.execute(query)

        return user.scalars().first()

    @classmethod
    async def get_user_by_github_id(cls, db: AsyncSession, github_id: int):
        result = await db.execute(
            select(models.User).where(models.User.github_id == github_id)
        )

        return result.scalar_one_or_none()
    
    @classmethod
    async def change_bio(cls,
                         db: AsyncSession,
                         user_github_id: int,
                         new_bio: str):
        
        query = update(models.User).where(models.User.github_id == user_github_id).values(
            bio=new_bio
        )

        await db.execute(query)
        await db.commit()

 
