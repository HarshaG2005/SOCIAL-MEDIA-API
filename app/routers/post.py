import app.models,app.oauth2
from sqlalchemy import func
from app.routers import auth
from fastapi import FastAPI, HTTPException, Depends, status, APIRouter,Query,Request
from app.schemas import CreatePost, Post,TokenData,PostOut
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError  
from app.databases import get_db
from slowapi import Limiter  
from slowapi.util import get_remote_address
from typing import Optional


router=APIRouter(prefix="/posts",
                   tags=["Posts"]
                              )
limiter = Limiter(key_func=get_remote_address)
#####CREATE_POST####
@router.post("/",response_model=Post)
@limiter.limit("10/minute")
def create_post(request: Request,
                post:CreatePost,
                db:Session=Depends(get_db),
                current_user:TokenData=Depends(app.oauth2.get_current_user))->Post:
    """  Create a new post.
         Rate Limit: 10 requests per minute
    Args:
        post:Post data
        db: Database session
        current_user: Authenticated user
    Returns:
        The newly created post

    """
    try:   
        new_post=app.models.Post(owner_id=current_user.id,**post.model_dump())
        db.add(new_post)
        db.commit()
        db.refresh(new_post)
        return new_post
    except HTTPException:
        raise
    except SQLAlchemyError as e:
      db.rollback()
      raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))
    
    except Exception as e:
      db.rollback()
      raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred")

#######SELECT_ALL##############

@router.get('/',response_model=list[PostOut])
def get_all_posts(request: Request,
        db:Session=Depends(get_db),
        current_user:TokenData=Depends(app.oauth2.get_current_user),
        limit:int=Query(default=10, ge=1, le=100),
        skip:int=Query(default=0,ge=0),
        search:Optional[str]="")->list[PostOut]:
        """
        Retrieve all posts with vote counts.
        
        Args:
        db: Database session
        current_user: Authenticated user
        limit: Maximum number of posts to return
        skip: Number of posts to skip (pagination)
        search: Search term to filter posts by title
    
        Returns:
          List of posts with vote counts
       """
        try:
         #posts=db.query(models.Post).filter(models.Post.title.ilike(f"%{search}%")).limit(limit).offset(skip).all()
           results=(
            db.query(app.models.Post,func.count(app.models.Vote.post_id))
            .join(
              app.models.Vote,
              app.models.Post.id==app.models.Vote.post_id,
              isouter=True
            )
            .group_by(app.models.Post.id)
            .filter(app.models.Post.title.ilike(f"%{search}%"))
            .limit(limit)
            .offset(skip)
            .all()
           )

         #return results
           return [{"post": post, "votes": votes} for post, votes in results]

        except HTTPException:
          raise
        except SQLAlchemyError as e:
         db.rollback()
         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))
    
        except Exception as e:
         db.rollback()
         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred")

     
#######SELECT_BY_ID###########
@router.get("/{id}",response_model=PostOut)
def select_post_by_id(
                      id:int,
                      db:Session=Depends(get_db),
                      current_user:TokenData=Depends(app.oauth2.get_current_user))->PostOut:
    """  Retrieve a post by its ID.
    Args:
        id : Post ID
        db: Database session
        current_user: Authenticated user
    Returns:
        The post with its vote count
    """
    try:
        post_query = db.query(app.models.Post).filter(app.models.Post.id == id).first()
        if not post_query:
            
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} not found")
        post_=(
          db.query(app.models.Post,func.count(app.models.Vote.post_id))
          .join(
            app.models.Vote,
            app.models.Post.id==app.models.Vote.post_id,
            isouter=True
          )
          .group_by(app.models.Post.id)
          .filter(app.models.Post.id==id)
          .first()
          )
        
        if post_ is None:
           raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='post not found')
        post,votes=post_
        return {'post':post,'votes':votes}
    except HTTPException:
        # Re-raise HTTPException as-is (don't catch and convert to 500!)
        raise
    except SQLAlchemyError as e:
      db.rollback()
      raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))
    
    except Exception as e:
      db.rollback()
      raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred")
   
##########UPDATING_POST##############
@router.put("/{id}")
@limiter.limit("5/minute")
def update_post(request: Request,
                id:int,
                updated:CreatePost,
                db:Session=Depends(get_db),
                current_user:TokenData=Depends(app.oauth2.get_current_user))->dict[str,Post]:
  """  Update a post by its ID
      Rate Limit: 5 requests per minute
    Args:
        id : Post ID
        updated: Updated post data
        db : database session
        current user: Authenticated user
      Returns:
        The updated post
  """
  try:
    post_query=db.query(app.models.Post).filter(app.models.Post.id==id)
    post=post_query.first()
    if post==None:
        raise HTTPException(status_code=404,detail=f"post with id:{id} does not exist!")
    if post.owner_id != current_user.id:
      raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="NOT AUTHORIZED TO PERFORM REQUESTED ACTION")
    post_query.update(updated.model_dump(),synchronize_session=False)
    db.commit()
    return {"new":post_query.first()}
  except HTTPException:
      raise
  except SQLAlchemyError as e:
      db.rollback()
      raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))
    
  except Exception as e:
      db.rollback()
      raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred")

 ##############DELETE_POST################
@router.delete("/{id}")
def delete_post(id:int,db:Session=Depends(get_db),
                current_user:TokenData=Depends(app.oauth2.get_current_user))->dict[str,str]:
  """ Delete a post by its ID
    Args:
        id : Post ID
        db : database session 
        current user : Authenticated user
    Returns:
         A message confirming deletion
  """
  try:
    post_query=(
      db.query(app.models.Post)
      .filter(app.models.Post.id==id)
    )
    post=post_query.first()
    if post==None:
        raise HTTPException(status_code=404,detail=f"post with id:{id} does not exist!")
    if post.owner_id != current_user.id:
      raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform requested action")
    post_query.delete(synchronize_session=False) 
    db.commit()
    return {"message":"post deleted successfully"}
  except HTTPException:
      raise
  except SQLAlchemyError as e:
      db.rollback()
      raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))
    
  except Exception as e:
      db.rollback()
      raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred")
