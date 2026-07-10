import logging
import pandas as pd
from models.Voucher import get_breakdown_by_department_program_id, get_date_by_voucher_id
from pydantic import BaseModel
import datetime

logger = logging.getLogger(__name__)


def get_budget_breakdown(program_id: str, department_id: str, year: int = 2026,
                         start_month: str = '0', end_month: str = '13'):
    """
    获取项目劳务成本明细
    :param program_id:
    :param department_id:
    :return:
    """

    department_id = str(department_id)
    program_id = str(program_id)

    voucher_results = get_breakdown_by_department_program_id(department_id, program_id, year)

    if not voucher_results:
        return False
    list_pznm_id = []
    for voucher_result in voucher_results:
        list_pznm_id.append(voucher_result.pznm)
    list_pznm_id = list(set(list_pznm_id))
    budget_date_list = get_date_by_voucher_id(list_pznm_id, year)
    dict_budget_date = {}
    for budget_date in budget_date_list:
        dict_budget_date[budget_date.pznm] = budget_date
    list_voucher_detail = []
    for vocher in voucher_results:
        vocher_detail = dict_budget_date[vocher.pznm]
        if int(vocher_detail.kjqj) > int(end_month) or int(vocher_detail.kjqj) < int(start_month):
            continue
        voucher_id = vocher_detail.pzbh
        type_id = vocher_detail.lxbh
        date = vocher_detail.pzrq
        list_voucher_detail.append(VoucherDetail(voucher_number='(' + str(type_id) + ')' + str(voucher_id),
                                                 voucher_date=date[:4] + "-" + date[4:6] + '-' + date[6:8],
                                                 program_id=program_id,
                                                 department_id=vocher.bmbh,
                                                 abstract=vocher.zy,
                                                 operator=vocher_detail.xgr,
                                                 amount=vocher.dje
                                                 ))
    return list_voucher_detail


def get_budget_stats(df_input1):
    """
    统计所有项目的预算数据
    :param df_input1:
    :return:
    """

    list_output = []
    list_error = []
    for index, item in df_input1.iterrows():
        try:
            list_budget = get_budget_breakdown(item['财务编号'], item['部门编号'])
            total = sum(item.amount for item in list_budget)
            list_output.append({'program_id':item['财务编号'], 'department_id':item['部门编号'], 'total':total, 'detail':list_budget})
        except Exception as e:
            logger.error(e)
            list_error.append(f"财务编号：{item['财务编号']}部门编号：{item['部门编号']} 数据异常")
    return list_output, list_error


def find_null_values(df):
    """
    查找并返回所有空值的详细位置
    """
    null_info = []

    # 遍历DataFrame的每一行
    for idx, row in df.iterrows():
        indicator_id = row['财务编号']  # 获取指标ID
        null_cols = []

        # 检查该行各列是否为空
        for col in df.columns:
            if pd.isna(row[col]):
                null_cols.append(col)
            elif pd.isna(row['部门编号']):
                null_cols.append(col)

        # 如果该行有空值，记录信息
        if null_cols:
            null_info.append({
                '财务编号': indicator_id,
                '空值列': null_cols,
                '空值数量': len(null_cols),
                '行索引': idx
            })

    return null_info


class VoucherDetail(BaseModel):
    voucher_date: str
    voucher_number: str
    program_id: int
    department_id: int
    abstract: str
    amount: float
    operator: str
