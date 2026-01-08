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
        authorized_amount = authorization.SQJE if authorization.SQJE else 0
        cancelled_amount = authorization.QXJE if authorization.QXJE else 0
        list_authorizations.append(
            AuthorizationDataObject(program_name=authorization.XMMC, program_id=authorization.XMBH,
                                    department_id=authorization.BMBH
                                    , authorized_amount=authorized_amount, cancelled_amount=cancelled_amount,
                                    is_cancelled=authorization.QXFLG, authorized_person=authorization.BSQRZJH,
                                    operator=authorization.SQRZJH, operate_time=authorization.MCZRQ,
                                    abstract=authorization.MOPERATE))

    return list_authorizations


def get_authorization_info_list_by_work_id(work_id: str):
    authorizations = get_authorization_by_work_id(work_id)
    if not authorizations:
        return False
    list_authorizations = []
    for authorization in authorizations:
        authorized_amount = authorization.SQJE if authorization.SQJE else 0
        cancelled_amount = authorization.QXJE if authorization.QXJE else 0
        list_authorizations.append(
            AuthorizationDataObject(program_name=authorization.XMMC, program_id=authorization.XMBH,
                                    department_id=authorization.BMBH,
                                    authorized_amount=authorized_amount,
                                    cancelled_amount=cancelled_amount,
                                    is_cancelled=authorization.QXFLG
                                    , operate_time=authorization.MCZRQ,
                                    authorized_person=authorization.BSQRZJH, operator=authorization.SQRZJH,
                                    abstract=authorization.MOPERATE))

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
