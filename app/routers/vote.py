from fastapi import (
    APIRouter,
    Depends,
    FastAPI,
    HTTPException,
    Request,
    Response,
    status,
)
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

import app.databases
import app.models
import app.oauth2
import app.schemas
from app.rate_limiter import limiter

router = APIRouter(prefix="/vote", tags=["Vote"])


@router.post("/", status_code=status.HTTP_201_CREATED)
@limiter.limit("20/minute")
async def vote(
    request: Request,
    vote: app.schemas.Vote,
    db: Session = Depends(app.databases.get_db),
    current_user: int = Depends(app.oauth2.get_current_user),
) -> dict:
    """Cast or remove a vote on a post.
        Rate Limit: 10 requests per minute
    Args:
        vote: Vote data containing post_id and direction
        db: Database session
        current_user: Authenticated user
    Returns:
        A message indicating the result of the vote operation

    """
    try:
        vote_query = db.query(app.models.Vote).filter(
            app.models.Vote.post_id == vote.post_id,
            app.models.Vote.user_id == current_user.id,
        )
        found_vote = vote_query.first()
        if vote.dir == 1:
            if found_vote:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"user:{current_user.id} has already voted on post {vote.post_id}",
                )
            new_vote = app.models.Vote(post_id=vote.post_id, user_id=current_user.id)
            db.add(new_vote)
            db.commit()
            return {"message": "Successfully Voted"}
        else:
            if not found_vote:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Vote doesnt exist"
                )
            vote_query.delete(synchronize_session=False)
            db.commit()
            return {"message": f"Successfully removed vote for post:{vote.post_id}"}
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
    except Exception as e:
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
