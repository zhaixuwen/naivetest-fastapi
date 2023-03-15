from fastapi import APIRouter, Depends, HTTPException, Body, Request
from typing import List, Optional, Union
from sqlalchemy.orm import Session
from utils import get_db
from . import schemas
from . import crud
from apitest.jsontools import resp_200, resp_400
from fastapi.encoders import jsonable_encoder

router = APIRouter()


@router.post("/", response_model=schemas.ExecuteAccount)
def create_execute_account(request: Request, execute_account: schemas.ExecuteAccountCreate,
                           db: Session = Depends(get_db)):
    db_execute_account = crud.get_execute_account_by_code(db, execute_account_code=execute_account.code)
    if db_execute_account:
        raise HTTPException(status_code=400, detail="Execute account already created, please change code.")
    user_id = int(request.headers.get('user_id'))
    return resp_200(
        data=jsonable_encoder(crud.create_execute_account(db=db, execute_account=execute_account, created_by=user_id,
                                                          last_updated_by=user_id)),
        db=db
    )


@router.put("/{execute_account_id}", response_model=schemas.ExecuteAccount)
def update_execute_account(request: Request, execute_account_id: int, execute_account: schemas.ExecuteAccountCreate,
                           db: Session = Depends(get_db)):
    user_id = int(request.headers.get('user_id'))
    db_execute_account = crud.update_execute_account_by_id(db, execute_account_id, execute_account, user_id)
    return resp_200(
        data=jsonable_encoder(db_execute_account),
        db=db
    )


@router.get("/", response_model=List[schemas.ExecuteAccount])
def read_execute_accounts(skip: int = 0, limit: int = 100, text: str = '', db: Session = Depends(get_db)):
    if text:
        execute_accounts = crud.get_execute_accounts_by_text(text, db, skip, limit)
    else:
        execute_accounts = crud.get_execute_accounts(db, skip, limit)
    return resp_200(
        data=jsonable_encoder(execute_accounts),
        count=len(execute_accounts),
        db=db
    )


@router.get("/{execute_account_id}", response_model=schemas.ExecuteAccount)
def read_execute_account_by_id(execute_account_id: int, db: Session = Depends(get_db)):
    execute_account = crud.get_execute_account_by_id(db, execute_account_id)
    return resp_200(
        data=jsonable_encoder(execute_account),
        db=db
    )


@router.delete("/{execute_account_id}")
def delete_execute_account(execute_account_id: int, db: Session = Depends(get_db)):
    db_execute_account = crud.get_execute_account_by_id(db, execute_account_id)
    if not db_execute_account:
        return resp_400(message='Delete failed, error execute account id')
    crud.delete_execute_account(db, db_execute_account.id)
