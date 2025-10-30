from fastapi import FastAPI,HTTPException,Depends,status,Request
import time
import app.models 
import app.utils
from app.schemas import CreatePost,Post,User,CreateUser
from app.databases import engine,SessionLocal
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.routers import post,user,auth,vote
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
############################INITIALIZING_SETUP###################################################################################################
app.models.Base.metadata.create_all(bind=engine)
app=FastAPI()
#  ADD RATE LIMITER
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
# INCLUDE ROUTERS
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)
origins = ['*']
    
# ADD CORS MIDDLEWARE
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

