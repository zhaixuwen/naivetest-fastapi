from apitest import models
from .schemas import InterfaceCreate
from sqlalchemy.orm import Session
from sqlalchemy import or_


def get_interface(db: Session, interface_id: int):
    """
    根据id获取接口信息
    :param db: 数据库会话
    :param interface_id: 接口id
    :return: 接口信息
    """
    return db.query(models.Interface).filter(models.Interface.id == interface_id).first()


def get_interface_by_name(db: Session, name: str):
    """
    根据接口名称获取接口信息
    :param db: 数据库会话
    :param name: 接口名称
    :return: 接口信息
    """
    return db.query(models.Interface).filter(models.Interface.name == name).first()


def get_interfaces(db: Session, skip: int, limit: int):
    """
    查询接口列表信息
    :param db: 数据库会话
    :param skip: 开始位置
    :param limit: 数量限制
    :return: 接口列表信息
    """
    if limit == 0:
        return db.query(models.Interface).all()
    return db.query(models.Interface).offset(skip).limit(limit).all()


def get_interfaces_by_text(text: str, db: Session):
    """
    模糊查询
    :param db: 数据库会话
    :param text: 查询字段
    :return: 接口信息
    """
    return db.query(models.Interface).filter(or_(
        models.Interface.name.like(f'%{text}%'),
        models.Interface.path.like(f'%{text}%')
    )).all()


def create_interface(db: Session, interface: InterfaceCreate, created_by: int = 0, last_updated_by: int = 0):
    """
    创建接口
    :param db: 数据库会话
    :param interface: 接口模型
    :param created_by: 创建用户id
    :param last_updated_by: 最后更新用户id
    :return: 创建的接口信息
    """
    db_interface = models.Interface(
        name=interface.name,
        description=interface.description,
        method=interface.method,
        path=interface.path,
        created_by=created_by,
        last_updated_by=last_updated_by
    )
    db.add(db_interface)
    db.commit()
    db.refresh(db_interface)
    return db_interface


def update_interface(db: Session, interface_id: int, interface: InterfaceCreate, last_updated_by: int = 0):
    """
    更新接口
    :param db: 数据库会话
    :param interface_id: 接口id
    :param interface: 接口模型
    :param last_updated_by: 最后更新用户id
    :return: 更新的接口信息
    """
    db_interface = get_interface(db, interface_id)
    if db_interface:
        db_interface.name = interface.name
        db_interface.description = interface.description
        db_interface.method = interface.method
        db_interface.path = interface.path
        db_interface.last_updated_by = last_updated_by
    db.commit()
    db.refresh(db_interface)
    return db_interface


def delete_interface(db: Session, interface_id: int):
    """
    删除接口
    :param db: 数据库会话
    :param interface_id: 接口id
    :return:
    """
    db_interface = db.query(models.Interface).filter(models.Interface.id == interface_id).first()
    db.delete(db_interface)
    db.commit()
