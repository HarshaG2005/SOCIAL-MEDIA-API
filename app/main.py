from fastapi import FastAPI,HTTPException,Depends,status
import time
import app.models 
import app.utils
from app.schemas import CreatePost,Post,User,CreateUser
from app.databases import engine,SessionLocal
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.routers import post,user,auth,vote
from fastapi.middleware.cors import CORSMiddleware






############################INITIALIZING_SETUP###################################################################################################
app.models.Base.metadata.create_all(bind=engine)
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

@app.get("/health")
def health_check():
    return {"status": "healthy"}

