from pydantic import BaseModel

from models.Student import get_student_toll, get_student_info
from models.Accommodation import get_accommodation_info_by_student_id
from models.StudentStatusChange import get_change_info_by_student_id


def get_project_name(project_id):
    if project_id == "01":
        return "学费"
    elif project_id == "02":
        return "住宿费"
    elif project_id == "03":
        return "辅修学费"
    elif project_id == "04":
        return "退费"
    elif project_id == "05":
        return "结业复读生学费"
    else:
        return ""


def get_expense(student_id):
    info = get_student_info(student_id)

    tolls = get_student_toll(student_id)

    # student_accounts_receivablee = get_student_accounts_receivablee(student_id)
    dict_expense = {}
    if tolls:
        tolls = list(tolls)
        for toll in tolls:
            dict_expense.setdefault(toll.SFQJDM, [])

            dict_expense[toll.SFQJDM].append(
                {"project_name": get_project_name(toll.SFXMDM),  # 收费项目名称
                 "amount_payable": toll.YJJE,  # 应交金额
                 "amount_paid_in": toll.SJJE,  # 实缴金额
                 "refund_amount": toll.TFJE,  # 退费金额
                 "reduction_amount": toll.JMJE  # 减免金额
                 }
            )
    if info:
        dict_expense['info'] = info
    return dict_expense


def get_accommodation_info(student_id):
    infos = get_accommodation_info_by_student_id(student_id)
    list_accommodation = []
    for info in infos:
        list_accommodation.append(AccommodationInfo(
            id=info.wybs,
            student_id=info.xh,
            campus=info.xqmc,
            community=info.sqmc,
            dormitory_building=info.jzwmc,
            floor=info.lch,
            room_num=info.ssfjh,
            bed_num=info.cwh,
            check_in_date=info.ruzrq,
            check_out_date=info.qcrq,
        ))
    return list_accommodation


def get_change_info(student_id):
    infos = get_change_info_by_student_id(student_id)
    list_change = []
    for info in infos:
        list_change.append(ChangeInfo(
            student_id=info.xh,
            change_date=info.ydrq,
            change_type=info.ydlbmdmmc,
        ))
    return list_change



class AccommodationInfo(BaseModel):
    id: str
    student_id: str  # 学号
    campus: str  # 校区
    community: str  # 社区
    dormitory_building: str  # 宿舍楼
    floor: str  # 楼层
    room_num: str  # 房间号
    bed_num: str  # 床号
    check_in_date: str  # 入住日期
    check_out_date: str  # 迁出日期


class ChangeInfo(BaseModel):
    student_id: str  # 学号
    change_date: str  # 异动日期
    change_type: str  # 异动类别码名称
