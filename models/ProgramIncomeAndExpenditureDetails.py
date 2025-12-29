from sqlmodel import SQLModel, Field, select, Session
from typing import Optional
from db import financial_engine


class ProgramIncomeAndExpenditureDetails(SQLModel, table=True):
    """
    项目收支明细
    """
    __tablename__ = "temp_xmszmxz_wwc"

    bmbh: Optional[str] = Field(default=None, primary_key=True)  # 部门编号
    bmmc: Optional[str] = Field(default=None)  # 部门名称
    xmbh: Optional[str] = Field(default=None, primary_key=True)  # 项目编号
    xmmc: str  # 项目编号
    fzr: str  # 负责人
    pznm: str  # 凭证数
    zy: str  # 摘要
    pzrq: str  # 凭证日期
    kjnd: str  # 开工年度
    kjqj: str  # 开工日期
    lxbh: str  # 类别编号
    pzbh: str  # 凭证编号
    kmhbh: str  # 科目编号
    kmmch: str  # 科目名称
    jjflkmbh: str  # 交易方向科目编号
    jjflkmmc: str  # 交易方向科目名称
    zfjje: float
    zfdje: float  # 资产负债金额
    jje: float  # 交易金额
    dje: float  # 资产负债金额
    ye: float  # 余额
    bh: str  # 编号
    xh: str  # 序号
    flag: str  # 标志
