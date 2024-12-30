from sqlmodel import SQLModel, create_engine, Session
from typing import Annotated
from fastapi import Depends

# 用户库相关配置
user_pgsql_url = 'mysql+pymysql://jonnyan404:www.mrdoc.fun@172.31.22.85:3306/mrdoc'
user_engine = create_engine(user_pgsql_url, echo=True)

# 财务库相关配置
financial_pgsql_url = 'mssql+pymssql://fc:123456@172.31.22.80:1433/gxcw60?tds_version=7.0&charset=GB18030'
financial_engine = create_engine(financial_pgsql_url, echo=True)

#
# def create_db_and_tables():
#     SQLModel.metadata.create_all(user_engine, checkfirst=True)
#     SQLModel.metadata.create_all(financial_engine, checkfirst=True)
