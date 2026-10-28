from sqlmodel import SQLModel, create_engine, Session
from typing import Annotated
from fastapi import Depends

# 用户库相关配置
user_pgsql_url = 'mysql+pymysql://jonnyan404:www.mrdoc.fun@172.31.22.85:3306/mrdoc'
user_engine = create_engine(user_pgsql_url, pool_recycle=3600,
                            pool_pre_ping=True
                            , echo=True)

# 财务库相关配置
financial_sql_url = 'mssql+pymssql://tc_gxcw60:gxcw60@172.31.22.168:1433/gxcw60?tds_version=7.0&charset=GB18030'

# # 本地调试时使用
# financial_sql_url = 'mssql+pymssql://tc_gxcw60:gxcw60@172.31.22.80:1433/gxcw60?tds_version=7.0&charset=GB18030'
financial_engine = create_engine(financial_sql_url,
                                 pool_recycle=3600,
                                 pool_pre_ping=True
                                 , echo=True)

# 财务库相关配置
financial_sql_write_url = 'mssql+pymssql://tc_gxcw60:gxcw60@172.31.22.168:1433/gxcw60?tds_version=7.0&charset=UTF-8'

# # 本地调试时使用
# financial_sql_write_url = 'mssql+pymssql://tc_gxcw60:gxcw60@172.31.22.80:1433/gxcw60?tds_version=7.0&charset=UTF-8'
financial_write_engine = create_engine(financial_sql_write_url, pool_recycle=3600,
                                       pool_pre_ping=True
                                       , echo=True)

# 2025财务库相关配置
financial_2025_sql_url = 'mssql+pymssql://tc_gxcw60:gxcw60@172.31.22.168:1433/gxcw60_2025?tds_version=7.0&charset=GB18030'
financial_engine_2025 = create_engine(financial_2025_sql_url, pool_recycle=3600,
                                      pool_pre_ping=True
                                      , echo=True)

# 2024财务库相关配置
financial_2024_sql_url = 'mssql+pymssql://tc_gxcw60:gxcw60@172.31.22.168:1433/gxcw60_2024?tds_version=7.0&charset=GB18030'
financial_engine_2024 = create_engine(financial_2024_sql_url, pool_recycle=3600,
                                      pool_pre_ping=True
                                      , echo=True)

# 学生收费库相关配置
student_expense_mssql_url = 'mssql+pymssql://tc_gxcw60:gxcw60@172.31.22.168:1433/xssf60?tds_version=7.0&charset=GB18030'

# # 本地调试时使用
# student_expense_mssql_url = 'mssql+pymssql://fc:123456@172.31.22.80:1433/xssf60?tds_version=7.0&charset=GB18030'
student_expense_engine = create_engine(student_expense_mssql_url, pool_recycle=3600,
                                       pool_pre_ping=True
                                       , echo=True)
#
# def create_db_and_tables():
#     SQLModel.metadata.create_all(user_engine, checkfirst=True)
#     SQLModel.metadata.create_all(financial_engine, checkfirst=True)
import oracledb
import logging

logger = logging.getLogger(__name__)

# Oracle 客户端初始化（支持 graceful fallback）
try:
    # 本地调试时使用
    oracledb.init_oracle_client(lib_dir="D:\\instantclient_11_2")
    logger.info("Oracle 客户端初始化成功 (D:\\instantclient_11_2)")
except Exception as e:
    try:
        # 服务器环境尝试其他路径
        oracledb.init_oracle_client(lib_dir="F:\\instantclient_11_2")
        logger.info("Oracle 客户端初始化成功 (F:\\instantclient_11_2)")
    except Exception as e2:
        logger.warning(f"Oracle 客户端初始化失败，将使用 thin 模式：{str(e2)}")
        # 不阻塞启动，oracledb 会自动使用 thin 模式
# 报销库相关配置
reimbursement_sql_url = "oracle+oracledb://ghwsyy:ghwsyy@172.31.22.229:1521/ORCL"
reimbursement_engine = create_engine(reimbursement_sql_url, pool_recycle=3600,
                                     pool_pre_ping=True, echo=True)

# 中间库配置
intermediate_database_url = "mysql+pymysql://root:22861626@172.31.22.3:3306/jobs"
intermediate_database_engine = create_engine(intermediate_database_url, pool_recycle=3600,
                            pool_pre_ping=True
                            , echo=True)

# 采购库配置
purchase_database_url = "mysql+pymysql://dgut_cw:Dgut#2026Cw88@172.31.60.112:3307/dgut_purchase"
purchase_database_engine = create_engine(purchase_database_url, pool_recycle=3600,
                            pool_pre_ping=True
                            , echo=True)


