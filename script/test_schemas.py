from sqlalchemy import create_engine, MetaData, Table

import oracledb

# 在应用启动时启用厚模式
oracledb.init_oracle_client(lib_dir="D:\instantclient_11_2")
connection_string = "oracle+oracledb://ghwsyy:ghwsyy@172.31.22.229:1521/ORCL"
engine = create_engine(connection_string)

# 反射表结构
metadata = MetaData()
metadata.reflect(bind=engine, schema='oracle_ocm')

# # 查看表的所有字段
# table = metadata.tables['GSSB_GXSFFB']
# for column in table.columns:
#     print(f"列名: {column.name}, 类型: {column.type}")

# 或者使用 inspect
from sqlalchemy import inspect
inspector = inspect(engine)
schemas = inspector.get_schema_names()
for schema in schemas:
    try:
        columns = inspector.get_columns('YY_PZFL', schema=schema)
    except:
        continue
    print(schema)
