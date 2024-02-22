from datetime import timedelta, datetime
from typing import Annotated, Optional
from fastapi import APIRouter, Depends, Request, Form, Response,  HTTPException
from pydantic import BaseModel
from db.database import SessionLocal
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from models import User, UserRole, Role
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt



router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

SECRET_KEY = '75094b6ffcb1b8193089c66704421b731e3bc35356277f0b717b6da672692504'
ALGORITHM = 'HS256'

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")

class LoginForm:
    def __init__(self, request: Request):
        self.request = request
        self.username: Optional[str] = None
        self.password: Optional[str] = None

    async def create_oauth_form(self):
        form = await self.request.form()
        self.username = form.get('username')
        self.password = form.get('password')


class Token(BaseModel):
    access_token: str
    token_type: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


def authenticate_user(username: str, password: str, db):
    
    result = db.query(User, Role)\
        .outerjoin(UserRole, User.id == UserRole.id_user)\
        .outerjoin(Role, UserRole.id_role == Role.id)\
        .filter(User.username == username)\
        .first()
    
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user, role = result

    if not user or not bcrypt_context.verify(password, user.hashed_password):
       
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user, role


def create_access_token(username: str, user_id: int, role: str, expires_delta: timedelta):
    encode = {'sub': username, 'id': user_id, 'role': role}
    expires = datetime.utcnow() + expires_delta
    encode.update({'exp': expires})
    encoded_jwt = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(request: Request):
    try:
        token = request.headers.get('access_token')
        if token is None:
            return None
        try:
            print(token)
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            print(payload)
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        except jwt.DecodeError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Error decoding token")
        
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        user_role: str = payload.get('role')

        # if username is None or user_id is None:
        #     logout(request)
        return {'username': username, 'id': user_id, 'role': user_role}
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")



@router.post("/token", response_model=Token , status_code=status.HTTP_200_OK)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 db: db_dependency):
    try:
        user, role = authenticate_user(form_data.username, form_data.password, db)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    
    try:
        token = create_access_token(user.username, user.id, role.name, timedelta(minutes=60))
    except Exception:
       raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return token


@router.post("/")
async def login(request: Request, 
                db: Session = Depends(get_db)):
    try:
        form = LoginForm(request)
        await form.create_oauth_form()

        validate_user_cookie = await login_for_access_token(form_data=form, db=db)
        

        return validate_user_cookie
    except HTTPException as e:
        return Response(status_code=e.status_code, content=e.detail)
    except Exception:
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content="Internal Server Error")
    

@router.post("/register")
async def register_user(request: Request, 
                        email: str = Form(...),
                        username: str = Form(...),
                        first_name: str = Form(...),
                        last_name: str = Form(...),
                        hashed_password: str = Form(...),
                        password: str = Form(...),
                        db: Session = Depends(get_db)):

    validation1 = db.query(User).filter(User.username == username).first()
    validation2 = db.query(User).filter(User.email == email).first()

    if hashed_password != password or validation1 is not None or validation2 is not None:
        msg = "Invalid registration request"
        return {"error": msg}
    
    user_model = User()
    user_model.username = username
    user_model.email = email
    user_model.first_name = first_name
    user_model.last_name = last_name
    user_model.country_id = 1
    user_model.region_id = 1
    user_model.city_id = 1
    user_model.phone_number = "0000000000"
    user_model.hashed_password = bcrypt_context.hash(hashed_password)
    user_model.is_active = True

    db.add(user_model)
    db.commit()

    msg = "Register successfully"
    return {"message": msg}
    

@router.post("/me")
async def get_user(request: Request, 
                   db: Session = Depends(get_db)):
    try:
        user = await get_current_user(request)

        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
        return user
    except HTTPException as e:
        return Response(status_code=e.status_code, content=e.detail)
    except Exception:
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content="Internal Server Error")