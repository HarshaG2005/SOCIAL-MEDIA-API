from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
import app.schemas,app.databases,app.models,app.oauth2
from sqlalchemy.orm import Session
router=APIRouter(
    prefix='/vote',
    tags=['Vote']
)
@router.post('/',status_code=status.HTTP_201_CREATED)
def vote(vote:app.schemas.Vote,db:Session=Depends(app.databases.get_db),current_user:int=Depends(app.oauth2.get_current_user)):
    vote_query=db.query(app.models.Vote).filter(app.models.Vote.post_id==vote.post_id,app.models.Vote.user_id==current_user.id)
    found_vote=vote_query.first()
    if (vote.dir==1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"user:{current_user.id} has already voted on post {vote.post_id}")
        new_vote=app.models.Vote(post_id=vote.post_id,user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message":"Successfully Voted"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Vote doesnt exist")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message":f"Successfully removed vote for post:{vote.post_id}"}
    
