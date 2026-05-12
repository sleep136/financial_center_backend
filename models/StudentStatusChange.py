from typing import Optional
from db import intermediate_database_engine
from sqlmodel import SQLModel, Field, Session, select
from sqlalchemy import UniqueConstraint


class StudentStatusChange(SQLModel, table=True):
    __tablename__ = "t_cwxt_bksxjydxx"

    xh: Optional[str] = Field(default=None, max_length=100, primary_key=True, description="学号")
    ydrq: Optional[str] = Field(default=None, max_length=20, primary_key=True, description="异动日期")
    ydlbm: Optional[str] = Field(default=None, max_length=10, primary_key=True, description="异动类别码")
    ydlbmdmmc: Optional[str] = Field(default=None, max_length=255, description="异动类别码名称")
    ydyym: Optional[str] = Field(default=None, max_length=10, description="异动原因码")
    ydyymdmmc: Optional[str] = Field(default=None, max_length=255, description="异动原因码名称")
    sprq: Optional[str] = Field(default=None, max_length=20, description="审批日期")
    spwh: Optional[str] = Field(default=None, max_length=100, description="审批文号")
    ydsm: Optional[str] = Field(default=None, max_length=100, description="异动说明")
    yyxbm: Optional[str] = Field(default=None, max_length=100, description="原院系编码")
    yzybm: Optional[str] = Field(default=None, max_length=100, description="原专业编码")
    ybjbm: Optional[str] = Field(default=None, max_length=100, description="原班级编码")
    ynj: Optional[str] = Field(default=None, max_length=100, description="原年级")
    yxz: Optional[str] = Field(default=None, max_length=100, description="原学制")
    xyxbm: Optional[str] = Field(default=None, max_length=100, description="现院系编码")
    xzybm: Optional[str] = Field(default=None, max_length=100, description="现专业编码")
    xbjbm: Optional[str] = Field(default=None, max_length=100, description="现班级编码")
    xnj: Optional[str] = Field(default=None, max_length=100, description="现年级")
    xxz: Optional[str] = Field(default=None, max_length=100, description="现学制")
    tstamp: Optional[str] = Field(default=None, max_length=20, description="时间戳")
    xn: Optional[str] = Field(default=None, max_length=100, description="学年")
    xqm: Optional[str] = Field(default=None, max_length=20, description="学期码")
    xq: Optional[str] = Field(default=None, max_length=4, description="学期")

    class Config:
        from_attributes = True

    # 如果需要显式指定复合主键约束（可选）
    __table_args__ = (
        UniqueConstraint('xh', 'ydrq', 'ydlbm', name='uq_xh_ydrq_ydlbm'),
    )

def get_change_info_by_student_id(student_id: str)  :
    with Session(intermediate_database_engine) as session:
        statement = select(StudentStatusChange).where(StudentStatusChange.xh == student_id)
        infos = session.exec(statement).all()
        return infos