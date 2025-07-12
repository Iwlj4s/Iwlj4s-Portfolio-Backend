from typing import List
from sqlalchemy import String, ForeignKey, Column, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.database import Base


class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    github_id: Mapped[int] = mapped_column(Integer, unique=True)
    github_login: Mapped[str] = mapped_column(String)  
    name: Mapped[str] = mapped_column(String)          
    email: Mapped[str] = mapped_column(String, unique=True, nullable=True)
    telegram: Mapped[str] = mapped_column(String, nullable=True)

    avatar_url: Mapped[str] = mapped_column(String, nullable=True)
    bio: Mapped[str] = mapped_column(String, nullable=True)          

    

