from apitest import models
from .schemas import TestcaseCreate, TestcaseLogCreate
from sqlalchemy.orm import Session
from sqlalchemy import or_


def get_testcase(db: Session, testcase_id: int):
    """
    根据用例id获取用例信息
    :param db: 数据库会话
    :param testcase_id: 用例id
    :return: 用例信息
    """
    return db.query(models.Testcase).filter(models.Testcase.id == testcase_id).first()


def get_testcases(db: Session, skip: int, limit: int):
    """
    查询用例列表信息
    :param db: 数据库会话
    :param skip: 开始位置
    :param limit: 数量限制
    :return: 用例列表信息
    """
    if limit == 0:
        return db.query(models.Testcase).all()
    return db.query(models.Testcase).offset(skip).limit(limit).all()


def get_testcase_by_title(db: Session, title: str):
    """
    根据用例标题获取用例信息
    :param db: 数据库会话
    :param title: 用例标题
    :return: 用例信息
    """
    return db.query(models.Testcase).filter(models.Testcase.title == title).first()


def get_testcases_by_text(db: Session, text: str):
    """
    模糊查询
    :param db: 数据库会话
    :param text: 查询字段
    :return: 用例列表信息
    """
    return db.query(models.Testcase).filter(or_(
        models.Testcase.title.like(f'%{text}%'),
    )).all()


def get_testcases_by_interface(db: Session, interface_id: int):
    """
    模糊查询
    :param db: 数据库会话
    :param interface_id: 接口id
    :return: 用例列表信息
    """
    return db.query(models.Testcase).filter(models.Testcase.interface_id == interface_id).all()


def get_testcases_by_env(db: Session, env_id: int):
    """
    模糊查询
    :param db: 数据库会话
    :param env_id: 环境id
    :return: 用例列表信息
    """
    return db.query(models.Testcase).filter(models.Testcase.env_id == env_id).all()


def create_testcase(db: Session, testcase: TestcaseCreate, created_by: int, last_updated_by: int):
    """
    创建用例
    :param db: 数据库会话
    :param testcase: 用例模型
    :param created_by: 创建用户id
    :param last_updated_by: 最后更新用户id
    :return: 创建的用例信息
    """
    db_testcase = models.Testcase(
        title=testcase.title,
        description=testcase.description,
        env_id=testcase.env_id,
        execute_account_id=testcase.execute_account_id,
        interface_id=testcase.interface_id,
        header=testcase.header,
        params=testcase.params,
        body=testcase.body,
        post_assert_code=testcase.post_assert_code,
        post_assert_json=testcase.post_assert_json,
        created_by=created_by,
        last_updated_by=last_updated_by
    )
    db.add(db_testcase)
    db.commit()
    db.refresh(db_testcase)
    return db_testcase


def update_testcase(db: Session, testcase_id: int, testcase: TestcaseCreate, last_updated_by: int):
    """
        更新用例
        :param db: 数据库会话
        :param testcase_id: 更新的用例id
        :param testcase: 用例模型
        :param last_updated_by: 最后更新用户id
        :return: 更新的用例信息
        """
    db_testcase = get_testcase(db, testcase_id)
    db_testcase.title = testcase.title,
    db_testcase.description = testcase.description,
    db_testcase.env_id = testcase.env_id,
    db_testcase.execute_account_id = testcase.execute_account_id,
    db_testcase.interface_id = testcase.interface_id,
    # update header
    header = db_testcase.header.copy()
    header.update(testcase.header)
    db_testcase.header = header
    # update params
    params = db_testcase.params.copy()
    params.update(testcase.params)
    db_testcase.params = params
    # update body
    body = db_testcase.body.copy()
    body.update(testcase.body)
    db_testcase.body = body
    db_testcase.post_assert_code = testcase.post_assert_code,
    # update post_assert_json
    post_assert_json = db_testcase.post_assert_json.copy()
    post_assert_json.update(testcase.post_assert_json)
    db_testcase.post_assert_json = post_assert_json
    db_testcase.last_updated_by = last_updated_by
    db.add(db_testcase)
    db.commit()
    db.refresh(db_testcase)
    return db_testcase


def delete_testcase(db: Session, testcase_id: int):
    """
    删除用例
    :param db: 数据库会话
    :param testcase_id: 用例id
    :return:
    """
    db_testcase = db.query(models.Testcase).filter(models.Testcase.id == testcase_id).first()
    db.delete(db_testcase)
    db.commit()


def create_testcase_log(db: Session, testcase_log: TestcaseLogCreate, created_by):
    """
    添加用例执行日志
    :param db: 数据库会话
    :param testcase_log: 用例日志模型
    :param created_by: 创建人id
    :return:
    """
    log = models.TestcaseLog(
        testcase_id=testcase_log.testcase_id,
        detail=testcase_log.detail,
        created_by=created_by
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return log


def read_testcase_log(db: Session, case_id: int, skip: int = 0, limit: int = 3):
    """
    查询用例执行日志
    :param db: 数据库会话
    :param case_id: 用例id
    :param skip: 起始查询位置
    :param limit: 查询数量
    :return: 用例执行日志信息
    """
    logs = db.query(models.TestcaseLog).filter(models.TestcaseLog.testcase_id == case_id).order_by(
        models.TestcaseLog.creation_date.desc()).offset(skip).limit(limit).all()
    return logs
