from fastapi import APIRouter, Depends, HTTPException, Body
from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
from werkzeug.security import check_password_hash
from fastapi.encoders import jsonable_encoder
from utils import get_db
from . import schemas
from . import crud
from apitest.jsontools import resp_200

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='xxx')

SECRET_KEY = "e56d96086dac41ff9f0a5fb241c4d931ce9015e00f674709a102cf8f89cc8da6"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 720


@router.post("/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@router.get("/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # 读取指定数量用户
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@router.get('/{user_id}', response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id)
    return user


@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id)
    if not db_user:
        return {"resMsg": "Delete failed, error user id"}
    crud.delete_user(db, db_user.id)


def _create_jwt_token(data: dict, expire_delta: Optional[timedelta] = None):
    expire = datetime.utcnow() + expire_delta if expire_delta else datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data.update({'exp': expire})
    token = jwt.encode(claims=data, key=SECRET_KEY, algorithm=ALGORITHM)
    return token


@router.post('/login')
async def login(email: str = Body(...), password: str = Body(...), db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email)
    if not db_user:
        raise HTTPException(status_code=400, detail="Error email address")
    if not check_password_hash(db_user.hashed_password, password):
        raise HTTPException(status_code=400, detail="Error login password")
    data = {'user_id': db_user.id}
    token = _create_jwt_token(data)
    return {'access_token': token}


def oauth_token(token: str = Depends(oauth2_scheme)):
    user_id = 0
    try:
        payload = jwt.decode(token=token, key=SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get('user_id')
    except JWTError as e:
        print(f'认证异常: {e}')
    finally:
        return user_id
