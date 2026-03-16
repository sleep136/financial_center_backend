import logging
import pandas as pd
from models.Voucher import get_breakdown_by_department_program_id, get_date_by_voucher_id
from pydantic import BaseModel
import datetime

logger = logging.getLogger(__name__)


def get_budget_breakdown(program_id: str, department_id: str, year: int = 2026):
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


class VoucherDetail(BaseModel):
    voucher_date: str
    voucher_number: str
    program_id: int
    department_id: int
    abstract: str
    amount: float
    operator: str
