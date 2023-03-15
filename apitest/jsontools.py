from fastapi import status
from fastapi.responses import JSONResponse, Response
from typing import Union
from user import crud as user_crud
from apitest.env_domain import crud as env_crud
from apitest.execute_account import crud as account_crud
from apitest.interface import crud as interface_crud
from sqlalchemy.orm import Session
from fastapi import Depends
from utils import get_db


def resp_200(*, data: Union[list, dict], db: Session = Depends(get_db), msg: str = 'success', **extra) -> Response:
    if type(data) == list:
        for d in data:
            _add_vos(d, db)
    elif type(data) == dict:
        _add_vos(data, db)
    content = {
        'resCode': 200,
        'resMsg': msg,
        'data': data,
    }
    if extra:
        content = {**extra, **content}
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=content
    )


def resp_400(*, data: str = None, message: str = "BAD REQUEST") -> Response:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            'resCode': 400,
            'resMsg': message,
            'data': data,
        }
    )


def _add_vos(resp: dict, db: Session = Depends(get_db)):
    if 'created_by' in resp.keys():
        user = user_crud.get_user(db, resp['created_by'])
        resp['created_by_vo'] = {
            'id': user.id,
            'email': user.email
        }
    if 'last_updated_by' in resp.keys():
        user = user_crud.get_user(db, resp['last_updated_by'])
        resp['last_updated_by_vo'] = {
            'id': user.id,
            'email': user.email
        }
    if 'env_id' in resp.keys():
        env = env_crud.get_env_domain(db, resp['env_id'])
        resp['env_vo'] = {
            'id': env.id,
            'name': env.name,
            'code': env.code,
            'domain': env.domain,
        }
    if 'execute_account_id' in resp.keys():
        account = account_crud.get_execute_account_by_id(db, resp['execute_account_id'])
        resp['execute_account_vo'] = {
            'id': account.id,
            'code': account.code,
            'username': account.username,
            'client_id': account.client_id
        }
    if 'interface_id' in resp.keys():
        interface = interface_crud.get_interface(db, resp['interface_id'])
        resp['interface_vo'] = {
            'id': interface.id,
            'name': interface.name,
            'method': interface.method,
            'path': interface.path
        }
    if 'header' in resp.keys():
        header_list = output_headers(resp['header'])
        resp['header'] = header_list
    return resp


def output_headers(header_dict: dict):
    # 返回给前端list格式header
    header_list = []
    for k, v in header_dict.items():
        header_list.append({
            'name': k,
            'value': v
        })
    return header_list
