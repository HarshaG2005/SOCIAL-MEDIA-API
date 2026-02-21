from fastapi import APIRouter, Depends, FastAPI, HTTPException, Request, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
import app.models
from app.databases import get_db
from app.oauth2 import create_access_token
from app.schemas import Token, UserLogin
from app.utils import verify
from app.rate_limiter import limiter
router = APIRouter(tags=["Authentication"])

@router.post("/login", response_model=Token)
@limiter.limit("5/minute")  # Rate limit: 5 requests per minute
async def login(
    request: Request,
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
) -> Token:
    """Authenticate a user and generate an access token.
         Rate Limit: 5 requests per minute
    Args:
          request: HTTP request object
          user_credentials: User login credentials
          db: Database session
    Returns:
             Access token and token type
    """
    try:
        user = (
            db.query(app.models.User)
            .filter(app.models.User.email == user_credentials.username)
            .first()
        )
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        if not verify(user_credentials.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials"
            )
        access_token = create_access_token(data={"user_id": user.id})
        return {"access_token": access_token, "token_type": "bearer"}
    except HTTPException :
        raise 
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
