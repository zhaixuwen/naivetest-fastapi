from fastapi import APIRouter, Depends, HTTPException, Body, Request
from typing import List, Optional, Union
from sqlalchemy.orm import Session
from utils import get_db
from . import schemas
from . import crud
from apitest.jsontools import resp_200, resp_400
from fastapi.encoders import jsonable_encoder

router = APIRouter()


@router.post('/', response_model=schemas.Interface)
def create_interface(request: Request, interface: schemas.InterfaceCreate, db: Session = Depends(get_db)):
    db_interface = crud.get_interface_by_name(db, interface.name)
    if db_interface:
        raise HTTPException(status_code=400, detail="Interface already created, please change name")
    user_id = int(request.headers.get('user_id'))
    return resp_200(
        data=jsonable_encoder(
            crud.create_interface(db=db, interface=interface, created_by=user_id, last_updated_by=user_id)
        ),
        db=db
    )


@router.put('/{interface_id}')
def update_interface(request: Request, interface_id: int, interface: schemas.InterfaceCreate,
                     db: Session = Depends(get_db)):
    user_id = int(request.headers.get('user_id'))
    db_interface = crud.update_interface(db, interface_id, interface, user_id)
    return resp_200(
        data=jsonable_encoder(db_interface),
        db=db
    )


@router.get('/', response_model=List[schemas.Interface])
def read_interfaces(skip: int = 0, limit: int = 100, text: str = '', db: Session = Depends(get_db)):
    if text:
        interfaces = crud.get_interfaces_by_text(text, db)
    else:
        interfaces = crud.get_interfaces(db, skip, limit)
    return resp_200(
        data=jsonable_encoder(interfaces),
        count=len(interfaces),
        db=db
    )


@router.get('/{interface_id}', response_model=schemas.Interface)
def read_interface(interface_id: int, db: Session = Depends(get_db)):
    interface = crud.get_interface(db, interface_id)
    return resp_200(
        data=jsonable_encoder(interface),
        db=db
    )


@router.delete('/{interface_id}')
def delete_interface(interface_id: int, db: Session = Depends(get_db)):
    db_interface = crud.get_interface(db, interface_id)
    if not db_interface:
        return resp_400(message='Delete failed, error interface id')
    crud.delete_interface(db, db_interface.id)
