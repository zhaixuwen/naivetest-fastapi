from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class TestsuiteBase(BaseModel):
    name: str
    description: Optional[str] = None
    is_active: bool
    members: List[int] = []
    testcases: List[int] = []


class TestsuiteCreate(TestsuiteBase):
    pass


class Testsuite(TestsuiteBase):
    id: int
    last_execute_status: int = 1
    created_by: int
    last_updated_by: int
    creation_date: datetime
    last_update_date: datetime

    class Config:
        orm_mode = True


class TestsuiteLog(BaseModel):
    id: int
    testsuite_id: int
    detail: list = []
    creation_date: datetime

    class Config:
        orm_mode = True
