from pydantic import BaseModel
from datetime import datetime


class EnvDomainBase(BaseModel):
    code: str
    name: str
    domain: str


class EnvDomainCreate(EnvDomainBase):
    pass


class EnvDomain(EnvDomainBase):
    id: int
    created_by: int
    last_updated_by: int
    creation_date: datetime
    last_update_date: datetime

    class Config:
        orm_mode = True
