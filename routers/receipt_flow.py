from fastapi import APIRouter, HTTPException, status
from service.receipt_flow import get_receipt_flow_by_ywlsh

router = APIRouter()


@router.get("/receipt-flow/{ywlsh}")
async def get_receipt_flow(ywlsh: str):
    """
    根据业务流水号查询接单流程状态
    
    :param ywlsh: 业务流水号，如 202607700445
    :return: 流程状态列表
    """
    try:
        flow_list = get_receipt_flow_by_ywlsh(ywlsh)
        
        if not flow_list:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"未找到流水号 {ywlsh} 的接单流程记录"
            )
        
        return {
            "ywlsh": ywlsh,
            "flow_status": flow_list
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"查询失败：{str(e)}"
        )
