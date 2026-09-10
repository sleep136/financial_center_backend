from sqlmodel import SQLModel, Field, select, Session
from typing import Optional
from db import financial_engine,purchase_database_engine
from datetime import datetime
from decimal import Decimal
from typing import Optional

from sqlalchemy import BigInteger, Column, Index, Numeric

class ProgramFreeze(SQLModel, table=True):
    """
    项目冻结明细
    """
    __tablename__ = "zw_xmdjmx"
    id: Optional[int] = Field(default=None, primary_key=True)
    rq: str  # 日期
    bmbh: str = Field(default=None, primary_key=True)  # 部门编号
    xmbh:str = Field(default=None, primary_key=True)  # 项目编号
    zy: str  # 摘要
    djje: float  # 冻结金额
    jdje: float  # 解冻金额
    lrr: str  # 录入人
    issh: str  # 是否审核
    shrq: str  # 审核日期
    shr: str  # 审核人
    pllsh: str  # 平台审核状态
    ywdh: str  # 业务编号
    sbr: str  # 提交人
    sbrq: str  # 提交日期
    lybh: str  # 来源编号
    yydh: str  # 业务编号
    xgr: str  # 对冲号
    xgrq: str  # 预约单号
    ywid: str  # 业务编号


def get_freeze_details(department_id: str, program_id: str):
    """
    通过项目编号获取项目信息，可能会查到多条
    :param program_id:
    :return:
    """
    with Session(financial_engine) as session:
        statement = select(ProgramFreeze).where(ProgramFreeze.xmbh == program_id, ProgramFreeze.bmbh == department_id)
        results = session.exec(statement).all()
        if results:
            return results


class ZcyJhJf(SQLModel, table=True):
    """采购计划经费表"""

    __tablename__ = "zcy_jh_jf"

    __table_args__ = (
        Index("fk_zcy_jh_jf_zcy_jf_1", "jf_id"),
        Index("zcy_jh_jf_jf_id_IDX", "jf_id", "jf_mx_id"),
        Index("idx_zcy_jh_jf_jh_id", "jh_id"),
    )

    # 原 DDL：bigint NOT NULL 主键，无 AUTO_INCREMENT，因此关闭自增，插入时需显式传 id
    id: int = Field(
        sa_column=Column(BigInteger, primary_key=True, autoincrement=False),
        description="主键",
    )
    jf_id: Optional[int] = Field(default=None, sa_column=Column(BigInteger), description="经费id")
    jf_mx_id: Optional[int] = Field(default=None, sa_column=Column(BigInteger), description="经费明细id")
    jf_xm_id: Optional[int] = Field(default=None, sa_column=Column(BigInteger), description="经费项目id")
    jh_id: Optional[int] = Field(default=None, sa_column=Column(BigInteger), description="计划id")

    jf_name: Optional[str] = Field(default=None, max_length=100, description="经费名称")
    jf_no: Optional[str] = Field(default=None, max_length=50, description="经费编号")
    jf_year: Optional[str] = Field(default=None, max_length=50, description="经费年度")
    jf_glbm: Optional[str] = Field(default=None, max_length=128, description="经费管理部门")
    jf_glbmbm: Optional[str] = Field(default=None, max_length=64, description="经费管理部门编码")
    jf_code: Optional[str] = Field(default=None, max_length=50, description="经费编码")
    jf_ed_name: Optional[str] = Field(default=None, max_length=128, description="额度名称")
    jf_ed_no: Optional[str] = Field(default=None, max_length=64, description="额度编号")
    jf_xm_name: Optional[str] = Field(default=None, max_length=100, description="经费项目名称")
    jf_fzr: Optional[str] = Field(default=None, max_length=64, description="经费负责人")
    jf_fzryhm: Optional[str] = Field(default=None, max_length=32, description="经费负责人用户名")
    jf_fgld: Optional[str] = Field(default=None, max_length=64, description="分管领导")
    jf_fgldyhm: Optional[str] = Field(default=None, max_length=32, description="分管领导用户名")
    jf_pmbm: Optional[str] = Field(default=None, max_length=32, description="经费品目编码")
    jf_pmmc: Optional[str] = Field(default=None, max_length=64, description="经费品目名称")
    jf_zckmbm: Optional[str] = Field(default=None, max_length=64, description="支出科目编码")

    syje: Optional[Decimal] = Field(default=None, sa_column=Column(Numeric(12, 2)), description="本项目使用预算")
    jf_is_cwxt: int = Field(default=0, sa_column_kwargs={"server_default": "0"}, description="是否财务系统经费")
    jf_cwxt_djje: Optional[Decimal] = Field(default=None, sa_column=Column(Numeric(12, 2)), description="财务系统冻结金额")
    jf_is_xdjf: int = Field(default=1, sa_column_kwargs={"server_default": "1"}, description="是否下达经费")
    jf_cwxt_djjf: Optional[Decimal] = Field(default=None, sa_column=Column(Numeric(12, 2)), description="财务系统经费冻结经费")

    creator: Optional[int] = Field(default=None, sa_column=Column(BigInteger), description="创建人")
    create_date: Optional[datetime] = Field(default=None, description="创建时间")
    updater: Optional[int] = Field(default=None, sa_column=Column(BigInteger), description="更新人")
    update_date: Optional[datetime] = Field(default=None, description="更新时间")

    jh_jf_xmlx: Optional[str] = Field(default=None, max_length=16, description="项目类型")
    jh_jf_bak1: Optional[str] = Field(default=None, max_length=64, description="财务系统经费id")
    jh_jf_bak2: Optional[str] = Field(default=None, max_length=64, description="财务系统部门编码")
    jh_jf_bak3: Optional[str] = Field(default=None, max_length=64, description="二期id")
    jh_jf_bak4: Optional[str] = Field(default=None, max_length=64, description="额度编码")
    jh_jf_bak5: Optional[str] = Field(default=None, max_length=64, description="冻结单号")
    jh_jf_bak6: Optional[str] = Field(default=None, max_length=32, description="备用字段6")
    jh_jf_bak7: Optional[str] = Field(default=None, max_length=32, description="备用字段7")
    jh_jf_bak8: Optional[str] = Field(default=None, max_length=32, description="备用字段8")
    jh_jf_bak9: Optional[str] = Field(default=None, max_length=32, description="备用字段9")
    jh_jf_bak10: Optional[str] = Field(default=None, max_length=32, description="备用字段10")
    jh_jf_bak11: Optional[Decimal] = Field(default=None, sa_column=Column(Numeric(12, 2)), description="备用字段11")
    jh_jf_bak12: Optional[Decimal] = Field(default=None, sa_column=Column(Numeric(12, 2)), description="备用字段12")
    jh_jf_bak13: Optional[Decimal] = Field(default=None, sa_column=Column(Numeric(12, 2)), description="备用字段13")

    old_jh_jf_id: Optional[str] = Field(default=None, max_length=32, description="旧系统id")
    jf_freeze_no: str = Field(
        default="",
        sa_column_kwargs={"server_default": "''"},
        max_length=100,
        description="经费冻结编码",
    )

def get_purchase_plannings(program_id: str)  :
    """
    通过项目编号获取对应的采购计划 id（jh_id），可能返回多条。

    :param program_id: 项目编号
    :return: 计划 id 列表，无匹配数据时返回空列表
    """
    if not program_id:
        return []

    with Session(purchase_database_engine) as session:
        statement = (
            select(ZcyJhJf)
            .where(
                ZcyJhJf.jf_no == str(program_id),
                ZcyJhJf.jh_id.is_not(None)

            )

        )
        return session.exec(statement).all()
