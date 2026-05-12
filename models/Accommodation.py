from typing import Optional
from db import intermediate_database_engine
from sqlmodel import SQLModel, Field,Session,select


class Accommodation(SQLModel, table=True):
    __tablename__ = "t_cwxt_xszsxx"

    wybs: Optional[str] = Field(default=None, primary_key=True)  # 唯一标识
    xh: str  # 学号
    xqmc: str  # 校区名称
    sqmc: str  # 社区名称
    jzwmc: str  # 建筑物名称
    lch: str  # 楼层号
    ssfjh: str  # 宿舍房间号
    cwh: str  # 床位号
    ssdh: str  # 宿舍电话
    ruzrq: str  # 入住日期
    qcrq: str  # 迁出日期
    xwzz: str  # 校外住址
    zcdh: str  # 住处电话
    rylb: str  # 人员类别
    tstamp: str  # 时间戳

def get_accommodation_info_by_student_id(student_id: str)  :
    with Session(intermediate_database_engine) as session:
        statement = select(Accommodation).where(Accommodation.xh == student_id)
        user = session.exec(statement).all()
        return user