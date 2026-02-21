from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import app.models
import app.oauth2
from app.database import get_db
from app.schemas import CartCreate, CartUpdate

router = APIRouter(prefix="/cart", tags=["Cart"])
