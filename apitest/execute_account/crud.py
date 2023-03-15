from apitest import models
from .schemas import ExecuteAccountCreate
from sqlalchemy.orm import Session
from sqlalchemy import or_


def get_execute_account(db: Session, execute_account_id: int):
    """
    根据id获取执行账户信息
    :param db: 数据库会话
    :param execute_account_id: 执行账户id
    :return: 执行账户信息
    """
    return db.query(models.ExecuteAccount).filter(models.ExecuteAccount.id == execute_account_id).first()


def get_execute_account_by_code(db: Session, execute_account_code: str):
    """
    根据code查询执行账户信息
    :param db: 数据库会话
    :param execute_account_code: 执行账户code
    :return: 执行账户信息
    """
    return db.query(models.ExecuteAccount).filter(models.ExecuteAccount.code == execute_account_code).first()


def get_execute_account_by_id(db: Session, execute_account_id: int):
    """
    根据id查询执行账户信息
    :param db: 数据库会话
    :param execute_account_id: 执行账户id
    :return: 执行账户信息
    """
    return db.query(models.ExecuteAccount).filter(models.ExecuteAccount.id == execute_account_id).first()


def get_execute_accounts(db: Session, skip: int = 0, limit: int = 100):
    """
    查询执行账户列表信息
    :param db: 数据库会话
    :param skip: 开始位置
    :param limit: 数量限制
    :return: 执行账户列表信息
    """
    if limit == 0:
        return db.query(models.ExecuteAccount).all()
    return db.query(models.ExecuteAccount).offset(skip).limit(limit).all()


def get_execute_accounts_by_text(text: str, db: Session, skip: int = 0, limit: int = 100):
    """
    模糊查询
    :param text: 查询字段
    :param db: 数据库会话
    :param skip: 开始位置
    :param limit: 限制数量
    :return: 域名列表信息
    """
    return db.query(models.ExecuteAccount).filter(or_(
        models.ExecuteAccount.code.like(f'%{text}%'),
        models.ExecuteAccount.username.like(f'%{text}%'),
        models.ExecuteAccount.client_id.like(f'%{text}%')
    )).offset(skip).limit(limit).all()


def create_execute_account(db: Session, execute_account: ExecuteAccountCreate, created_by: int = 0,
                           last_updated_by: int = 0):
    """
    创建执行账户
    :param db: 数据库会话
    :param execute_account: 执行账户模型
    :param created_by: 创建用户id
    :param last_updated_by: 最后更新用户id
    :return: 创建的执行账户信息
    """
    db_execute_account = models.ExecuteAccount(
        code=execute_account.code,
        env_id=execute_account.env_id,
        username=execute_account.username,
        password=execute_account.password,
        client_id=execute_account.client_id,
        client_secret=execute_account.client_secret,
        created_by=created_by,
        last_updated_by=last_updated_by
    )
    db.add(db_execute_account)
    db.commit()  # 提交到数据库
    db.refresh(db_execute_account)  # 刷新数据库
    return db_execute_account


def update_execute_account_by_id(db: Session, account_id: int, execute_account: ExecuteAccountCreate,
                                 last_updated_by: int):
    """
    创建执行账户
    :param db: 数据库会话
    :param account_id: 执行账户id
    :param execute_account: 执行账户模型
    :param last_updated_by: 最后更新用户id
    :return: 更新的执行账户信息
    """
    db_execute_account = db.query(models.ExecuteAccount).filter(models.ExecuteAccount.id == account_id).first()
    db_execute_account.code = execute_account.code
    db_execute_account.env_id = execute_account.env_id
    db_execute_account.username = execute_account.username
    db_execute_account.password = execute_account.password
    db_execute_account.client_id = execute_account.client_id
    db_execute_account.client_secret = execute_account.client_secret
    db_execute_account.last_updated_by = last_updated_by
    db.commit()
    db.refresh(db_execute_account)
    return db_execute_account


def delete_execute_account(db: Session, execute_account_id: int):
    """
    删除执行账户
    :param db: 数据库会话
    :param execute_account_id: 执行账户id
    :return:
    """
    db_execute_account = db.query(models.ExecuteAccount).filter(models.ExecuteAccount.id == execute_account_id).first()
    db.delete(db_execute_account)
    db.commit()
