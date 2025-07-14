from pydantic import BaseModel, Field

from typing import Union


class Something(BaseModel):
    name: Union[str, None] = Field(default=None, min_length=3, title="Имя чего то")


class User(BaseModel):
    user_name: Union[str, None] = Field(default=None, min_length=3, title="Имя пользователя")
    name: Union[str, None] = Field(default=None, min_length=3, title="User name пользователя")
    email: Union[str, None] = Field(default=None, title="Эл.почта пользователя")
    telegram: Union[str, None] = Field(default=None, title="Телеграм пользователя")
    avatar_url: Union[str, None] = Field(default=None, title="Аватарка пользователя")


class ChangeBio(BaseModel):
    bio: Union[str, None] = Field(default="Нет информации", min_length=10, title="Информация о себе")


class AddProject(BaseModel):
    repository_name: Union[str, None] = Field(title="Название репы")


# Token #
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Union[str, None] = None
    id: int