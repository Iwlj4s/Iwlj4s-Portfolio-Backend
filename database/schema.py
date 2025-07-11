from pydantic import BaseModel, Field

from typing import Union


class Something(BaseModel):
    name: Union[str, None] = Field(default=None, min_length=3, title="Имя чего то")


class User(BaseModel):
    user_name: Union[str, None] = Field(default=None, min_length=3, title="Имя пользователя")
    name: Union[str, None] = Field(default=None, min_length=3, title="User name пользователя")
    email: Union[str, None] = Field(default=None, title="Эл.почта пользователя")

    avatar_url: Union[str, None] = Field(default=None, title="Аватарка пользователя")



# Token #
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Union[str, None] = None
    id: int