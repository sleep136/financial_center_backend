from sqlmodel import SQLModel, Field, select, Session
from typing import Optional
from db import financial_engine, financial_engine_2025, financial_engine_2024
from decimal import Decimal

class Voucher(SQLModel, table=True):
    """
    凭证
    """
    __tablename__ = "zwpzfl"
    pznm: str = Field(default=None, primary_key=True)  # 凭证编号
    flbh: str = Field(default=None, primary_key=True)
    kmbh: str  # 科目编号
    bmbh: str  # 部门编号
    xmbh: str  # 项目编号
    zy: str  # 摘要
    jje: Decimal  # 借金额
    dje: Decimal  # 贷金额
    wbbh: str  #
    hl: str  #
    jsbh: str
    jsdh: str
    ywrq: str
    dfdw: str
    yhdz: str
    jwb: str
    dwb: str
    dch: str
    zrr: str
    zclb: str
    zcbh: str
    gkyslxdm: str
    gklkxdm: str
    gkzclxdm: str
    gkfzdm: str
    gkxxm: str
    isgk: str
    jbr: str  # 经办人
    gkjjfldm: str
    xjyhcn: str
    sl: str
    dj: str
    xjllxm: str
    yhzh: str
    dfyh: str
    yhdm: str
    istc: str
    bankcode: str
    dfdz: str
    EDKZBM: str
    xmdmsqr: str
    xmzcsqr: str
    xjcnsqr: str
    yhcnsqr: str
    GNKMBH: str
    DWBH: str
    HTBH: str
    PJH: str
    SRBH: str
    GKYSSXDM: str
    YSKMBH: str
    ISZFK: str
    ISZCK: str
    ISXJ: str
    ISYH: str
    CF1: str
    CF2: str
    CF3: str
    CF4: str
    ktxx: str
    iszdzx: str
    bknd: str
    isjjfl: str
    jjflkmbh: str  # 经济分类编号
    ywbh: str
    jtkmbh: str
    rzdh: str
    bkdh: str
    gwkywbh: str
    isgwk: str
    cf5: str
    cf6: str
    kyxmbh: str
    wyfy: str
    kmedkzbh: str
    bmkmedkzbh: str
    cf7: str
    cf8: str
    cf9: str
    cf10: str
    sbbh: str
    Gcdm: str
    wlrq: str
    fykmbh: str
    isczzc: str
    xmgklx: str
    zysm: str


class VoucherDetail(SQLModel, table=True):
    __tablename__ = "zwpzb"
    pznm: str = Field(default=None, primary_key=True)  # 凭证编号
    kjnd: str  # 开具年度
    kjqj: str  # 开具月份
    pzrq: str    # 凭证日期
    pzbh: str   # 凭证的编号
    lxbh: str   # 类型编号
    fjzs: str
    zdr: str
    shr: str
    fhr: str
    jzr: str
    cn: str
    kjzg: str
    fhf: str
    jzf: str
    zff: str
    wzf: str
    lybh: str
    status: str
    yydh: str  # 预约单号
    ZTSX: str
    YSPZNM: str
    KJPZNM: str
    ISZZ: str
    ISXG: str
    ISSC: str
    CWSM: str
    yzm: str
    bz1: str
    bz2: str
    bz3: str
    yhdm: str
    lrrq: str  # 录入日期
    xgr: str   # 相关人
    xgrq: str
    bz4: str
    bz5: str
    bz6: str
    jbrdm: str
    dzpznm: str
    dafhr: str
    dafhf: str


def get_voucher_by_department_program_id(department_id: str, program_id: str, year: int = 2026):
    """
    通过项目编号获取项目信息，可能会查到多条
    :param program_id:
    :return:
    """
    if year == 2026:
        engine = financial_engine
    elif year == 2025:
        engine = financial_engine_2025
    elif year == 2024:
        engine = financial_engine_2024
    else:
        engine = financial_engine

    with Session(engine) as session:
        statement = select(Voucher).where(Voucher.bmbh == department_id, Voucher.xmbh == program_id)
        results = session.exec(statement).all()
        if results:
            return deduplicate_by_attrs(results, ["pznm", "kmbh"])


def get_breakdown_by_department_program_id(department_id: str, program_id: str, year: int = 2026):
    """
    通过项目编号获取预算下发明细
    :param program_id:
    :return:
    """
    if year == 2026:
        engine = financial_engine
    elif year == 2025:
        engine = financial_engine_2025
    elif year == 2024:
        engine = financial_engine_2024
    else:
        engine = financial_engine

    with Session(engine) as session:
        statement = select(Voucher).where(Voucher.bmbh == department_id, Voucher.xmbh == program_id, Voucher.dje > 0,
                                          Voucher.gklkxdm != '', Voucher.cf6 > 0)
        results = session.exec(statement).all()
        if results:
            return results

def get_breakdown_by_voucher_id(department_id: str, program_id: str, year: int = 2026):
    """
    通过项目编号获取预算下发明细
    :param program_id:
    :return:
    """
    if year == 2026:
        engine = financial_engine
    elif year == 2025:
        engine = financial_engine_2025
    elif year == 2024:
        engine = financial_engine_2024
    else:
        engine = financial_engine

    with Session(engine) as session:
        statement = select(Voucher).where(Voucher.bmbh == department_id, Voucher.xmbh == program_id, Voucher.dje > 0,
                                          Voucher.gklkxdm != '')
        results = session.exec(statement).all()
        if results:
            return results

def get_date_by_voucher_id(voucher_id_list:list, year: int = 2026):
    if year == 2026:
        engine = financial_engine
    elif year == 2025:
        engine = financial_engine_2025
    elif year == 2024:
        engine = financial_engine_2024
    else:
        engine = financial_engine

    with Session(engine) as session:
        statement = select(VoucherDetail).where(VoucherDetail.pznm.in_(voucher_id_list))
        results = session.exec(statement).all()
        if results:
            return results


def deduplicate_by_attrs(obj_list, attrs):
    """按指定属性去重，保持顺序"""
    seen = set()
    result = []

    for obj in obj_list:
        # 创建属性的元组作为唯一标识
        key = tuple(getattr(obj, attr) for attr in attrs)

        if key not in seen:
            seen.add(key)
            result.append(obj)

    return result
