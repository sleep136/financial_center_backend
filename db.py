from sqlmodel import SQLModel, create_engine, Session
from typing import Annotated
from fastapi import Depends

# 用户库相关配置
user_pgsql_url = 'mysql+pymysql://jonnyan404:www.mrdoc.fun@172.31.22.85:3306/mrdoc'
user_engine = create_engine(user_pgsql_url, echo=True)

# 财务库相关配置
financial_sql_url = 'mssql+pymssql://tc_gxcw60:gxcw60@172.31.22.168:1433/gxcw60?tds_version=7.0&charset=GB18030'
financial_engine = create_engine(financial_sql_url, echo=True)

# 2025财务库相关配置
financial_2025_sql_url = 'mssql+pymssql://tc_gxcw60:gxcw60@172.31.22.168:1433/gxcw60_2025?tds_version=7.0&charset=GB18030'
financial_engine_2025 = create_engine(financial_2025_sql_url, echo=True)

# 2024财务库相关配置
financial_2024_sql_url = 'mssql+pymssql://tc_gxcw60:gxcw60@172.31.22.168:1433/gxcw60_2024?tds_version=7.0&charset=GB18030'
financial_engine_2024 = create_engine(financial_2024_sql_url, echo=True)

# 学生收费库相关配置
student_expense_mssql_url = 'mssql+pymssql://tc_gxcw60:gxcw60@172.31.22.168:1433/xssf60?tds_version=7.0&charset=GB18030'
student_expense_engine = create_engine(student_expense_mssql_url, echo=True)
#
# def create_db_and_tables():
#     SQLModel.metadata.create_all(user_engine, checkfirst=True)
#     SQLModel.metadata.create_all(financial_engine, checkfirst=True)
import oracledb

# windows用应用启动时启用厚模式
oracledb.init_oracle_client(lib_dir="F:\instantclient_11_2")

# # docker中用
# oracledb.init_oracle_client(lib_dir="/opt/oracle/instantclient/instantclient_11_2")
# 报销库相关配置
reimbursement_sql_url = "oracle+oracledb://ghwsyy:ghwsyy@172.31.22.229:1521/ORCL"
reimbursement_engine = create_engine(reimbursement_sql_url, echo=True)