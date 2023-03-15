from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class InterfaceBase(BaseModel):
    name: str
    description: Optional[str] = None
    method: str
    path: str


class InterfaceCreate(InterfaceBase):
    pass


class Interface(InterfaceBase):
    id: int
    created_by: int
    last_updated_by: int
    creation_date: datetime
    last_update_date: datetime

    class Config:
        orm_mode = True
