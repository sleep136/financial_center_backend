from sqlmodel import SQLModel, Field, select, Session
from typing import Optional
from db import reimbursement_engine


class Authorization(SQLModel, table=True):
    __tablename__ = "WEB_XMSQSYLOG"
    __table_args__ = {'schema': "GGK"}
    LOGID: str = Field(primary_key=True)
    BMBH: str = Field(default=None)  # 部门编号
    XMBH: str = Field(default=None)  # 项目编号
    SQRZJH: str = Field(default=None)  # 授权人账号
    BSQRZJH: str = Field(default=None)  # 被授权人账号
    MSYSTEM: str = Field(default=None)  # 系统id
    MOPERATE: str = Field(default=None)  # 操作名称
    MCZRQ: str = Field(default=None)  # 操作时间
    MIP: str = Field(default=None)  # 操作IP
    SQJE: float = Field(default=None)  # 授权金额
    QXJE: float = Field(default=None)  # 取消金额
    YSQRZID: str = Field(default=None)  # 原授权ID
    QXFLG: str = Field(default=None)  # 0：代表该log是取消操作，1：原log已取消，2：原log未取消
    XMMC: str = Field(default=None)  # 项目名称
    MAC: str = Field(default=None)  # 操作MAC
    ZTDM: str = Field(default=None)  # 状态代码


class AuthorizationDetail(SQLModel, table=True):
    __tablename__ = "WEB_XMSQSYXX"
    __table_args__ = {'schema': "GGK"}
    ZTDM: str = Field(default=None)
    YSSQJE: str = Field(default=None)
    YSQSRQ: str = Field(default=None)
    YSJZRQ: str = Field(default=None)
    YECK: str = Field(default=None)
    XMMC: str = Field(default=None)
    XMBH: str = Field(primary_key=True)
    TSLSH: str = Field(default=None)
    SYSID: str = Field(primary_key=True)
    SQSY: str = Field(default=None)
    SQRZJH: str = Field(default=None)
    SQLY: str = Field(default=None)
    SQLSH: str = Field(default=None)
    SBSQJE: str = Field(default=None)
    SBQSRQ: str = Field(default=None)
    SBJZRQ: str = Field(default=None)
    QXLSH: str = Field(default=None)
    MXZCK: str = Field(default=None)
    KZJE: str = Field(default=None)
    KYQSRQ: str = Field(default=None)
    KYJZRQ: str = Field(default=None)
    JSXX: str = Field(default=None)
    JPQSRQ: str = Field(default=None)
    JPJZRQ: str = Field(default=None)
    ISYSECSQ: str = Field(default=None)
    ISYS: str = Field(default=None)
    ISSBECSQ: str = Field(default=None)
    ISSB: str = Field(default=None)
    ISLJ: str = Field(default=None)
    ISKYECSQ: str = Field(default=None)
    ISKY: str = Field(default=None)
    ISJPECSQ: str = Field(default=None)
    ISJP: str = Field(default=None)
    ISFZRSQ: str = Field(default=None)
    ISCXECSQ: str = Field(default=None)
    ISCX: str = Field(default=None)
    ISBXECSQ: str = Field(default=None)
    ISBX: str = Field(default=None)
    CZXMBGR: str = Field(default=None)
    CZRQ: str = Field(default=None)
    CZBGR: str = Field(default=None)
    CXQSRQ: str = Field(default=None)
    CXJZRQ: str = Field(default=None)
    BXSQJE: str = Field(default=None)
    BXQSRQ: str = Field(default=None)
    BXJZRQ: str = Field(default=None)
    BSQRZJH: str = Field(primary_key=True)
    BMBH: str = Field(primary_key=True)
    BGXM: str = Field(default=None)
    BGR: str = Field(default=None)
    BBGXM: str = Field(default=None)
    BBGR: str = Field(default=None)


def get_authorization_by_program_id(program_id: str):
    """
    通过项目编号获取授权信息
    :param program_id: 项目编号
    :return:
    """
    with Session(reimbursement_engine) as session:
        statement = select(AuthorizationDetail).where(AuthorizationDetail.XMBH == int(program_id))
        results = session.exec(statement).all()
        if results:
            return results


def get_authorization_by_work_id(work_id: str):
    """
    通过被授权人账号获取授权信息
    :param work_id: 被授权人账号
    :return:
    """
    with Session(reimbursement_engine) as session:
        statement = select(AuthorizationDetail).where(AuthorizationDetail.BSQRZJH == work_id)
        results = session.exec(statement).all()
        if results:
            return results

