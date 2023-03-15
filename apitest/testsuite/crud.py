from apitest import models
from .schemas import TestsuiteCreate
from sqlalchemy.orm import Session


def get_testsuite(db: Session, testsuite_id: int):
    """
    根据id获取执行集信息
    :param db: 数据库会话
    :param testsuite_id: 执行集id
    :return: 执行集信息
    """
    return db.query(models.Testsuite).filter(models.Testsuite.id == testsuite_id).first()


def get_testsuite_by_name(db: Session, name: str):
    """
    根据执行集名称获取信息
    :param db: 数据库会话
    :param name: 执行集名称
    :return: 执行集信息
    """
    return db.query(models.Testsuite).filter(models.Testsuite.name == name).first()


def get_testsuites(db: Session, skip: int, limit: int):
    """
    查询执行集列表信息
    :param db: 数据库会话
    :param skip: 开始位置
    :param limit: 数量限制
    :return: 执行集列表信息
    """
    return db.query(models.Testsuite).offset(skip).limit(limit).all()


def create_testsuite(db: Session, testsuite: TestsuiteCreate, created_by: int, last_updated_by: int):
    """
    创建执行集
    :param db: 数据库会话
    :param testsuite: 执行集模型
    :param created_by: 创建人id
    :param last_updated_by: 最后更新人id
    :return: 创建的执行集信息
    """
    db_testsuite = models.Testsuite(
        name=testsuite.name,
        description=testsuite.description,
        is_active=testsuite.is_active,
        members=testsuite.members,
        testcases=testsuite.testcases,
        created_by=created_by,
        last_updated_by=last_updated_by
    )
    db.add(db_testsuite)
    db.commit()
    db.refresh(db_testsuite)
    return db_testsuite


def update_testsuite_by_id(db: Session, testsuite_id: int, testsuite: TestsuiteCreate, last_updated_by: int):
    """
    更新执行集
    :param db: 数据库会话
    :param testsuite_id: 执行集id
    :param testsuite: 执行集模型
    :param last_updated_by: 最后更新人
    :return: 更新的执行集信息
    """
    db_testsuite = db.query(models.Testsuite).filter(models.Testsuite.id == testsuite_id).first()
    db_testsuite.name = testsuite.name
    db_testsuite.description = testsuite.description
    db_testsuite.is_active = testsuite.is_active
    db_testsuite.members = testsuite.members
    db_testsuite.testcases = testsuite.testcases
    # update members
    # members = db_testsuite.members.copy()
    # members.update(testsuite.members)
    # db_testsuite.members = members
    # update testcases
    # testcases = db_testsuite.testcases.copy()
    # testcases.update(testsuite.testcases)
    # db_testsuite.testcases = testcases
    db_testsuite.last_updated_by = last_updated_by
    db.commit()
    db.refresh(db_testsuite)
    return db_testsuite


def delete_testsuite(db: Session, testsuite_id: int):
    """
    删除执行集
    :param db: 数据库会话
    :param testsuite_id: 执行集id
    :return:
    """
    db_testsuite = db.query(models.Testsuite).filter(models.Testsuite.id == testsuite_id).first()
    db.delete(db_testsuite)
    db.commit()


def create_testsuite_log(db: Session, log: models.TestsuiteLog):
    """
    插入执行集执行日志
    :param db: 数据库会话
    :param log: 执行集日志模型
    :return:
    """
    db_log = models.TestsuiteLog(testsuite_id=log.testsuite_id, detail=log.detail)
    db.add(db_log)
    db.commit()
    db.refresh(db_log)


def get_testsuite_logs(db: Session, testsuite_id: int):
    """
    查询执行集报告
    :param db: 数据库会话
    :param testsuite_id: 执行集id
    :return: 执行集报告列表
    """
    db_logs = db.query(models.TestsuiteLog).filter(models.TestsuiteLog.testsuite_id == testsuite_id).order_by(
        models.TestsuiteLog.creation_date.desc()).offset(0).limit(5).all()
    return db_logs
