from pydantic import BaseModel
from models.Authorization import get_authorization_by_program_id, get_authorization_by_work_id
import logging

logger = logging.getLogger(__name__)


def get_authorization_info_list_by_program_id(program_id: str):
    authorizations = get_authorization_by_program_id(program_id)
    if not authorizations:
        return False
    list_authorizations = []
    for authorization in authorizations:
        authorization_type = ''
        start_time = ''
        end_time = ''
        authorized_amount = 0

        cancelled_amount = 0

        if authorization.ISCX:
            authorization_type = "网络查询"
            start_time = authorization.CXQSRQ
            end_time = authorization.CXJZRQ
        elif authorization.ISBX:
            authorization_type = "网报"
            start_time = authorization.BXQSRQ
            end_time = authorization.BXJZRQ
            authorized_amount = authorization.BXSQJE
        elif authorization.ISSB:
            authorization_type = "劳务申报"
            start_time = authorization.SBQSRQ
            end_time = authorization.SBJZRQ
            authorized_amount = authorization.SBSQJE
        else:
            authorization_type = "未知"
        list_authorizations.append(
            AuthorizationDataObject(program_name=authorization.XMMC, program_id=authorization.XMBH,
                                    department_id=authorization.BMBH,
                                    authorized_amount=authorized_amount,
                                    cancelled_amount=0,
                                    is_cancelled=authorization.SQSY,
                                    operate_time=authorization.CZRQ,
                                    authorized_person=authorization.BSQRZJH, operator=authorization.SQRZJH,
                                    abstract="",
                                    start_time=start_time,
                                    end_time=end_time,
                                    authorization_type=authorization_type

                                    ))
    return list_authorizations


def get_authorization_info_list_by_work_id(work_id: str):
    authorizations = get_authorization_by_work_id(work_id)
    if not authorizations:
        return False
    list_authorizations = []
    for authorization in authorizations:
        authorization_type = ''
        start_time = ''
        end_time = ''
        authorized_amount = 0

        cancelled_amount = 0

        if authorization.ISCX:
            authorization_type = "网络查询"
            start_time = authorization.CXQSRQ
            end_time = authorization.CXJZRQ
        elif authorization.ISBX:
            authorization_type = "网报"
            start_time = authorization.BXQSRQ
            end_time = authorization.BXJZRQ
            authorized_amount = authorization.BXSQJE
        elif authorization.ISSB:
            authorization_type = "劳务申报"
            start_time = authorization.SBQSRQ
            end_time = authorization.SBJZRQ
            authorized_amount = authorization.SBSQJE
        else:
            authorization_type = "未知"
        list_authorizations.append(
            AuthorizationDataObject(program_name=authorization.XMMC, program_id=authorization.XMBH,
                                    department_id=authorization.BMBH,
                                    authorized_amount=authorized_amount,
                                    cancelled_amount=0,
                                    is_cancelled=authorization.SQSY,
                                    operate_time=authorization.CZRQ,
                                    authorized_person=authorization.BSQRZJH, operator=authorization.SQRZJH,
                                    abstract="",
                                    start_time=start_time,
                                    end_time=end_time,
                                    authorization_type=authorization_type

                                    ))

    return list_authorizations


class AuthorizationDataObject(BaseModel):
    program_id: int
    department_id: int
    program_name: str
    authorized_person: str  # 被授权人
    operator: str
    authorized_amount: float = 0.0  # 授权金额
    cancelled_amount: float = 0.0  # 取消金额
    operate_time: str  # 操作时间
    is_cancelled: str  # 是否取消
    abstract: str  # 摘要
    start_time: str
    end_time: str
    authorization_type: str
