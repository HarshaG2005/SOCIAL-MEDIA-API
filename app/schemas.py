from pydantic import BaseModel,Field,ConfigDict,EmailStr,conint
from pydantic import field_validator
from typing import Optional
from datetime import datetime
############################SCHEMA_DEFINITIONS##############################################################
# Schemas for request and response models

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

    @field_validator('password')
    def password_length(cls,v):
        if len(v)<6:
            raise ValueError('password must be at least 6 characters long')
        return v

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
