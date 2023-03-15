from typing import Optional
from aioredis import Redis


# 将header中的key统一小写,方便后续处理
def lower_dict(d: dict) -> dict:
    new_dict = dict((k.lower(), v) for k, v in d.items())
    return new_dict


async def handle_head(execute_account_id: int, head: Optional[dict], redis: Redis) -> dict:
    h = await redis.hgetall(str(execute_account_id))
    # 合并2个dict,存在重复字段则第2个覆盖第1个
    return lower_dict({**h, **head})
