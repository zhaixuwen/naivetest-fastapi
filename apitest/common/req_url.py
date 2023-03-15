from typing import Optional
from sqlalchemy.orm import Session
from apitest.interface import crud as interface_crud
from apitest.env_domain import crud as env_crud


def handle_url(env_id: int, interface_id: int, params: Optional[dict], db: Session) -> (str, str):
    env = env_crud.get_env_domain(db, env_id)
    interface = interface_crud.get_interface(db, interface_id)
    path = env.domain + interface.path
    if params:
        suffix = '?'
        for k, v in params.items():
            suffix += '{}={}&'.format(k, v)
        return path + suffix[:-1], interface.method
    return path, interface.method
