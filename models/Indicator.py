from sqlmodel import SQLModel, Field, select, Session
from typing import Optional, List
from db import financial_engine
from datetime import datetime


class Indicator(SQLModel, table=True):
    __tablename__ = "zw_yszbzd"
    Zbdm: Optional[str] = Field(default=None, primary_key=True)  # 指标代码
    Zbmc: str  # 指标名称
    ysnd: str  # 预算年度
    Gkxmdm: str  # 预算项目代码
    kmbh: str  # 零余额科目编号
    fhkmbh: str  #
    Lkx: str  # 功能分类
    gkjjfldm: str  # 政府预算支出经济分类代码代码
    jjflkmbh: str  # 部门预算支出经济分类编号
    Zbwh: str  # 指标文号
    Zjxzdm: str  # 资金性质编码
    Zjlydm: str
    Zbje: str  # 指标金额
    Tzje: str
    Zbye: str  # 指标余额
    Zbsm: str
    Zblxdm: str  # 指标类型编码
    Iscg: str
    Zblydm: str
    lrr: str  # 录入人
    lrrq: str  # 录入日期
    Xgr: str  # 修改人
    xgrq: str  # 修改日期
    isqy: str  # 是否启用
    zxje: str
    czbzdm: str  # 财政标准代码
    issm: str
    zbglh: str
    yszckmbh: str
    cf1: str
    cf2: str
    cf3: str
    cf4: str
    cf5: str
    lybh: str
    isfczzb: str


def check_zbdm_exists(zbdm_list: List[str]) -> dict:
    """
    检查指定的指标代码是否已经存在于数据库中

    参数:
        zbdm_list: 要检查的指标代码列表

    返回:
        dict: 包含两个键的字典:
            - "exists": 已存在的指标代码列表
            - "not_exists": 不存在的指标代码列表
    """
    if not zbdm_list:
        return {"exists": [], "not_exists": []}

    try:
        with Session(financial_engine) as session:
            # 查询数据库中已存在的指标代码
            statement = select(Indicator.Zbdm).where(Indicator.Zbdm.in_(zbdm_list))
            existing_zbdms = session.exec(statement).all()

            # 转换结果为集合以便快速查找
            existing_set = set(existing_zbdms)

            # 检查每个指标代码是否存在
            exists = []
            not_exists = []

            for zbdm in zbdm_list:
                if zbdm in existing_set:
                    exists.append(zbdm)
                else:
                    not_exists.append(zbdm)

            return {
                "exists": exists,
                "not_exists": not_exists
            }

    except Exception as e:
        print(f"检查指标代码是否存在时出错: {e}")
        # 出错时返回空列表，避免影响主流程
        return {"exists": [], "not_exists": zbdm_list}


def check_single_zbdm_exists(zbdm: str) -> bool:
    """
    检查单个指标代码是否已经存在于数据库中

    参数:
        zbdm: 要检查的指标代码

    返回:
        bool: 如果存在返回True，否则返回False
    """
    try:
        with Session(financial_engine) as session:
            statement = select(Indicator).where(Indicator.Zbdm == zbdm)
            result = session.exec(statement).first()
            return result is not None

    except Exception as e:
        print(f"检查指标代码 {zbdm} 是否存在时出错: {e}")
        return False  # 出错时默认返回False


def filter_existing_indicators(list_indicators: List[dict]) -> tuple[List[dict], List[dict]]:
    """
    过滤已存在的指标数据，返回需要插入的新数据和已存在的数据

    参数:
        list_indicators: 指标信息列表，每个元素是一个字典

    返回:
        tuple: (需要插入的新数据列表, 已存在的数据列表)
    """
    if not list_indicators:
        return [], []

    # 提取所有要检查的指标代码
    zbdm_list = []
    for indicator_data in list_indicators:
        zbdm = indicator_data.get('预算指标代码')
        if zbdm:
            zbdm_list.append(zbdm)

    # 检查哪些指标代码已存在
    check_result = check_zbdm_exists(zbdm_list)
    existing_zbdms = set(check_result["exists"])

    # 分离数据
    new_indicators = []
    existing_indicators = []

    for indicator_data in list_indicators:
        zbdm = indicator_data.get('预算指标代码')
        if zbdm and zbdm in existing_zbdms:
            existing_indicators.append(indicator_data)
        else:
            new_indicators.append(indicator_data)

    return new_indicators, existing_indicators


