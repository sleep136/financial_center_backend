from models.Program import get_program_by_program_id, get_program_by_program_id_and_department_id
from models.Reimbursement import get_reimbursement_by_program_id, get_reimbursement_in_transit_by_program_id
from models.ProgramFreeze import get_freeze_details
from models.LaborCost import get_labor_cost_by_program_id
from pydantic import BaseModel
import logging
import json

logger = logging.getLogger(__name__)


def get_program_info_list(program_id: str):
    programs = get_program_by_program_id(program_id)
    if not programs:
        return False
    list_programs = []
    for program in programs:
        list_programs.append(Program(program_name=program.xmmc, program_id=program.xmbh, department_id=program.bmbh))

    return list_programs


def get_one_program(program_id: str, department_id: str):
    program = get_program_by_program_id_and_department_id(program_id, department_id)
    if not program:
        return False

    return Program(program_name=program.xmmc, program_id=program.xmbh, department_id=program.bmbh)


def get_freeze_detail(program_id: str, department_id: str):
    """
    获取项目冻结明细
    :param program_id:
    :param department_id:
    :return:
    """
    department_id = str(department_id)
    program_id = str(program_id)
    freeze_details = get_freeze_details(department_id, program_id)
    if not freeze_details:
        return False
    list_program_details = []
    for freeze_detail in freeze_details:
        list_program_details.append(ProgramFreeze(program_id=freeze_detail.xmbh, department_id=freeze_detail.bmbh,
                                                  abstract=freeze_detail.zy,
                                                  freeze_number=freeze_detail.djje,
                                                  unfreeze_number=freeze_detail.jdje, operator=freeze_detail.sbr,
                                                  operate_time=freeze_detail.sbrq, is_review=freeze_detail.pllsh,
                                                  review_date=freeze_detail.shrq,
                                                  business_order_number=freeze_detail.ywdh,
                                                  hedge_number=freeze_detail.xgr))
    return list_program_details


def get_reimbursement_detail(program_id: int, department_id: int, filter_state: int = 1):
    """
    获取项目报销明细
    :param program_id:
    :param department_id:
    :param filter_state: 1 已处理 2 未处理
    :return:
    """
    is_filter = filter_state == 1
    reimbursement_details = get_reimbursement_by_program_id(department_id, program_id, is_filter)
    if not reimbursement_details:
        return False
    list_reimbursement_details = []
    for reimbursement in reimbursement_details:
        list_reimbursement_details.append(Reimbursement(reservation_number=reimbursement.YYDH,
                                                        business_order_number=reimbursement.YWBH,
                                                        program_id=reimbursement.XMBH,
                                                        department_id=reimbursement.BMBH,
                                                        abstract=reimbursement.ZY,
                                                        operator=reimbursement.JBR,
                                                        amount=reimbursement.JJE,
                                                        state=reimbursement.ZT).model_dump())
    return list_reimbursement_details


def get_labor_cost_detail(program_id: int, department_id: int, is_filter: int = 1):
    """
    获取项目劳务成本明细
    :param program_id:
    :param department_id:
    :param filter_state: 1 已处理 2 未处理
    :return:
    """
    is_filter = is_filter == 1
    on_campus_results, off_campus_results, student_cost_results = get_labor_cost_by_program_id(department_id,
                                                                                               program_id,
                                                                                               is_filter)
    logger.info(
        f"on_campus_results: {on_campus_results} off_campus_results: {off_campus_results} student_cost_results: {student_cost_results} ")

    dict_labor_cost_details = {}
    list_labor_cost_details = []
    for labor_cost in on_campus_results:
        if labor_cost.LSH in dict_labor_cost_details:
            dict_labor_cost_details[labor_cost.LSH]['amount'] = dict_labor_cost_details[labor_cost.LSH][
                                                                    'amount'] + labor_cost.JE
        else:
            dict_labor_cost_details[labor_cost.LSH] = {'amount': labor_cost.JE,
                                                       'business_order_number': labor_cost.XUHAO,
                                                       'program_id': labor_cost.XMBH,
                                                       'department_id': labor_cost.BMBH,
                                                       'abstract': labor_cost.ZY,
                                                       'operator': labor_cost.JBR,
                                                       'state': labor_cost.STATE,
                                                       'type': 1  # 1: 校内劳务 2: 校外劳务 3: 学生劳务
                                                       }

    for labor_cost in off_campus_results:
        if labor_cost.LSH in dict_labor_cost_details:
            dict_labor_cost_details[labor_cost.LSH]['amount'] = dict_labor_cost_details[labor_cost.LSH][
                                                                    'amount'] + labor_cost.JE
        else:
            dict_labor_cost_details[labor_cost.LSH] = {'amount': labor_cost.JE,
                                                       'business_order_number': labor_cost.XUHAO,
                                                       'program_id': labor_cost.XMBH,
                                                       'department_id': labor_cost.BMBH,
                                                       'abstract': labor_cost.ZY,
                                                       'operator': labor_cost.JBR,
                                                       'state': labor_cost.STATE,
                                                       'type': 2  # 1: 校内劳务 2: 校外劳务 3: 学生劳务
                                                       }
    for labor_cost in student_cost_results:
        if labor_cost.LSH in dict_labor_cost_details:
            dict_labor_cost_details[labor_cost.LSH]['amount'] = dict_labor_cost_details[labor_cost.LSH][
                                                                    'amount'] + labor_cost.JE
        else:
            dict_labor_cost_details[labor_cost.LSH] = {'amount': labor_cost.JE,
                                                       'business_order_number': labor_cost.XUHAO,
                                                       'program_id': labor_cost.XMBH,
                                                       'department_id': labor_cost.BMBH,
                                                       'abstract': labor_cost.ZY,
                                                       'operator': labor_cost.JBR,
                                                       'state': labor_cost.STATE,
                                                       'type': 3  # 1: 校内劳务 2: 校外劳务 3: 学生劳务
                                                       }

    for k, v in dict_labor_cost_details.items():
        list_labor_cost_details.append(LaborCost(labor_number=k,
                                                 business_order_number=v['business_order_number'],
                                                 program_id=v['program_id'],
                                                 department_id=v['department_id'],
                                                 abstract=v['abstract'],
                                                 operator=v['operator'],
                                                 state=v['state'],
                                                 amount=v['amount'],
                                                 type=v['type'],
                                                 ))
    return list_labor_cost_details


class Program(BaseModel):
    program_name: str
    program_id: str
    department_id: str


class ProgramFreeze(BaseModel):
    program_id: str
    department_id: str
    abstract: str
    freeze_number: float
    unfreeze_number: float
    operator: str
    operate_time: str
    is_review: str
    review_date: str
    business_order_number: str
    hedge_number: str


class Reimbursement(BaseModel):
    reservation_number: str
    business_order_number: str
    program_id: int
    department_id: int
    abstract: str
    operator: str
    amount: float
    state: int


class LaborCost(BaseModel):
    labor_number: str
    business_order_number: int
    program_id: int
    department_id: int
    abstract: str
    operator: str
    state: str
    amount: float
    type: int  # 1: 校内劳务 2: 校外劳务 3: 学生劳务
