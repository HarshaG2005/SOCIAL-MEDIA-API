from fastapi import FastAPI,HTTPException,Depends,status
import time
import models 
import utils
from schemas import CreatePost,Post,User,CreateUser
from databases import engine,SessionLocal
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from routers import post,user,auth,vote
from fastapi.middleware.cors import CORSMiddleware






############################INITIALIZING_SETUP###################################################################################################
models.Base.metadata.create_all(bind=engine)
app=FastAPI()
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)
origins = ['*']
    

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

