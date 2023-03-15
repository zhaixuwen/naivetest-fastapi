import json
from database import engine
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware

from user import models as user_models
from user.router import oauth_token
from user.router import router as user_router

from apitest import models as apitest_models
from apitest.env_domain.router import router as env_domain_router
from apitest.execute_account.router import router as execute_account_router
from apitest.interface.router import router as interface_router
from apitest.testcase.router import router as testcase_router
from apitest.testsuite.router import router as testsuite_router

from utils import get_db, get_redis
from scheduler import scheduler
from scheduler import router as job_router
from utils import logger

user_models.Base.metadata.create_all(bind=engine)
apitest_models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(job_router, prefix='/jobs')
app.include_router(user_router, prefix='/users')
app.include_router(env_domain_router, prefix='/env_domains')
app.include_router(execute_account_router, prefix='/execute_accounts')
app.include_router(interface_router, prefix='/interfaces')
app.include_router(testcase_router, prefix='/testcases')
app.include_router(testsuite_router, prefix='/testsuites')

db = get_db()
logger.info(f"MySQL连接成功->{db}")


@app.on_event("startup")
async def startup_event():
    # Redis服务注册
    app.state.redis = await get_redis()
    logger.info(f"Redis连接成功->{app.state.redis}")
    # APScheduler服务注册
    scheduler.start()
    logger.info('APScheduler启动成功')


@app.on_event("shutdown")
async def shutdown_event():
    await app.state.redis.close()


# 中间件校验token
@app.middleware("http")
async def check_token(request: Request, call_next):
    if request.url.components.path not in ['/users/login', '/users/login/']:
        # 从header中获取token字段
        auth = request.headers.get("access_token")
        if not auth:
            return {"resMsg": "No access token"}
        # 认证token返回token对应的用户id
        user_id = oauth_token(auth)
        if user_id:
            # 在header中加入token解析出的user_id
            request.headers._list.append((b'user_id', bytes(str(user_id).encode('utf-8'))))
            response: Response = await call_next(request)
            response.headers['user_id'] = str(user_id)
            return response
        else:
            # user id为0则提示token错误
            resp = Response(
                content=json.dumps({"resMsg": "Error access token", "resCode": 401}),
                headers={"content-type": "application/json"}
            )
            resp.status_code = 401
            return resp
    else:
        # 登录接口跳过认证
        response: Response = await call_next(request)
        return response


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
