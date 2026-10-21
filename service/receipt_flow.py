import logging
from sqlalchemy import text
from db import financial_write_engine
from models.ReceiptFlow import ReceiptFlowStatus

logger = logging.getLogger(__name__)


def get_receipt_flow_by_ywlsh(ywlsh: str) -> list[ReceiptFlowStatus]:
    """
    根据业务流水号查询接单流程状态
    
    :param ywlsh: 业务流水号
    :return: 流程状态列表
    """
    flow_status_list = []
    
    try:
        with financial_write_engine.connect() as conn:
            # 只查询 zw_jdgl_wlb 表
            query = text("""
                SELECT 
                    id, ywlx, ywlsh, clsj, clr, clrtel, xtdm,
                    jbr, bmbh, xmbh, je, bz, clsm, pzlxbh,
                    clrdm, jbrdm, wlbh, isfb, UUID, pznm
                FROM zw_jdgl_wlb 
                WHERE ywlsh = :ywlsh
                ORDER BY clsj ASC
            """)
            
            result = conn.execute(query, {"ywlsh": ywlsh})
            rows = result.fetchall()
            
            if not rows:
                logger.warning(f"未找到流水号 {ywlsh} 的物流包记录")
                return []
            
            # 处理每条记录
            for row in rows:
                status = _map_wlb_status(row)
                remark = str(row.clsm or row.bz or "")
                if row.wlbh:
                    remark = f"{remark} 物流编号:{str(row.wlbh)}" if remark else f"物流编号:{str(row.wlbh)}"
                
                flow_status_list.append(ReceiptFlowStatus(
                    sequence=0,
                    source="物流系统",
                    handler=str(row.clr or ""),
                    remark=remark,
                    process_time=_format_datetime_from_full(row.clsj),
                    status=status
                ))
                
    except Exception as e:
        logger.error(f"查询接单流程状态失败：{str(e)}", exc_info=True)
        raise
    
    # 按时间正序排序（从早到晚，空时间排到最后）
    flow_status_list.sort(
        key=lambda x: x.process_time if x.process_time else "9999-99-99 99:99:99",
        reverse=False
    )
    
    # 重新编号
    for idx, flow in enumerate(flow_status_list, 1):
        flow.sequence = idx
    
    return flow_status_list


def _map_wlb_status(row) -> str:
    """映射物流包状态"""
    # 根据 zw_jdgl_wlb 表的字段判断
    if row.isfb and str(row.isfb).strip() == '1':
        return "已发布"
    elif row.isfb and str(row.isfb).strip() == '0':
        return "未发布"
    elif row.clsj:
        return "已处理"
    else:
        return "待处理"


def _format_datetime_from_full(datetime_str: str) -> str:
    """格式化完整日期时间字符串"""
    if not datetime_str:
        return ""
    
    try:
        datetime_str = str(datetime_str)
        # 处理 "2026-07-10 09:42:05" 格式
        if len(datetime_str) >= 19:
            return datetime_str[:19]
    except Exception as e:
        logger.warning(f"日期时间格式化失败：{str(e)}")
    
    return str(datetime_str) if datetime_str else ""
