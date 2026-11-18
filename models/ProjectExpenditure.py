from pydantic import BaseModel


class ProjectExpenditureItem(BaseModel):
    """项目支出范围单条记录"""
    department: str       # 实施部门
    financial_code: str   # 财务编号
    project_type: str     # 项目类型
    project_name: str     # 项目名称
    expenditure_desc: str # 开支说明
