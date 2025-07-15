from typing import List
from sqlalchemy import DateTime, String, ForeignKey, Column, Integer, Text
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

    

class Project(Base):
    __tablename__ = 'projects'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    repo_name: Mapped[str] = mapped_column(String, unique=True)
    owner_name: Mapped[str] = mapped_column(String, unique=False)

    full_readme: Mapped[str] = mapped_column(Text, unique=False)          

    repo_created_at: Mapped[DateTime] = mapped_column(DateTime) 
    repo_updated_at: Mapped[DateTime] = mapped_column(DateTime) 

    # "Cached" Github data 
    github_data: Mapped[str] = mapped_column(Text)
