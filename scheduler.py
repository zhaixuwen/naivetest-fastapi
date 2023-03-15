import asyncio
import logging
import time
from typing import Dict
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.triggers.cron import CronTrigger
from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session

from config import REDIS_HOST, REDIS_PASSWORD
from utils import get_db, get_redis
from apitest.tasks import get_token
from apitest.jsontools import resp_200
from apitest.execute_account.crud import get_execute_accounts
from apitest.common.req import testsuite_request

# ====================创建Scheduler实例====================
REDIS_DB = {
    "db": 0,
    "host": REDIS_HOST,
    "password": REDIS_PASSWORD
}

interval_task = {
    # 配置存储器
    "jobstores": {
        # 使用Redis进行存储
        'default': RedisJobStore(**REDIS_DB)
    },
    # 配置执行器
    "executors": {
        # 使用进程池进行调度，最大进程数是10个
        'default': ThreadPoolExecutor(10)
    },
    # 创建job时的默认参数
    "job_defaults": {
        'coalesce': False,  # 是否合并执行
        'max_instances': 3,  # 最大实例数
    }
}

scheduler = BackgroundScheduler(**interval_task)


# ====================Token任务====================

# Depends注入无法在非路由方法中使用，用next()代替获取生成器的值
async def refresh_token(db: Session = next(get_db())):
    redis = await get_redis()
    accounts = get_execute_accounts(db=db, skip=0, limit=100)
    for account in accounts:
        await get_token(account, db, redis)
    db.close()


def run_task(func, args=None):
    if args:
        asyncio.run(func(args))
    else:
        asyncio.run(func())


# 添加token或许定时任务
scheduler.add_job(
    run_task,
    CronTrigger.from_crontab('*/30 * * * *', timezone='Asia/Shanghai'),
    id='refresh_token',
    name='refresh_token',
    args=[refresh_token],
    replace_existing=True,
    coalesce=True
)

# ====================Scheduler增删改查====================
router = APIRouter()


@router.get('/refresh_token')
def manual_refresh_token(db: Session = Depends(get_db)):
    asyncio.run(refresh_token(db))


@router.get('/')
def get_jobs(skip: int = 0, limit: int = 10):
    jobs = scheduler.get_jobs()
    limit_jobs = jobs[skip:skip+limit]
    resp = []
    for job in limit_jobs:
        if job.id == 'refresh_token':
            continue
        trigger_list = str(job.trigger).split('\'')
        resp.append({
            'id': job.id,
            'name': job.name,
            'testsuite_id': int(job.id.split('-')[1]),
            'trigger': f'{trigger_list[9]} {trigger_list[7]} {trigger_list[5]} {trigger_list[3]} {trigger_list[1]}',
            'next_run_time': job.next_run_time.strftime("%Y-%m-%d %H:%M:%S")
        })
    return resp_200(data=resp, count=len(jobs))


@router.get('/{job_id}')
def get_job(job_id: str):
    job = scheduler.get_job(job_id)
    trigger_list = str(job.trigger).split('\'')
    resp = {
        "id": job.id,
        'name': job.name,
        'testsuite_id': int(job.args[1]),
        "trigger": f'{trigger_list[9]} {trigger_list[7]} {trigger_list[5]} {trigger_list[3]} {trigger_list[1]}',
        'next_run_time': job.next_run_time.strftime("%Y-%m-%d %H:%M:%S")
    }
    return resp_200(data=resp)


@router.post('/')
async def create_job(item: Dict):
    testsuite_id = item.get('testsuite_id')
    job_name = item.get('job_name')
    job_id = 'TestsuiteRun-{}-{}'.format(testsuite_id, str(int(time.time())))
    crontab = item.get('crontab')
    scheduler.add_job(
        run_task,
        CronTrigger.from_crontab(crontab, timezone='Asia/Shanghai'),
        id=job_id,
        args=[testsuite_request, testsuite_id],
        replace_existing=True,
        coalesce=True,
        name=job_name
    )
    return {
        'resCode': 200,
        'resMsg': "success"
    }


@router.put('/')
def modify_job(item: Dict):
    job = scheduler.get_job(item.get('id'))
    job.modify(
        name=item.get('job_name'),
        trigger=CronTrigger.from_crontab(item.get('crontab'), timezone='Asia/Shanghai'),
    )
    return {
        'resCode': 200,
        'resMsg': "success"
    }


@router.delete('/{job_id}')
def del_job(job_id: str):
    if job_id == 'refresh_token':
        pass
    else:
        scheduler.remove_job(job_id)
    return {
        'resCode': 200,
        'resMsg': "success"
    }
