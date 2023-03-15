from apitest import models
from .schemas import EnvDomainCreate
from sqlalchemy.orm import Session
from sqlalchemy import or_


def get_env_domain(db: Session, env_domain_id: int):
    """
    根据id获取域名信息
    :param db: 数据库会话
    :param env_domain_id: 域名id
    :return: 域名信息
    """
    return db.query(models.EnvDomain).filter(models.EnvDomain.id == env_domain_id).first()


def get_env_domain_by_code(db: Session, env_domain_code: str):
    """
    根据code获取域名信息
    :param db: 数据库会话
    :param env_domain_code: 域名code
    :return: 域名信息
    """
    return db.query(models.EnvDomain).filter(models.EnvDomain.code == env_domain_code).first()


def get_env_domains(db: Session, skip: int = 0, limit: int = 100):
    """
    获取域名列表信息
    :param db: 数据库会话
    :param skip: 开始位置
    :param limit: 限制数量
    :return: 域名列表信息
    """
    if limit == 0:
        return db.query(models.EnvDomain).all()
    return db.query(models.EnvDomain).offset(skip).limit(limit).all()


def get_env_domains_by_text(text: str, db: Session, skip: int = 0, limit: int = 100):
    """
    模糊查询域名列表
    :param text: 查询字段
    :param db: 数据库会话
    :param skip: 开始位置
    :param limit: 限制数量
    :return: 域名列表信息
    """
    return db.query(models.EnvDomain).filter(or_(
        models.EnvDomain.code.like(f'%{text}%'),
        models.EnvDomain.name.like(f'%{text}%'),
        models.EnvDomain.domain.like(f'%{text}%'),
    )).offset(skip).limit(limit).all()


def create_env_domain(db: Session, env_domain: EnvDomainCreate, created_by: int = 0, last_updated_by: int = 0):
    """
    创建域名
    :param db: 数据库会话
    :param env_domain: 域名模型
    :param created_by: 创建用户id
    :param last_updated_by: 最后更新用户id
    :return: 创建的域名信息
    """
    db_env_domain = models.EnvDomain(
        code=env_domain.code,
        name=env_domain.name,
        domain=env_domain.domain,
        created_by=created_by,
        last_updated_by=last_updated_by
    )
    db.add(db_env_domain)
    db.commit()  # 提交到数据库
    db.refresh(db_env_domain)  # 刷新数据库
    return db_env_domain


def update_env_domain_by_id(db: Session, env_domain_id: int, env_domain: EnvDomainCreate, last_updated_by: int = 0):
    """
    更新域名
    :param db: 数据库会话
    :param env_domain_id: 域名id
    :param env_domain: 域名模型
    :param last_updated_by: 最后更新用户id
    :return: 更新的域名信息
    """
    db_env_domain = db.query(models.EnvDomain).filter(models.EnvDomain.id == env_domain_id).first()
    db_env_domain.code = env_domain.code
    db_env_domain.name = env_domain.name
    db_env_domain.domain = env_domain.domain
    db_env_domain.last_updated_by = last_updated_by
    db.commit()
    db.refresh(db_env_domain)  # 刷新数据库
    return db_env_domain


def delete_env_domain(db: Session, env_domain_id: int):
    """
    删除域名
    :param db: 数据库会话
    :param env_domain_id: 域名id
    :return:
    """
    db_env_domain = db.query(models.EnvDomain).filter(models.EnvDomain.id == env_domain_id).first()
    db.delete(db_env_domain)
    db.commit()
