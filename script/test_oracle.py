import logging
from sqlalchemy import create_engine, text, inspect
from sqlalchemy.orm import sessionmaker


def diagnose_empty_results(connection_string, table_name):
    """诊断空结果问题的完整脚本"""

    # 启用 SQL 日志
    logging.basicConfig()
    logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

    # 创建引擎
    engine = create_engine(connection_string, echo=True)

    print("=" * 50)
    print("开始诊断空结果问题")
    print("=" * 50)

    # 1. 检查连接
    print("\n1. 检查数据库连接...")
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT user, sysdate FROM dual"))
            user, sysdate = result.fetchone()
            print(f"   ✓ 连接成功 - 用户: {user}, 系统时间: {sysdate}")
    except Exception as e:
        print(f"   ✗ 连接失败: {e}")
        return

    # 2. 检查表是否存在
    print(f"\n2. 检查表 '{table_name}'...")
    inspector = inspect(engine)
    schemas = inspector.get_schema_names()

    table_found = False
    for schema in schemas:
        tables = inspector.get_table_names(schema=schema)
        if table_name.upper() in [t.upper() for t in tables]:
            print(f"   ✓ 表存在 - Schema: {schema}, 表名: {table_name}")
            table_found = True
            break

    if not table_found:
        print(f"   ✗ 表不存在或找不到")
        print(f"   可用的 Schema: {schemas}")
        return

    # 3. 检查表结构
    print(f"\n3. 检查表结构...")
    try:
        columns = inspector.get_columns(table_name)
        print(f"   表有 {len(columns)} 列:")
        for col in columns:
            print(f"     - {col['name']}: {col['type']}")
    except Exception as e:
        print(f"   获取列信息失败: {e}")

    # 4. 直接执行 SQL 查询
    print(f"\n4. 直接执行 SQL 查询...")
    with engine.connect() as conn:
        # 查询行数
        count_result = conn.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
        row_count = count_result.scalar()
        print(f"   表中有 {row_count} 行数据")

        if row_count > 0:
            # 查询前几行数据
            sample_result = conn.execute(text(f"SELECT * FROM {table_name} WHERE ROWNUM <= 5"))
            print(f"   前 {min(5, row_count)} 行数据示例:")
            for i, row in enumerate(sample_result):
                print(f"     行 {i + 1}: {dict(row._mapping)}")

    # 5. 使用 ORM 查询
    print(f"\n5. 使用 SQLAlchemy ORM 查询...")
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # 反射表
        from sqlalchemy import Table, MetaData
        metadata = MetaData()
        table = Table(table_name, metadata, autoload_with=engine)

        # 使用 ORM 查询
        from sqlalchemy.sql import select
        stmt = select(table).limit(5)
        result = session.execute(stmt)

        orm_results = result.fetchall()
        print(f"   ORM 查询到 {len(orm_results)} 行数据")

        if orm_results:
            print(f"   ORM 查询结果示例:")
            for i, row in enumerate(orm_results):
                print(f"     行 {i + 1}: {dict(row._mapping)}")
        else:
            print(f"   ⚠️ ORM 查询返回空结果")

            # 对比 SQL
            print(f"\n6. 对比 SQL 语句...")
            print(f"   ORM 生成的 SQL: {stmt}")

    except Exception as e:
        print(f"   ORM 查询失败: {e}")
    finally:
        session.close()

    print("\n" + "=" * 50)
    print("诊断完成")
    print("=" * 50)


# 使用示例
if __name__ == "__main__":
    import oracledb

    # 在应用启动时启用厚模式
    oracledb.init_oracle_client(lib_dir="D:\instantclient_11_2")
    connection_string = "oracle+oracledb://ghwsyy:ghwsyy@172.31.22.229:1521/ORCL"
    table_name = "YY_PZFL"
    diagnose_empty_results(connection_string, table_name)