def insert_indicators_with_check(list_indicators: List[dict]) -> dict:
    """
    带检查的指标插入方法，避免重复插入

    参数:
        list_indicators: 指标信息列表，每个元素是一个字典

    返回:
        dict: 包含插入结果的字典，包含以下键:
            - "total": 总记录数
            - "inserted": 成功插入的记录数
            - "skipped": 跳过的记录数（已存在）
            - "failed": 失败的记录数
            - "skipped_zbdms": 跳过的指标代码列表
    """
    if not list_indicators:
        return {
            "total": 0,
            "inserted": 0,
            "skipped": 0,
            "failed": 0,
            "skipped_zbdms": []
        }

    # 过滤已存在的指标
    new_indicators, existing_indicators = filter_existing_indicators(list_indicators)

    if existing_indicators:
        print(f"发现 {len(existing_indicators)} 条已存在的指标记录，将跳过这些记录")
        # 提取已存在的指标代码
        skipped_zbdms = [ind.get('预算指标代码', '未知') for ind in existing_indicators]
        print(f"跳过的指标代码: {skipped_zbdms}")
    else:
        skipped_zbdms = []

    inserted_count = 0
    failed_count = 0

    # 插入新数据
    with Session(financial_engine) as session:
        for indicator_data in new_indicators:
            try:
                zbdm = indicator_data.get('预算指标代码', '未知')

                # 创建Indicator实例并映射字段
                indicator = Indicator(
                    Zbdm=zbdm,
                    Zbmc=indicator_data.get('预算指标名称'),
                    ysnd=indicator_data.get('预算年度'),
                    Gkxmdm=indicator_data.get('财政预算项目代码'),
                    gkjjfldm=indicator_data.get('政府支出经济分类'),
                    jjflkmbh=indicator_data.get('部门支出经济分类'),
                    Zbwh=indicator_data.get('本级指标文号'),
                    Zjxzdm=indicator_data.get('资金性质代码'),
                    Lkx=indicator_data.get('支出功能分类'),
                    Zblxdm=indicator_data.get('指标类型代码'),
                    kmbh=indicator_data.get('集中支付科目编号'),
                    czbzdm=indicator_data.get('财政标准代码'),
                    isqy=indicator_data.get('是否启用'),
                    Zbje=indicator_data.get('指标金额'),
                    Zbye=indicator_data.get('指标余额'),

                    # 以下字段在传入数据中可能不存在，设置为默认值
                    fhkmbh='',  # 没有对应数据，设为空字符串
                    Zjlydm='',  # 没有对应数据，设为空字符串
                    Tzje='0',  # 默认值为0
                    Zbsm='',  # 指标说明为空
                    Iscg='0',  # 默认不是采购
                    Zblydm='',  # 指标来源代码为空
                    lrr='系统导入',  # 录入人设为系统导入
                    lrrq=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),  # 当前时间
                    Xgr='系统导入',  # 修改人为空
                    xgrq=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),  # 修改日期为空
                    zxje='0',  # 执行金额默认为0
                    issm='0',  # 默认不是说明
                    zbglh='',  # 指标管理号为空
                    yszckmbh='',  # 预算支出科目编号为空
                    cf1='',
                    cf2='',
                    cf3='',
                    cf4='',
                    cf5='',
                    lybh='',  # 来源编号为空
                    isfczzb='0'  # 默认不是非财政指标
                )

                # 添加到session
                session.add(indicator)
                inserted_count += 1
                print(f"成功准备插入指标代码: {zbdm}")

            except Exception as e:
                failed_count += 1
                print(f"准备插入指标 {indicator_data.get('预算指标代码', '未知')} 时出错: {e}")
                continue

        try:
            # 提交所有更改到数据库
            session.commit()
            print(f"批量插入完成: 成功插入 {inserted_count} 条记录")

        except Exception as e:
            session.rollback()
            failed_count += len(new_indicators) - inserted_count
            print(f"提交到数据库时出错: {e}")

    return {
        "total": len(list_indicators),
        "inserted": inserted_count,
        "skipped": len(existing_indicators),
        "failed": failed_count,
        "skipped_zbdms": skipped_zbdms
    }


