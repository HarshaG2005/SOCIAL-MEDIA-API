import  models
import utils
from fastapi import FastAPI, HTTPException, Depends, status, APIRouter
from schemas import CreateUser, User
from databases import engine, get_db
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
router=APIRouter(prefix="/users",
                   tags=["Users"])


###################################CREATING_USER######################################################################
@router.post("/",status_code=status.HTTP_201_CREATED,response_model=User)
def create_user(user:CreateUser,db:Session=Depends(get_db)):
            try:
                #hash the password
                hashed_password=utils.hash(user.password)
                user.password=hashed_password
                new_user=models.User(**user.model_dump())
                db.add(new_user)
                db.commit()
                db.refresh(new_user)
                return new_user
            except IntegrityError:
                    db.rollback()
                    raise HTTPException(
                           status_code=status.HTTP_400_BAD_REQUEST,
                           detail="User with that email already exists."
                                     )
            except Exception as e:
                
                raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
#######################SELECT_USER_ACCOUNT########################################################################################
@router.get("/{id}",response_model=User)
def select_user(id:int,db:Session=Depends(get_db)):
  try:
     post=db.query(models.User).filter(models.User.id==id).first()
     if post==None:
      raise HTTPException(status_code=404,detail=f"Cant find user related to id:{id}")
     return post
  except Exception as e:
    
    raise HTTPException(status_code=500,detail=str(e))
#################################################################################################################
