import logging

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from typing import List, Dict
from utils import get_db
from . import schemas
from . import crud
from apitest.common.req import testcase_request
from apitest.jsontools import resp_200, resp_400
from fastapi.encoders import jsonable_encoder
from apitest.testcase import crud as case_crud
from apitest import models

router = APIRouter()


@router.post('/', response_model=schemas.Testcase)
def create_testcase(request: Request, testcase: Dict, db: Session = Depends(get_db)):
    # 处理前端header
    if type(testcase.get('header')) == list:
        new_head = input_headers(testcase.get('header'))
        testcase['header'] = new_head
    testcase = schemas.TestcaseCreate(**testcase)

    db_testcase = crud.get_testcase_by_title(db, testcase.title)
    if db_testcase:
        raise HTTPException(status_code=400, detail="Testcase already created, please change title")
    user_id = int(request.headers.get('user_id'))
    return resp_200(
        data=jsonable_encoder(
            crud.create_testcase(db=db, testcase=testcase, created_by=user_id, last_updated_by=user_id)),
        db=db
    )


@router.put('/{testcase_id}', response_model=schemas.Testcase)
def update_testcase(request: Request, testcase_id: int, testcase: Dict, db: Session = Depends(get_db)):
    # 处理前端header
    if type(testcase.get('header')) == list:
        new_head = input_headers(testcase.get('header'))
        testcase['header'] = new_head
    testcase = schemas.TestcaseCreate(**testcase)
    user_id = int(request.headers.get('user_id'))
    db_testcase = crud.update_testcase(db, testcase_id, testcase, user_id)
    print(jsonable_encoder(db_testcase))
    return resp_200(
        data=jsonable_encoder(db_testcase),
        db=db
    )


@router.get('/', response_model=List[schemas.Testcase])
def read_testcases(skip: int = 0, limit: int = 100, text: str = '', db: Session = Depends(get_db)):
    if text:
        testcases = crud.get_testcases_by_text(db, text)
    else:
        testcases = crud.get_testcases(db, skip, limit)
    return resp_200(
        data=jsonable_encoder(testcases),
        count=len(testcases),
        db=db
    )


@router.get('/interface/{interface_id}', response_model=List[schemas.Testcase])
def read_testcases_by_interface(interface_id: int, db: Session = Depends(get_db)):
    testcases = crud.get_testcases_by_interface(db, interface_id)
    return resp_200(
        data=jsonable_encoder(testcases),
        count=len(testcases),
        db=db
    )


@router.get('/env/{env_id}', response_model=List[schemas.Testcase])
def read_testcases_by_env(env_id: int, db: Session = Depends(get_db)):
    testcases = crud.get_testcases_by_env(db, env_id)
    return resp_200(
        data=jsonable_encoder(testcases),
        count=len(testcases),
        db=db
    )


@router.get('/{testcase_id}')
def read_testcase_by_id(testcase_id: int, db: Session = Depends(get_db)):
    testcase = crud.get_testcase(db, testcase_id)
    return resp_200(
        data=jsonable_encoder(testcase),
        db=db
    )


@router.delete('/{testcase_id}')
def delete_testcase(testcase_id: int, db: Session = Depends(get_db)):
    db_testcase = crud.get_testcase(db, testcase_id)
    if not db_testcase:
        return resp_400(message='Delete failed, error testcase id')
    crud.delete_testcase(db, db_testcase.id)


@router.post('/debug')
async def debug_testcase(testcase: schemas.TestcaseCreate, req: Request, db: Session = Depends(get_db)):
    case = jsonable_encoder(testcase)
    redis = await req.app.state.redis
    r = await testcase_request(case=case, db=db, redis=redis)
    return resp_200(data=r)


@router.post('/request')
async def request_testcase(item: Dict, req: Request, db: Session = Depends(get_db)):
    case = crud.get_testcase(db, item.get('testcase_id'))
    redis = await req.app.state.redis
    user_id = int(req.headers.get('user_id'))
    r = await testcase_request(case=jsonable_encoder(case), db=db, redis=redis)
    case_crud.create_testcase_log(db, models.TestcaseLog(testcase_id=case.id, detail=r), user_id)
    return resp_200(data=r)


@router.get('/logs/{testcase_id}')
def get_testcase_log(testcase_id: int, db: Session = Depends(get_db)):
    logs = crud.read_testcase_log(db, testcase_id)
    return resp_200(data=jsonable_encoder(logs), db=db)


def input_headers(header_list: list):
    header_dict = {}
    for head in header_list:
        header_dict[head['name']] = head['value']
    return header_dict
