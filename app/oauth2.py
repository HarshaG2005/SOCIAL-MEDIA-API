from jose import JWTError,jwt
from datetime import datetime,timedelta
from sqlalchemy.orm import Session
from databases import get_db
from fastapi import HTTPException,status,Depends
from schemas import TokenData
from fastapi.security import OAuth2PasswordBearer
from config import settings
import models
ACCESS_TOKEN_EXPIRE_MINUTES=settings.access_token_expire_minutes
ALGORITHM=settings.algorithm
SECRET_KEY=settings.secret_key
oauth2_scheme=OAuth2PasswordBearer(tokenUrl='login')
def create_access_token(data:dict):
    to_encode=data.copy()
    expire=datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    encoded_jwt=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt
def verify_access_token(token:str,credentials_exception):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        id:str=payload.get("user_id")
        print(id)
        if id is None:
            raise credentials_exception
        id_=int(id)
        token_data=TokenData(id=id_)
        return token_data
    except JWTError:
        raise credentials_exception
def get_current_user(token:str=Depends(oauth2_scheme),db: Session = Depends(get_db)):
    credentials_exception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Could not validate credentials",headers={"WWW-Authenticate":"Bearer"})
    token=verify_access_token(token,credentials_exception)
    current_user = db.query(models.User).filter(models.User.id == token.id).first()
    if current_user is None:
        raise credentials_exception
    return current_user

