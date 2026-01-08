from pydantic import BaseModel
from models.ApprovalWorkflow import get_approval_workflow_by_business_id, get_approval_workflow_by_work_id
import json

def get_workflow_by_business_id(business_id: str):
    """
    通过业务编号获取工作流信息
    :param business_id: 业务编号
    :return:
    """
    approval_workflows = get_approval_workflow_by_business_id(business_id)
    list_workflows = []

    for approval_workflow in approval_workflows:
        approval_date = approval_workflow.SPRQ if approval_workflow.SPRQ else ""
        approver = approval_workflow.SPR  if approval_workflow.SPR  else ""
        list_workflows.append(
            ApprovalWorkflowDataObject(business_id=approval_workflow.YWLSH,
                                       business_type=approval_workflow.YWBH,
                                       applicants_id=approval_workflow.SQRBH,
                                       applicants_name=approval_workflow.SQR,
                                       apply_date=approval_workflow.SQRQ,
                                       approver=approver,
                                       approval_date=approval_date,
                                       approval_state=approval_workflow.SPZT,
                                       approval_sort=approval_workflow.SPJB,
                                       approval_role=approval_workflow.SPJS,
                                       abstract=approval_workflow.SQNR
                                       ))
    return list_workflows


def get_workflow_by_work_id(work_id: str):
    """
    通过工作流编号获取工作流信息
    :param work_id: 工作流编号
    :return:
    """
    approval_workflows = get_approval_workflow_by_work_id(work_id)

    dict_workflows = {}
    for approval_workflow in approval_workflows:
        if approval_workflow.YWLSH in dict_workflows:
            if dict_workflows[approval_workflow.YWLSH]['approval_state'] == 2:
                continue
            if approval_workflow.SPJB < dict_workflows[approval_workflow.YWLSH]['approval_sort']:
                continue

        dict_workflows[approval_workflow.YWLSH] = {
            'business_id': approval_workflow.YWLSH,
            'business_type': approval_workflow.YWBH,
            'applicants_id': approval_workflow.SQRBH,
            'applicants_name': approval_workflow.SQR,
            'apply_date': approval_workflow.SQRQ,
            'approver': approval_workflow.SPR,
            'approval_date': approval_workflow.SPRQ,
            'approval_state': approval_workflow.SPZT,
            'approval_sort': approval_workflow.SPJB,
            'approval_role': approval_workflow.SPJS,
            'abstract': approval_workflow.SQNR

        }

    list_workflows = []

    for lsh, approval_workflow in dict_workflows.items():
        print(approval_workflow)
        abstract_dict = json.loads(approval_workflow['abstract'])
        abstract =flatten_dict_to_str(abstract_dict)
        approval_date = approval_workflow['approval_date'] if approval_workflow['approval_date'] else ""
        approver = approval_workflow['approver'] if approval_workflow['approver'] else ""
        list_workflows.append(
            ApprovalWorkflowDataObject(business_id=approval_workflow['business_id'],
                                       business_type=approval_workflow['business_type'],
                                       applicants_id=approval_workflow['applicants_id'],
                                       applicants_name=approval_workflow['applicants_name'],
                                       apply_date=approval_workflow['apply_date'],
                                       approver=approver,
                                       approval_date=approval_date,
                                       approval_state=approval_workflow['approval_state'],
                                       approval_sort=approval_workflow['approval_sort'],
                                       approval_role=approval_workflow['approval_role'],
                                       abstract=abstract
                                       ))
    return list_workflows


class ApprovalWorkflowDataObject(BaseModel):
    business_id: str
    business_type: str
    applicants_id: str
    applicants_name: str
    apply_date: str
    approver: str
    approval_date: str
    approval_state: str  #
    approval_sort: str  #
    approval_role: str  #
    abstract: str  # 申请内容摘要


def flatten_dict_to_str(d, sep='_', kv_sep='='):
    """
    将字典完全平铺为字符串

    Args:
        d: 要处理的字典
        sep: 嵌套键之间的分隔符
        kv_sep: 键和值之间的分隔符
    """

    def _flatten(data, parent_key=''):
        items = []
        if isinstance(data, dict):
            for k, v in data.items():
                new_key = f"{parent_key}{sep}{k}" if parent_key else k
                items.extend(_flatten(v, new_key))
        elif isinstance(data, (list, tuple)):
            for i, item in enumerate(data):
                new_key = f"{parent_key}{sep}{i}" if parent_key else str(i)
                items.extend(_flatten(item, new_key))
        else:
            items.append(f"{parent_key}{kv_sep}{data}")
        return items

    return '; '.join(_flatten(d))