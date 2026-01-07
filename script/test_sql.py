import pymssql
import sys


def test_connection():
    try:
        # 尝试基本连接
        conn = pymssql.connect(
            server='172.31.22.168',  # 服务器IP
            user='tc_gxcw60',  # 刚创建的账户
            password='gxcw60',  # 密码
            database='gxcw60',  # 数据库名
            port=1433,  # 默认端口
            timeout=10,  # 连接超时
            as_dict=True  # 返回字典格式
        )

        print("✅ 连接成功!")

        # 执行简单查询测试
        cursor = conn.cursor()
        cursor.execute("SELECT @@VERSION as version")
        row = cursor.fetchone()
        print(f"SQL Server 版本: {row['version']}")

        conn.close()
        return True

    except pymssql.OperationalError as e:
        print(f"❌ 连接失败: {e}")

        # 提供更具体的诊断建议
        error_msg = str(e)
        if '18456' in error_msg:
            print("\n🔍 18456 错误诊断建议:")
            print("1. 确认用户名/密码正确")
            print("2. 确认SQL Server启用了混合认证模式")
            print("3. 确认账户未被禁用或锁定")
            print("4. 确认密码没有过期")
            print("5. 在SSMS中测试该账户是否能登录")

        return False
    except Exception as e:
        print(f"❌ 其他错误: {e}")
        return False


if __name__ == "__main__":
    test_connection()