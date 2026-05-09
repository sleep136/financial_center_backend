from typing import Optional
from db import financial_engine
from sqlmodel import SQLModel, Field, Session, select
from typing import Optional, List

class Person(SQLModel, table=True):
    __tablename__ = "zwzgzd"
    ygbh: Optional[str] = Field(default=None, primary_key=True)  # 人员编号
    ygmc: str  # 姓名
    bmbh: str  # 部门编号
    zjm: str
    gzbmbh: str
    gzbmmc: str
    rylbdm: str
    rylbmc: str
    rylx: str
    mobie: str
    lxdh: str
    email: str
    ickh: str
    yhzh: str
    sfzh: str
    yh1: str
    gzkh1: str
    yh2: str
    gzkh2: str
    yh3: str
    gzkh3: str
    yh4: str
    gzkh4: str
    yh5: str
    gzkh5: str
    jkcs: int
    jpcs: int
    lhh1: str
    khhmc1: str
    lhh2: str
    khhmc2: str
    lhh3: str
    khhmc3: str
    lhh4: str
    khhmc4: str
    lhh5: str
    khhmc5: str
    gwkh: str
    isok: str
    Xb: str
    YHLXDM: str
    YHLXMC: str
    YHMM: str
    BMMC: str
    TXDZ: str
    ZJLX: str
    BANK: str
    XLDM: str
    XLMC: str
    ZHIYDM: str
    ZHIYMC: str
    ZWDM: str
    ZWMC: str
    BZ: str
    ALLLOGIN: str
    JZRQ: str
    khxm: str
    zcdm: str
    zcmc: str
    lrr: str
    lrrq: str
    xgr: str
    xgrq: str


    @classmethod
    def get_all_persons(cls) -> List["Person"]:
        with Session(financial_engine) as session:
            statement = select(cls)
            return session.exec(statement).all()
