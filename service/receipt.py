from models.Receipt import get_recipe, get_recipe_url
from pydantic import BaseModel


def get_recipe_info_list(work_id: str = '', user_name: str = '', company_name: str = ''):
    recipes = get_recipe(work_id, user_name, company_name)
    if not recipes:
        return False
    list_recipes = []
    for recipe in recipes:
        list_recipes.append(
            ReceiptData(serial_num=recipe.ID, operator_id=recipe.JPRGZH, operator_name=recipe.JPRXM,
                        department_id=recipe.BMBH if recipe.BMBH else '',
                        company_name=recipe.DFDWMC, create_time=recipe.CREATE_TIME.strftime('%Y-%m-%d %H:%M:%S'),
                        contract_num=recipe.HTBH if recipe.HTBH else '',
                        program_name=recipe.XMMC, amount=recipe.BCKPJE,
                        recipe_type=recipe.PJLXMC, approval_state=recipe.STATUS,
                        reason=recipe.REASON if recipe.REASON else '',
                        system_msg=recipe.RET_MSG if recipe.RET_MSG else '',
                        ))

    return list_recipes


def get_recipe_urls(serial_num: str):
    recipe = get_recipe_url(serial_num)
    if not recipe:
        return ''

    return recipe.PJURL


class ReceiptData(BaseModel):
    serial_num: str  # 流水号
    operator_id: str  # 经办人工号
    operator_name: str  # 经办人姓名
    department_id: str  # 部门id
    company_name: str  # 对方单位名称
    create_time: str  # 申请时间
    # business_type: str  # 业务类型
    contract_num: str  # 合同编号
    program_name: str  # 项目名称
    amount: float  # 开票金额（元）
    recipe_type: str  # 票据类型
    approval_state: str  # 审核状态
    reason: str  # 原因
    system_msg: str  # 系统提示
