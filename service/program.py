from models.Program import get_program_by_program_id, get_program_by_program_id_and_department_id
from models.Reimbursement import get_reimbursement_by_program_id, get_reimbursement_in_transit_by_program_id
from models.ProgramFreeze import get_freeze_details
from pydantic import BaseModel


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


def get_reimbursement_detail(program_id: str, department_id: str):
    """
    获取项目报销明细
    :param program_id:
    :param department_id:
    :return:
    """
    reimbursement_details = get_reimbursement_by_program_id(department_id, program_id)
    if not reimbursement_details:
        return False
    list_reimbursement_details = []
    for reimbursement in reimbursement_details:
        list_reimbursement_details.append(Reimbursement(reservation_number=reimbursement.yydh,
                                                        business_order_number=reimbursement.ywdh,
                                                        program_id=reimbursement.xmbh,
                                                        department_id=reimbursement.bmbh,
                                                        abstract=reimbursement.zy,
                                                        operator=reimbursement.jbr,
                                                        state=reimbursement.zt))
    return list_reimbursement_details


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
    program_id: str
    department_id: str
    abstract: str
    operator: str
    state: str
