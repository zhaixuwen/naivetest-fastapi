import asyncio
from typing import Dict
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from utils import get_db
from . import schemas
from . import crud
from user import crud as user_crud
from apitest.testcase import crud as case_crud
from apitest.jsontools import resp_200, resp_400
from fastapi.encoders import jsonable_encoder
from apitest.common.req import testsuite_request

router = APIRouter()


@router.post('/', response_model=schemas.Testsuite)
def create_testcase(request: Request, testsuite: schemas.TestsuiteCreate, db: Session = Depends(get_db)):
    db_testsuite = crud.get_testsuite_by_name(db, testsuite.name)
    if db_testsuite:
        raise HTTPException(status_code=400, detail="Testsuite already created, please change name")
    user_id = int(request.headers.get('user_id'))
    return resp_200(data=jsonable_encoder(
        crud.create_testsuite(db=db, testsuite=testsuite, created_by=user_id, last_updated_by=user_id)),
        db=db
    )


@router.put('/{testsuite_id}')
def update_testsuite(request: Request, testsuite_id: int, testsuite: schemas.TestsuiteCreate,
                     db: Session = Depends(get_db)):
    user_id = int(request.headers.get('user_id'))
    db_testsuite = crud.update_testsuite_by_id(db, testsuite_id, testsuite, user_id)
    return resp_200(
        data=jsonable_encoder(db_testsuite),
        db=db
    )


@router.get('/')
async def read_testsuites(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    testsuites = crud.get_testsuites(db, skip, limit)
    for suite in testsuites:
        if suite.is_active:
            suite.__setattr__('is_active_show', '启用')
        else:
            suite.__setattr__('is_active_show', '禁用')
        if suite.last_execute_status:
            suite.__setattr__('last_execute_status_show', '成功')
        else:
            suite.__setattr__('last_execute_status_show', '失败')

        members_vo = []
        for uid in suite.members:
            user = user_crud.get_user(db, uid)
            members_vo.append({
                'id': user.id,
                'email': user.email
            })
        suite.__setattr__('members_vo', members_vo)
        testcases_vo = []
        for cid in suite.testcases:
            case = case_crud.get_testcase(db, cid)
            if case:
                testcases_vo.append({
                    'id': case.id,
                    'title': case.title,
                    'description': case.description,
                    'env_id': case.env_id,
                    'execute_account_id': case.execute_account_id
                })
            else:
                suite.testcases.remove(cid)  # 如果用例不存在则删除
        suite.__setattr__('testcases_vo', testcases_vo)
    return resp_200(data=jsonable_encoder(testsuites), count=len(testsuites), db=db)


@router.get('/{testsuite_id}')
def read_testsuite_by_id(testsuite_id: int, db: Session = Depends(get_db)):
    db_testsuite = crud.get_testsuite(db, testsuite_id)
    return resp_200(data=jsonable_encoder(db_testsuite), db=db)


@router.delete('/{testsuite_id}')
def delete_testsuite(testsuite_id: int, db: Session = Depends(get_db)):
    db_testsuite = crud.get_testsuite(db, testsuite_id)
    if not db_testsuite:
        return resp_400(message='Delete failed, error testsuite id')
    crud.delete_testsuite(db, db_testsuite.id)


@router.post('/run')
async def run_testsuite(item: Dict, db: Session = Depends(get_db)):
    testsuite_id = item.get('testsuite_id')
    asyncio.create_task(testsuite_request(
        testsuite_id,
    ))
    return resp_200(data={
        'detail': 'Testcase is running background, please check result later.'},
        db=db
    )


@router.get('/logs/{testsuite_id}')
async def get_testsuite_logs(testsuite_id: int, db: Session = Depends(get_db)):
    logs = crud.get_testsuite_logs(db, testsuite_id)
    return resp_200(
        data=jsonable_encoder(logs),
        db=db
    )
