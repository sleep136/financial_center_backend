from sqlmodel import SQLModel, create_engine, Session
from typing import Annotated
from fastapi import Depends

# 用户库相关配置
user_pgsql_url = 'mysql+pymysql://jonnyan404:www.mrdoc.fun@172.31.22.85:3306/mrdoc'
user_engine = create_engine(user_pgsql_url, echo=True)

# 财务库相关配置
financial_sql_url = 'mssql+pymssql://fc:123456@172.31.22.80:1433/gxcw60?tds_version=7.0&charset=GB18030'
financial_engine = create_engine(financial_sql_url, echo=True)

# 学生收费库相关配置
student_expense_mssql_url = 'mssql+pymssql://fc:123456@172.31.22.80:1433/xssf60?tds_version=7.0&charset=GB18030'
student_expense_engine = create_engine(student_expense_mssql_url, echo=True)
#
# def create_db_and_tables():
#     SQLModel.metadata.create_all(user_engine, checkfirst=True)
#     SQLModel.metadata.create_all(financial_engine, checkfirst=True)

# 报销库相关配置
reimbursement_sql_url = 'oracle://ghwsyy:ghwsyy@172.31.22.229:1521/ORCL'
reimbursement_engine = create_engine(reimbursement_sql_url, echo=True)