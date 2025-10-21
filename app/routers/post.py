import app.models,app.oauth2
from app.routers import auth
from fastapi import FastAPI, HTTPException, Depends, status, APIRouter
from app.schemas import CreatePost, Post,TokenData,PostOut
from app.databases import get_db
from sqlalchemy.orm import Session
from typing import Optional
from sqlalchemy import func
router=APIRouter(prefix="/posts",
                   tags=["Posts"]
                              )
#####CREATE_POST####
@router.post("/",response_model=Post)
def create_post(post:CreatePost,
                db:Session=Depends(get_db),
                current_user:TokenData=Depends(app.oauth2.get_current_user))->{str,Post}:
    """  Create a new post.
    Args:
        post:Post data
        db: Database session
        current_user: Authenticated user
    Returns:
        The newly created post

    """
    try:   
        new_post=app.models.Post(owner_id=current_user.id,**post.dict())
        db.add(new_post)
        db.commit()
        db.refresh(new_post)
        return new_post
    except SQLAlchemyError as e:
      db.rollback()
      raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))
    
    except Exception as e:
      db.rollback()
      raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred")

#######SELECT_ALL##############

@router.get('/',response_model=list[PostOut])
def get_all_posts(db:Session=Depends(get_db),
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
           results=db.query(app.models.Post,func.count(app.models.Vote.post_id)).join(app.models.Vote,app.models.Post.id==app.models.Vote.post_id,isouter=True).group_by(app.models.Post.id).filter(app.models.Post.title.ilike(f"%{search}%")).limit(limit).offset(skip).all()
         
         #return results
           return [{"post": post, "votes": votes} for post, votes in results]

        
        except SQLAlchemyError as e:
         db.rollback()
         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))
    
        except Exception as e:
         db.rollback()
         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred")

     
#######SELECT_BY_ID###########
@router.get("/{id}",response_model=PostOut)
def select(id:int,db:Session=Depends(get_db),
           current_user:TokenData=Depends(app.oauth2.get_current_user))->{str,PostOut}:
    """  Retrieve a post by its ID.
    Args:
        id : Post ID
        db: Database session
        current_user: Authenticated user
    Returns:
        The post with its vote count
    """
    try:
        #post=db.query(models.Post).filter(models.Post.id==id).first()
        post_=db.query(app.models.Post,func.count(app.models.Vote.post_id)).join(app.models.Vote,app.models.Post.id==app.models.Vote.post_id,isouter=True).group_by(app.models.Post.id).filter(app.models.Post.id==id).first()
        if post_==None:
           raise HTTPException(status_code=404,detail='post not found')
        post,votes=post_
        return {'post':post,'votes':votes}
        
    except SQLAlchemyError as e:
      db.rollback()
      raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))
    
    except Exception as e:
      db.rollback()
      raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred")
   
##########UPDATING_POST##############
@router.put("/{id}")
def update_post(id:int,
                updated:CreatePost,
                db:Session=Depends(get_db),
                current_user:TokenData=Depends(app.oauth2.get_current_user))->dict[str,Post]:
  """  Update a post by its ID
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
    post_query.update(updated.dict(),synchronize_session=False)
    db.commit()
    return {"new":post_query.first()}
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
    post_query=db.query(app.models.Post).filter(app.models.Post.id==id)
    post=post_query.first()
    if post==None:
        raise HTTPException(status_code=404,detail=f"post with id:{id} does not exist!")
    if post.owner_id != current_user.id:
      raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform requested action")
    post_query.delete(synchronize_session=False) 
    db.commit()
    return {"message":f"post with id:{id} got deleted"}
  except SQLAlchemyError as e:
      db.rollback()
      raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))
    
  except Exception as e:
      db.rollback()
      raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred")
