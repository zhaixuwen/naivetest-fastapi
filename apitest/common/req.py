import time
import requests
from aioredis import Redis
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from .req_url import handle_url
from .req_head import handle_head
from .req_assert import handle_assert
from apitest.testcase import crud as case_crud
from apitest.testsuite import crud as suite_crud
from apitest import models
from utils import get_redis, get_db, logger


async def testcase_request(case: dict, db: Session, redis: Redis):
    redis = await redis
    url, method = handle_url(case.get('env_id'), case.get('interface_id'), case.get('params'), db)
    head = await handle_head(case.get('execute_account_id'), case.get('header'), redis)
    content_type = head.get('content-type')
    logger.info('Request method=>' + method)
    logger.info('Request url=>' + url)
    logger.info(f'Request header=>{head}')
    logger.info(f'Request body=>{case.get("body")}')
    if content_type and content_type == 'application/json':
        resp = requests.request(method=method, url=url, json=case.get('body'), headers=head)
    else:
        resp = requests.request(method=method, url=url, data=case.get('body'), headers=head)
    logger.info('Response content=>' + resp.content.decode())
    assert_result = handle_assert(resp, case.get('post_assert_code'), case.get('post_assert_json'))
    request_result = {
        'response': resp.json(),
        'assert': assert_result,
        'time': round(resp.elapsed.total_seconds(), 2),
        'creation_date': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    }
    if case.get('id'):
        request_result['id'] = case.get('id')
        request_result['title'] = case.get('title')
        request_result['method'] = case.get('method')
    return request_result


async def testsuite_request(testsuite_id: int):
    db = next(get_db())
    redis = await get_redis()
    suite = suite_crud.get_testsuite(db, testsuite_id)
    cases = jsonable_encoder(suite.testcases)
    has_error = False
    suite_log = {
        'testsuite_id': testsuite_id,
        'detail': []
    }
    logger.info(f'Start run testsuite=>{testsuite_id}')
    for cid in cases:
        try:
            r = await testcase_request(
                jsonable_encoder(case_crud.get_testcase(db, cid)),
                db,
                redis
            )
            if r.get('assert').get('result') == 'error':
                has_error = True
        except Exception as e:
            raise e
        finally:
            db.close()
        suite_log.get('detail').append(r)
    # suite_log['has_error'] = has_error
    # 增加执行集执行人和结果状态信息
    suite_crud.create_testsuite_log(db, models.TestsuiteLog(**suite_log))
