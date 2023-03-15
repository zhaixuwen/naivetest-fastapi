from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from config import MYSQL_URL

# 数据库连接配置
SQLALCHEMY_DATABASE_URI = MYSQL_URL

# 创建数据库引擎
engine = create_engine(SQLALCHEMY_DATABASE_URI, pool_timeout=60, pool_recycle=1800)
# 创建数据库会话
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# 声明基类
Base = declarative_base()
