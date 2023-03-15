import requests
from aioredis import Redis
from sqlalchemy.orm import Session
from apitest.execute_account.schemas import ExecuteAccount
from apitest.env_domain import crud as env_crud
from utils import logger


async def get_token(account: ExecuteAccount, db: Session, redis: Redis):
    env = env_crud.get_env_domain(db, account.env_id)
    token_dict = {}
    # 根据不同公司业务，将获取token的服务存放在token_dict中，并保存到redis中
    if account.username:
        url = env.domain + '/api/xxx/token'
        body = {
            "username": account.username,
            "password": account.password
        }
        r = requests.post(url=url, data=body)
        if r.status_code == 200:
            token = r.json().get('access_token')
            logger.info(f"ExeAccount {account.id} => {token}")
            token_dict = {'authorization': f'Bearer {token}'}
    else:
        url = env.domain + f'/api/xxx/token/get?client_id={account.client_id}&client_secret={account.client_secret}'
        r = requests.get(url=url)
        if r.status_code == 200:
            token = r.json()['data'].get('access_token')
            logger.info(f"ExeAccount {account.id} => {token}")
            token_dict = {'access_token': r.json()['data'].get('access_token')}
    await redis.hset(name=str(account.id), mapping=token_dict)