def get_batch_indicators(year: str, page: int = 1, page_size: int = 20, indicator_name: str = '',
                         total_only: bool = True) -> dict:
    """
    分页获取指标信息

    参数:
        year: 预算年度
        page: 页码，从1开始
        page_size: 每页记录数，默认20
        indicator_name: 指标名称模糊查询关键词
        total_only: 是否只返回总数，用于前端分页计算

    返回:
        dict: 包含分页信息的字典，结构如下:
        {
            "total": 总记录数,
            "total_pages": 总页数,
            "current_page": 当前页码,
            "page_size": 每页记录数,
            "data": [Indicator对象列表],  # 当前页数据
            "has_next": 是否有下一页,
            "has_prev": 是否有上一页,
            "next_page": 下一页页码（如果没有则为None）,
            "prev_page": 上一页页码（如果没有则为None）
        }
    """
    try:
        with Session(financial_engine) as session:
            # 构建基础查询语句
            statement = select(Indicator).where(Indicator.ysnd == str(year))

            if indicator_name:
                # 使用like进行模糊查询，添加通配符%
                statement = statement.where(Indicator.Zbmc.like(f"%{indicator_name}%"))

            # 如果只需要总数，则直接返回总数
            if total_only:
                total_count = session.exec(select(Indicator).where(
                    Indicator.ysnd == str(year),
                    *([Indicator.Zbmc.like(f"%{indicator_name}%")] if indicator_name else [])
                )).count()
                return {"total": total_count}

            # 获取总记录数
            total_count = session.exec(statement).count()

            # 计算总页数
            total_pages = (total_count + page_size - 1) // page_size  # 向上取整

            # 处理页码边界
            if page < 1:
                page = 1
            elif page > total_pages and total_pages > 0:
                page = total_pages

            # 计算偏移量
            offset = (page - 1) * page_size

            # 添加分页限制和排序（按指标代码排序，确保分页稳定性）
            paginated_statement = statement.offset(offset).limit(page_size).order_by(Indicator.Zbdm)

            # 执行查询
            results = session.exec(paginated_statement).all()

            # 计算是否有下一页/上一页
            has_next = page < total_pages
            has_prev = page > 1

            # 构建返回结果
            return {
                "total": total_count,
                "total_pages": total_pages if total_count > 0 else 0,
                "current_page": page,
                "page_size": page_size,
                "data": results if results else [],
                "has_next": has_next,
                "has_prev": has_prev,
                "next_page": page + 1 if has_next else None,
                "prev_page": page - 1 if has_prev else None
            }

    except Exception as e:
        print(f"获取指标信息时出错: {e}")
        # 返回空结果，避免程序崩溃
        return {
            "total": 0,
            "total_pages": 0,
            "current_page": page,
            "page_size": page_size,
            "data": [],
            "has_next": False,
            "has_prev": False,
            "next_page": None,
            "prev_page": None,
            "error": str(e)
        }


def insert_indicators(list_indicators: list):
    """
    通过传入的指标信息插入到数据库中
    :param list_indicators: 指标信息列表，每个元素是一个字典
    :return: 成功插入的记录数
    """

    inserted_count = 0

    with Session(financial_engine) as session:
        for indicator_data in list_indicators:
            try:
                # 创建Indicator实例并映射字段
                indicator = Indicator(
                    Zbdm=indicator_data.get('预算指标代码'),
                    Zbmc=indicator_data.get('预算指标名称'),
                    ysnd=indicator_data.get('预算年度'),
                    Gkxmdm=indicator_data.get('财政预算项目代码'),
                    gkjjfldm=indicator_data.get('政府支出经济分类'),
                    jjflkmbh=indicator_data.get('部门支出经济分类'),
                    Zbwh=indicator_data.get('本级指标文号'),
                    Zjxzdm=indicator_data.get('资金性质代码'),
                    Lkx=indicator_data.get('支出功能分类'),
                    Zblxdm=indicator_data.get('指标类型代码'),
                    kmbh=indicator_data.get('集中支付科目编号'),
                    czbzdm=indicator_data.get('财政标准代码'),
                    isqy=indicator_data.get('是否启用'),
                    Zbje=indicator_data.get('指标金额'),
                    Zbye=indicator_data.get('指标余额'),

                    # 以下字段在传入数据中可能不存在，设置为默认值
                    fhkmbh='',  # 没有对应数据，设为空字符串
                    Zjlydm='',  # 没有对应数据，设为空字符串
                    Tzje='0',  # 默认值为0
                    Zbsm='',  # 指标说明为空
                    Iscg='0',  # 默认不是采购
                    Zblydm='',  # 指标来源代码为空
                    lrr='系统导入',  # 录入人设为系统导入
                    lrrq=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),  # 当前时间
                    Xgr='系统导入',  # 修改人为空
                    xgrq=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),  # 修改日期为空
                    zxje='0',  # 执行金额默认为0
                    issm='0',  # 默认不是说明
                    zbglh='',  # 指标管理号为空
                    yszckmbh='',  # 预算支出科目编号为空
                    cf1='',
                    cf2='',
                    cf3='',
                    cf4='',
                    cf5='',
                    lybh='',  # 来源编号为空
                    isfczzb='0'  # 默认不是非财政指标
                )

                # 添加到session
                session.add(indicator)
                inserted_count += 1

            except Exception as e:
                print(f"插入指标 {indicator_data.get('预算指标代码', '未知')} 时出错: {e}")
                # 可以选择继续处理其他数据或抛出异常
                continue

        try:
            # 提交所有更改到数据库
            session.commit()
            print(f"成功插入 {inserted_count} 条指标记录")
            return inserted_count

        except Exception as e:
            session.rollback()
            print(f"提交到数据库时出错: {e}")
            return 0
