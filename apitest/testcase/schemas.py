from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class TestcaseBase(BaseModel):
    title: str
    description: Optional[str] = None
    env_id: int
    execute_account_id: int
    interface_id: int
    header: Optional[dict] = None
    params: Optional[dict] = None
    body: Optional[dict] = None
    post_assert_code: Optional[int] = None
    post_assert_json: dict = {}


class TestcaseCreate(TestcaseBase):
    pass


class Testcase(TestcaseBase):
    id: int
    created_by: int
    last_updated_by: int
    creation_date: datetime
    last_update_date: datetime

    class Config:
        orm_mode = True


class TestcaseLogBase(BaseModel):
    testcase_id: int
    detail: dict = {}


class TestcaseLogCreate(TestcaseLogBase):
    pass


class TestcaseLog(TestcaseLogBase):
    id: int
    created_by: int
    creation_date: datetime

    class Config:
        orm_mode = True
