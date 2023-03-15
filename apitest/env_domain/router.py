from fastapi import APIRouter, Depends, HTTPException, Body, Request
from typing import List, Optional, Union
from sqlalchemy.orm import Session
from utils import get_db
from . import schemas
from . import crud
from apitest.jsontools import resp_200, resp_400
from fastapi.encoders import jsonable_encoder

router = APIRouter()


@router.post("/", response_model=schemas.EnvDomain)
def create_env_domain(request: Request, env_domain: schemas.EnvDomainCreate, db: Session = Depends(get_db)):
    db_env_domain = crud.get_env_domain_by_code(db, env_domain_code=env_domain.code)
    if db_env_domain:
        raise HTTPException(status_code=400, detail="Env domain already created, please change code.")
    user_id = int(request.headers.get('user_id'))
    return resp_200(
        data=jsonable_encoder(
            crud.create_env_domain(db=db, env_domain=env_domain, created_by=user_id, last_updated_by=user_id)),
        db=db
    )


@router.put("/{env_domain_id}", response_model=schemas.EnvDomain)
def update_env_domain(request: Request, env_domain_id: int, env_domain: schemas.EnvDomainCreate,
                      db: Session = Depends(get_db)):
    user_id = int(request.headers.get('user_id'))
    db_env_domain = crud.update_env_domain_by_id(db, env_domain_id, env_domain, user_id)
    return resp_200(
        data=jsonable_encoder(db_env_domain),
        db=db
    )


@router.get("/", response_model=List[schemas.EnvDomain])
def read_env_domains(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), text: str = ''):
    if text:
        env_domains = crud.get_env_domains_by_text(text, db, skip, limit)
    else:
        env_domains = crud.get_env_domains(db, skip, limit)
    return resp_200(
        data=jsonable_encoder(env_domains),
        count=len(env_domains),
        db=db
    )


@router.get("/{env_domain_id}", response_model=schemas.EnvDomain)
def read_env_domain(env_domain_id: int, db: Session = Depends(get_db)):
    env_domains = crud.get_env_domain(db, env_domain_id)
    return resp_200(
        data=jsonable_encoder(env_domains),
        db=db
    )


@router.delete("/{env_domain_id}")
def delete_env_domain(env_domain_id: int, db: Session = Depends(get_db)):
    db_env_domain = crud.get_env_domain(db, env_domain_id)
    if not db_env_domain:
        return resp_400(message='Delete failed, error env domain id')
    crud.delete_env_domain(db, db_env_domain.id)
