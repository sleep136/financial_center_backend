from typing import Optional
from db import financial_engine
from sqlmodel import SQLModel, Field, Session, select
from typing import Optional, List
from sqlalchemy import Column

class Department(SQLModel, table=True):
    __tablename__ = "zwbmzd"
    bmdm: Optional[str] = Field(
        default=None,
        sa_column=Column(name="bmbh", primary_key=True)  # 主键移到这里
    )
    bmmc: str  # 部门名称
    bmxz: str
    jc: str

    @classmethod
    def get_all_departments(cls) -> List["Department"]:
        with Session(financial_engine) as session:
            statement = select(cls)
            return session.exec(statement).all()
