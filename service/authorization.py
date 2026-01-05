from pydantic import BaseModel
from models.Authorization import get_authorization_by_program_id
import logging

logger = logging.getLogger(__name__)


def get_authorization_info_list(program_id: str):
    authorizations = get_authorization_by_program_id(program_id)
    if not authorizations:
        return False
    list_authorizations = []
    for authorization in authorizations:
        list_authorizations.append(
            AuthorizationDataObject(program_name=authorization.XMMC, program_id=authorization.XMBH,
                                    department_id=authorization.BMBH
                                    , authorized_person=authorization.BSQRZJH, operator=authorization.SQRZJH,
                                    abstract=authorization.MOPERATE))

    return list_authorizations


class AuthorizationDataObject(BaseModel):
    program_id: int
    department_id: int
    program_name: str
    authorized_person: str  # 被授权人
    operator: str
    amount: float  # 授权金额
    is_cancelled: str  # 是否取消
    abstract: str  # 摘要
