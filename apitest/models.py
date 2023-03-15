from sqlalchemy import Column, Boolean, Integer, String, DateTime, func
from sqlalchemy.types import JSON
from sqlalchemy.ext.mutable import MutableDict, MutableList
from database import Base


class EnvDomain(Base):
    __tablename__ = 'env_domain'
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(255), unique=True, index=True)
    name = Column(String(255), unique=True)
    domain = Column(String(255))
    created_by = Column(Integer)
    last_updated_by = Column(Integer)
    creation_date = Column(DateTime, default=func.now())
    last_update_date = Column(DateTime, onupdate=func.now(), default=func.now())


class ExecuteAccount(Base):
    __tablename__ = 'execute_account'
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(255), unique=True, index=True)
    env_id = Column(Integer)
    username = Column(String(255))
    password = Column(String(255))
    client_id = Column(String(255))
    client_secret = Column(String(255))
    created_by = Column(Integer)
    last_updated_by = Column(Integer)
    creation_date = Column(DateTime, default=func.now())
    last_update_date = Column(DateTime, onupdate=func.now(), default=func.now())


class Interface(Base):
    __tablename__ = 'interface'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, index=True)
    description = Column(String(255))
    method = Column(String(10))
    path = Column(String(255))
    created_by = Column(Integer)
    last_updated_by = Column(Integer)
    creation_date = Column(DateTime, default=func.now())
    last_update_date = Column(DateTime, onupdate=func.now(), default=func.now())


class Testcase(Base):
    __tablename__ = 'testcase'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), unique=True, index=True)
    description = Column(String(255))
    env_id = Column(Integer)
    execute_account_id = Column(Integer)
    interface_id = Column(Integer)
    header = Column(MutableDict.as_mutable(JSON))
    params = Column(MutableDict.as_mutable(JSON))
    body = Column(MutableDict.as_mutable(JSON))
    post_assert_code = Column(Integer)
    post_assert_json = Column(MutableDict.as_mutable(JSON))
    created_by = Column(Integer)
    last_updated_by = Column(Integer)
    creation_date = Column(DateTime, default=func.now())
    last_update_date = Column(DateTime, onupdate=func.now(), default=func.now())


class Testsuite(Base):
    __tablename__ = 'testsuite'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, index=True)
    description = Column(String(255))
    is_active = Column(Boolean, default='Y')
    members = Column(MutableList.as_mutable(JSON))
    last_execute_status = Column(Integer, default=1)
    testcases = Column(MutableList.as_mutable(JSON))
    created_by = Column(Integer)
    last_updated_by = Column(Integer)
    creation_date = Column(DateTime, default=func.now())
    last_update_date = Column(DateTime, onupdate=func.now(), default=func.now())


class TestcaseLog(Base):
    __tablename__ = 'testcase_log'
    id = Column(Integer, primary_key=True, index=True)
    testcase_id = Column(Integer, index=True)
    detail = Column(MutableDict.as_mutable(JSON))
    created_by = Column(Integer)
    creation_date = Column(DateTime, default=func.now())


class TestsuiteLog(Base):
    __tablename__ = 'testsuite_log'
    id = Column(Integer, primary_key=True, index=True)
    testsuite_id = Column(Integer, index=True)
    detail = Column(MutableList.as_mutable(JSON))
    creation_date = Column(DateTime, default=func.now())
