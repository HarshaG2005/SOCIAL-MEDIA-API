from pydantic import BaseModel,Field,ConfigDict,EmailStr,conint
from typing import Optional
from datetime import datetime
class CreatePost(BaseModel):
    title:str=Field(
        max_length=300
       )
    content:str|None=Field(
        max_length=500
    )
    published:bool=Field(
        default=True
    )

class User(BaseModel):
    id:int
    email:EmailStr
    created_at:datetime
    model_config=ConfigDict(from_attributes=True)
class Post(CreatePost):
    id:int
    created_at:datetime
    owner_id:int
    owner:User
    model_config = ConfigDict(from_attributes=True)
class PostOut(BaseModel):
    post:Post
    votes:int
    model_config = ConfigDict(from_attributes=True)
class CreateUser(BaseModel):
    email:EmailStr
    password:str

class UserLogin(BaseModel):
    email:EmailStr
    password:str
class Token(BaseModel):
    access_token:str
    token_type:str
class TokenData(BaseModel):
    id:Optional[int]=None
class Vote(BaseModel):
    post_id:int
    dir:conint(le=1)
