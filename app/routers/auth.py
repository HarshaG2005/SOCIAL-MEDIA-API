from fastapi import FastAPI, HTTPException, Depends, status, APIRouter
from app.databases import get_db
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import app.models
from app.schemas import UserLogin,Token
from app.utils import verify
from app.oauth2 import create_access_token
router=APIRouter(
    tags=["Authentication"]
)
@router.post("/login",response_model=Token)
def login(user_credentials:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
   try:
       user=db.query(app.models.User).filter(app.models.User.email==user_credentials.username).first()
       if not user:
               raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
       if not verify(user_credentials.password,user.password):
               raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid Credentials")
       access_token=create_access_token(data={"user_id":user.id})
       return {"access_token":access_token,"token_type":"bearer"}
   except Exception as e:
        
        raise HTTPException(status_code=500, detail=str(e))