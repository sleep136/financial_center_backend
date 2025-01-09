from models.Student import get_student_toll
from models.User import get_user_by_id


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
    tolls = get_student_toll(student_id)

    # student_accounts_receivablee = get_student_accounts_receivablee(student_id)
    dict_expense = {}
    if tolls:
        for toll in tolls:
            dict_expense.setdefault(toll["SFQJDM"], [])

            dict_expense[toll["SFQJDM"]].append(
                {"project_name": get_project_name(toll["SFXMDM"]),  # 收费项目名称
                 "amount_payable": toll["YJJE"],  # 应交金额
                 "amount_paid_in": toll["SJJE"],  # 实缴金额
                 "refund_amount": toll["TFJE"],  # 退费金额
                 "reduction_amount": toll["JMJE"]  # 减免金额
                 }
            )
    return dict_expense

    def get_user_info(student_id):
        user = get_user_by_id(student_id)
        if not user:
            return False
        user_info = {"user_id": student_id, "user_name": user.username}
        return user_info
