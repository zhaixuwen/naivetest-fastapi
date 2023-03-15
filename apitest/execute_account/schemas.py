from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ExecuteAccountBase(BaseModel):
    code: str
    env_id: int
    username: Optional[str] = None
    password: Optional[str] = None
    client_id: Optional[str] = None
    client_secret: Optional[str] = None


class ExecuteAccountCreate(ExecuteAccountBase):
    pass


class ExecuteAccount(ExecuteAccountBase):
    id: int
    created_by: int
    last_updated_by: int
    creation_date: datetime
    last_update_date: datetime

    class Config:
        orm_mode = True
