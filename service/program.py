from models.Program import get_program_by_program_id, get_program_by_program_id_and_department_id
from models.Reimbursement import get_reimbursement_by_program_id, get_reimbursement_in_transit_by_program_id
from models.ProgramFreeze import get_freeze_details
from models.LaborCost import get_labor_cost_by_program_id
from models.Voucher import get_voucher_by_department_program_id
from pydantic import BaseModel
import logging
import json

logger = logging.getLogger(__name__)

dict_subjects_code = {"0101": "设备费",
                      "0201": '材料费',
                      '0301': "测试化验加工费",
                      "0401": "燃料动力费",
                      "0501": "差旅费/会议费/国际合作与交流费",
                      "0601": "出版/文献/信息传播/知识产权事务费/印刷费/宣传费",
                      "0701": "劳务费",
                      "0801": "专家咨询费",
                      "0901": "管理费",
                      "1001": "绩效支出",
                      "1101": "科研发展基金",
                      "1201": "图书资料发",
                      "1301": "数据采集费",
                      "1401": "办公费",
                      "1501": "基础建设费",
                      "1601": "外协费",
                      "1701": "增值税及附加税费",
                      "1801": "横向科研业务费",
                      "1901": "学校科研发展基金",
                      "2001": "业务活动费"
                      }

dict_economic_classification = {
    "0101": ["3021304", "3021305", "3021399", "31002", "31003", "31006", "31007", "3021303"],
    "0201": ["30218"],
    "0301": ["3022702", "3022709", "3022701"],
    "0401": ["30225"],
    "0501": ["30212", "30215", "30216", "30239", "3029912", "30211"],
    "0601": ["3020202", "3020203", "3020204", "3020205", "3020206", "3029904", "3029916", "31022", "3020201"],
    "0701": ["3022603", "3022606", "3022699", "3022601", "30226"],
    "0801": ["3022605"],
    "0901": ["302991002", "820102"],
    "1001": ["302291001"],
    "1101": ["41504"],
    "1201": ["31099", "3020207"],
    "1301": ["3029911"],
    "1401": ["30207", "30201"],
    "1501": ["3021302", "31001", "31005", "3021301"],
    "1601": ["3022703"],
    "1701": ["30240"],
    "1801": ["30202", "30203", "30204", "30205", "30206", "30207", "30209", "30211", "30212", "30213", "30214", "30215",
             "30216",
             "30218", "30255", "3022701", "3022702", "3022709", "30239", "3029904", "3029906", "3029908", "3029911",
             "3029912",
             "3029916", "3029919", "31002", "31003", "31005", "31006", "31007", "31014", "31099", "417", "30201"],
    "1901": ["41504"],
    "2001": ["3029915"]
}


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
    dict_labor_cost_details = dict(sorted(dict_labor_cost_details.items()))
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


def get_economic_classification_cost(program_id: str, department_id: str, subjects_code: str, year: int = 2026):
    """
    获取项目劳务成本明细
    :param program_id:
    :param department_id:
    :param subjects_code:
    :return:
    """

    department_id = str(department_id)
    program_id = str(program_id)
    economic_classification_code_list = dict_economic_classification.get(subjects_code)

    if not economic_classification_code_list:
        return False
    economic_classification_results = get_voucher_by_department_program_id(department_id,
                                                                           program_id,year)

    if not economic_classification_results:
        return False
    list_economic_classification = []
    for economic_classification_result in economic_classification_results:
        for economic_classification_code in economic_classification_code_list:
            if economic_classification_result.jjflkmbh.startswith(economic_classification_code):
                if economic_classification_result in list_economic_classification:
                    continue
                list_economic_classification.append(economic_classification_result)
    sorted_by_pznm = sorted(list_economic_classification, key=lambda x: x.pznm)
    list_voucher_detail = []
    for vocher in sorted_by_pznm:
        list_voucher_detail.append(VoucherDetail(voucher_number=vocher.pznm,

                                                 program_id=vocher.xmbh,
                                                 department_id=vocher.bmbh,
                                                 abstract=vocher.zy,
                                                 subject_code=vocher.jjflkmbh,
                                                 amount=vocher.jje,

                                                 ))
    return list_voucher_detail


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


class VoucherDetail(BaseModel):
    voucher_number: str
    program_id: int
    department_id: int
    abstract: str
    subject_code: str
    amount: float
