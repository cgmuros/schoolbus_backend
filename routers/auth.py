from datetime import timedelta, datetime
from typing import Annotated, Optional
from fastapi import APIRouter, Depends, HTTPException, Request, Response, Form
from pydantic import BaseModel
from db.database import SessionLocal
# from passlib.context import CryptContext
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
# from jose import JWTError, jwt
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@router.get("/")
async def test(db: db_dependency):
    return {"message": "Hello World"}
