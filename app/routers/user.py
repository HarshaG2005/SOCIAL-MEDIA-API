import  app.models
import app.utils
from fastapi import FastAPI, HTTPException, Depends, status, APIRouter
from app.schemas import CreateUser, User
from app.databases import engine, get_db
from sqlalchemy.exc import IntegrityError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
router=APIRouter(prefix="/users",
                   tags=["Users"])


###################################CREATING_USER####################
@router.post("/",status_code=status.HTTP_201_CREATED,response_model=User)
def create_user(user:CreateUser,db:Session=Depends(get_db))->User:
            """ Create a new user account.
            Args:
                user: User data for the new account
                db: Database session
            Returns:
                   The newly created user account

            """
            try:
                #hash the password
                hashed_password=app.utils.hash(user.password)
                user.password=hashed_password
                new_user=app.models.User(**user.model_dump())
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
            except SQLAlchemyError as e:
               db.rollback()
               raise HTTPException(status_code=500, detail=f'Database errror: {str(e)}')
#######################SELECT_USER_ACCOUNT############################
@router.get("/{id}",response_model=User)
def select_user(id:int,db:Session=Depends(get_db))->User:
  """ Retrieve a user account by its ID.
  Args:
      id: User ID
      db: Database session
  Returns:
          The user account associated with the given ID
  """
  try:
     post=(
      db.query(app.models.User)
      .filter(app.models.User.id==id)
      .first())
     if post==None:
      raise HTTPException(status_code=404,detail=f"Cant find user related to id:{id}")
     return post
  except Exception as e:
    raise
  except Exception as e:
    
    raise HTTPException(status_code=500,detail=str(e))
  except SQLAlchemyError as e:
     raise HTTPException(status_code=500, detail=f'Database error: {str(e)}')
