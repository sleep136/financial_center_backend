from sqlmodel import SQLModel, Field, select, Session
from typing import Optional
from db import financial_engine


class Program(SQLModel, table=True):
    __tablename__ = "zwxmzd"
    xmnm: Optional[str] = Field(default=None)
    bmbh: Optional[str] = Field(default=None, primary_key=True)  # 部门编号
    xmbh: Optional[str] = Field(default=None, primary_key=True)  # 项目编号
    xmmc: str  # 项目编号
    lbbh: str  # 类别编号
    jc: str  # 简称？
    mx: str  # 是否明细
    kgrq: str  # 开工日期
    wgrq: str  # 完工日期
    wgf: str
    fzr: str  # 负责人
    czf: str  # 是否超支
    czje: float  # 超支金额
    madd: str
    tcode: str
    qyf: str
    fkf: str
    ic_id: str
    fkr: str
    xmmm: str
    srkm: str  # 收入科目
    zckm: str  #
    bz: str
    zzlx: str
    isfb: str  # 是否发布
    fzrbh: str
    xmlx: str
    flsx1: str
    flsx2: str
    flsx3: str
    czy: str
    czrq: str
    gkxxm: str
    xmjc: str
    CCLASS: str
    EDBMBH: str
    EDXMBH: str
    ISGK: str
    KYXMBH: str
    ZJE: float
    XMQC: str
    ZXBH: str
    XMLYM: str
    MJM: str
    CJXS: str
    GCDM: str
    ZTZJE: str
    TZGCDM: str
    TZLYDM: str
    JZMJ: int
    DWBH: str
    YSNDXX: str
    XMYSSX: str
    CX1: str
    CX2: str
    CX3: str
    CX4: str
    BZLX: str
    isfnd: str
    iszdzx: str
    isedkz: str
    jjflzckm: str
    czzckm: str
    YSZCZJLYBH: str
    YSLXBH: str
    YSXMLBBH: str
    BMYSXMBM: str
    YSSRZJLYBH: str
    ISZFCG: str
    ZFCGLBBH: str
    EDFLBH: str
    isdx: str
    gkbmbh: str
    jkcs: int
    iszxm: str
    zbmbh: str
    zxmbh: str
    jtbh: str
    jtrq: str
    isjt: str
    djje: float  # 冻结金额
    gkxmdm: str
    xmfl: str
    yszclxbh: str
    xmsx: str
    jtmbbh: str
    nosrkm: str
    nozckm: str
    nojjflkm: str
    isczzc: str
    yslx: str
    lkx: str
    yssrkm: str
    yszckm: str
    gclxdm: str
    gcxzdm: str
    gcgmdm: str
    gcytdm: str
    gcjsdm: str
    gcjspfdm: str
    gcgcdm: str
    sbfldm: str
    gcfl: str
    jzjysx: str
    xgr: str
    xgrq: str
    fadm: str
    xmgklx: str
    iswbzdy1: str
    iswbzdy2: str
    iswbzdy3: str
    lybh: str
    pch: str
    zxdm: str
    bknd: str
    pch_jx: str
    jpcs: int
    isjz: str
    iszb: str
    isssbk: str


def get_program_by_program_id(program_id: str):
    """
    通过项目编号获取项目信息，可能会查到多条
    :param program_id:
    :return:
    """
    with Session(financial_engine) as session:
        statement = select(Program).where(Program.xmbh == program_id)
        results = session.exec(statement).all()
        if results:
            return results


def get_program_by_program_id_and_department_id(program_id: str, department_id: str):
    """
    通过项目编号和部门标号获取项目信息，
    :param program_id:
    :return:
    """
    with Session(financial_engine) as session:
        statement = select(Program).where(Program.xmbh == program_id, Program.bmbh == department_id)
        results = session.exec(statement)
        if results:
            for row in results:
                return row

# Program.metadata.create_all(financial_engine)
