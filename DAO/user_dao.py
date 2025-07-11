from sqlalchemy import select, update, delete, and_, func

from sqlalchemy.ext.asyncio import AsyncSession

from database import models
from database.models import User


class UserDAO:
    @classmethod
    async def get_user_email(cls, db: AsyncSession, user_email: str):
        query = select(User).where(User.email == str(user_email))
        email = await db.execute(query)

        return email.scalars().first()

    @classmethod
    async def get_user_name(cls, db: AsyncSession, user_name: str):
        query = select(User).where(User.name == str(user_name))
        name = await db.execute(query)

        return name.scalars().first()

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