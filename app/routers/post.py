import models,oauth2
from routers import auth
from fastapi import FastAPI, HTTPException, Depends, status, APIRouter
from schemas import CreatePost, Post,TokenData,PostOut
from databases import get_db
from sqlalchemy.orm import Session
from typing import Optional
from sqlalchemy import func
router=APIRouter(prefix="/posts",
                   tags=["Posts"]
                              )
#####CREATE_POST####
@router.post("/",response_model=Post)
async def create_post(post:CreatePost,db:Session=Depends(get_db),current_user:TokenData=Depends(oauth2.get_current_user)):
    try:   
        new_post=models.Post(owner_id=current_user.id,**post.dict())
        db.add(new_post)
        db.commit()
        db.refresh(new_post)
        return new_post
         
    
    except Exception as e:
      db.rollback()
      raise HTTPException(status_code=500, detail="🛑🛑🛑"+str(e)+"🛑🛑🛑")

#######SELECT_ALL##############

@router.get('/',response_model=list[PostOut])
async def showall(db:Session=Depends(get_db),current_user:TokenData=Depends(oauth2.get_current_user),limit:int=10,skip:int=0,search:Optional[str]=""):
    try:
         #posts=db.query(models.Post).filter(models.Post.title.ilike(f"%{search}%")).limit(limit).offset(skip).all()
         results=db.query(models.Post,func.count(models.Vote.post_id)).join(models.Vote,models.Post.id==models.Vote.post_id,isouter=True).group_by(models.Post.id).filter(models.Post.title.ilike(f"%{search}%")).limit(limit).offset(skip).all()
         print(results)
         #return results
         return [{"post": post, "votes": votes} for post, votes in results]

        
    except Exception as e:
      db.rollback()
      raise HTTPException(status_code=500, detail="🛑🛑🛑"+str(e)+"🛑🛑🛑")

     
#######SELECT_BY_ID###########J
@router.get("/{id}",response_model=PostOut)
async def select(id:int,db:Session=Depends(get_db),current_user:TokenData=Depends(oauth2.get_current_user)):
    try:
        #post=db.query(models.Post).filter(models.Post.id==id).first()
        post_=db.query(models.Post,func.count(models.Vote.post_id)).join(models.Vote,models.Post.id==models.Vote.post_id,isouter=True).group_by(models.Post.id).filter(models.Post.id==id).first()
        if post_==None:
           raise HTTPException(status_code=404,detail='post not found😑😑😑')
        post,votes=post_
        return {'post':post,'votes':votes}
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500,detail="🛑🛑🛑"+str(e)+"🛑🛑🛑")   
##########UPDATING_POST##############
@router.put("/{id}")
async def update_post(id:int,updated:CreatePost,db:Session=Depends(get_db),current_user:TokenData=Depends(oauth2.get_current_user)):
  try:
    post_query=db.query(models.Post).filter(models.Post.id==id)
    post=post_query.first()
    if post==None:
        raise HTTPException(status_code=404,detail=f"post with id:{id} does not exist!⚠⚠⚠")
    if post.owner_id != current_user.id:
      raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="NOT AUTHORIZED TO PERFORM REQUESTED ACTION🛑🛑🛑")
    post_query.update(updated.dict(),synchronize_session=False)
    db.commit()
    return {"new":post_query.first()}
  except Exception as e:
    db.rollback()
    raise HTTPException(status_code=500,detail="🛑🛑🛑"+str(e)+"🛑🛑🛑")
 ##############DELETE_POST################
@router.delete("/{id}")
async def delete_post(id:int,db:Session=Depends(get_db),current_user:TokenData=Depends(oauth2.get_current_user)):
  try:
    post_query=db.query(models.Post).filter(models.Post.id==id)
    post=post_query.first()
    if post==None:
        raise HTTPException(status_code=404,detail=f"post with id:{id} does not exist!🚫🚫🚫")
    if post.owner_id != current_user.id:
      raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform requested action🛑🛑🛑")
    post_query.delete(synchronize_session=False) 
    db.commit()
    return {"message":f"post with id:{id} got deleted😁😁😁"}
  except Exception as e:
    db.rollback()
    raise HTTPException(status_code=404,detail="🛑🛑🛑"+str(e)+"🛑🛑🛑")