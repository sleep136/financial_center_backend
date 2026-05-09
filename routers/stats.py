from fastapi import APIRouter, HTTPException
from script.reimbursement_stats import ReimbursementStats  # 你的统计类
from redis import Redis
import json
from datetime import datetime

from config.settings import settings
redis = Redis.from_url(settings.REDIS_URL, decode_responses=True)
router = APIRouter()



@router.get("/stats/trigger", summary="手动触发报销统计（生成Excel+存入Redis）")
async def trigger_report_stats():  # 👈 加 async
    try:
        print("开始执行统计任务...")  # 👈 强制打印

        stats = ReimbursementStats()
        result = stats.run()

        print(" 统计执行完成：", result)
        return {
            "code": 200,
            "msg": "执行成功",
            "result": result
        }
    except Exception as e:
        print("执行失败：", str(e))  # 👈 强制打印错误
        raise HTTPException(status_code=500, detail=f"执行失败：{str(e)}")


# ------------------------------------------------------------------------------
# 2. 获取年度总览（总金额、总次数）
# ------------------------------------------------------------------------------
@router.get("/stats/total", summary="获取年度统计总览")
def get_report_total(year: str = None):
    if not year:
        year = datetime.now().strftime("%Y")
    key = f"report:total:{year}"
    data = redis.get(key)
    if not data:
        raise HTTPException(status_code=404, detail="暂无统计数据")
    return json.loads(data)

# ------------------------------------------------------------------------------
# 3. 获取月度趋势数据（折线图）
# ------------------------------------------------------------------------------
@router.get("/stats/month", summary="获取月度报销趋势")
def get_month_trend(year: str = None):
    if not year:
        year = datetime.now().strftime("%Y")
    key = f"report:month:trend:{year}"
    data = redis.get(key)
    if not data:
        raise HTTPException(status_code=404, detail="暂无统计数据")
    return json.loads(data)

# ------------------------------------------------------------------------------
# 4. 获取供应商金额排名 TOP10（柱状图）
# ------------------------------------------------------------------------------
@router.get("/stats/supplier", summary="获取供应商报销金额TOP50")
def get_supplier_rank(year: str = None):
    if not year:
        year = datetime.now().strftime("%Y")
    key = f"rank:supplier:{year}"
    # 👈 从 10 改成 50
    rank_list = redis.zrevrange(key, 0, 49, withscores=True)

    result = []
    for supplier, amount in rank_list:
        # 👇 从明细里拿 发票数量
        detail_key = f"report:detail:supplier:{year}"
        detail_data = redis.get(detail_key)
        count = 0
        if detail_data:
            details = json.loads(detail_data)
            count = len(details.get(supplier, []))

        result.append({
            "supplier": supplier,
            "amount": round(amount, 2),
            "count": count  # 👈 新增发票数
        })
    return result

# ------------------------------------------------------------------------------
# 5. 获取学院统计（可选扩展）
# ------------------------------------------------------------------------------
@router.get("/stats/college", summary="获取各学院报销统计")
def get_college_stats(year: str = None):
    if not year:
        year = datetime.now().strftime("%Y")
    key = f"report:college:{year}"
    data = redis.hgetall(key)
    result = {k: json.loads(v) for k, v in data.items()}
    return result

# ------------------------------------------------------------------------------
# 6. 按供应商查询发票明细（只包含>20条的供应商）
# ------------------------------------------------------------------------------
@router.get("/stats/detail/supplier", summary="按供应商查询发票明细（>20条）")
def get_supplier_detail(supplier: str, year: str = None):
    if not year:
        year = datetime.now().strftime("%Y")
    key = f"report:detail:supplier:{year}"
    data = redis.get(key)
    if not data:
        raise HTTPException(status_code=404, detail="无数据")
    details = json.loads(data)
    if supplier not in details:
        raise HTTPException(status_code=404, detail="该供应商无明细或未满足>20条")
    return {"supplier": supplier, "items": details[supplier]}

# ------------------------------------------------------------------------------
# 7. 按学院查询发票明细
# ------------------------------------------------------------------------------
@router.get("/stats/detail/college", summary="按学院查询发票明细")
def get_college_detail(college: str, year: str = None):
    if not year:
        year = datetime.now().strftime("%Y")
    key = f"report:detail:college:{year}"
    data = redis.get(key)
    if not data:
        raise HTTPException(status_code=404, detail="无数据")
    details = json.loads(data)
    if college not in details:
        raise HTTPException(status_code=404, detail="该学院无明细")
    return {"college": college, "items": details[college]}

# ------------------------------------------------------------------------------
# 8. 按月份查询发票明细
# ------------------------------------------------------------------------------
@router.get("/stats/detail/month", summary="按月份查询发票明细 1~12月")
def get_month_detail(month: str, year: str = None):
    if not year:
        year = datetime.now().strftime("%Y")
    key = f"report:detail:month:{year}"
    data = redis.get(key)
    if not data:
        raise HTTPException(status_code=404, detail="无数据")
    details = json.loads(data)
    month_text = f"{int(month)}月"
    if month_text not in details:
        raise HTTPException(status_code=404, detail="该月份无明细")
    return {"month": month, "items": details[month_text]}

@router.get("/stats/month/top/college", summary="获取指定月份报销TOP10学院")
def get_month_top_college(month: str, year: str = None):
    if not year:
        year = datetime.now().strftime("%Y")
    key = f"report:detail:month:{year}"
    data = redis.get(key)
    if not data:
        raise HTTPException(status_code=404, detail="暂无月度统计数据")

    details = json.loads(data)
    month_text = f"{int(month)}月"
    if month_text not in details:
        return []

    items = details[month_text]
    # 按学院聚合金额、数量
    college_dict = {}
    for item in items:
        col_name = item.get("dept_name", "未知学院") or "未知学院"
        try:
            amt = float(item.get("ZJE", 0))
        except:
            amt = 0
        if col_name not in college_dict:
            college_dict[col_name] = {"amount": 0.0, "count": 0}
        college_dict[col_name]["amount"] += amt
        college_dict[col_name]["count"] += 1

    # 转列表、按金额倒序、取前10
    res_list = [
        {"name": k, "amount": round(v["amount"], 2), "count": v["count"]}
        for k, v in college_dict.items()
    ]
    res_list.sort(key=lambda x: x["amount"], reverse=True)
    return res_list[:10]


@router.get("/stats/month/top/user", summary="获取指定月份报销TOP10经办人")
def get_month_top_user(month: str, year: str = None):
    if not year:
        year = datetime.now().strftime("%Y")
    key = f"report:detail:month:{year}"
    data = redis.get(key)
    if not data:
        raise HTTPException(status_code=404, detail="暂无月度统计数据")

    details = json.loads(data)
    month_text = f"{int(month)}月"
    if month_text not in details:
        return []

    items = details[month_text]
    # 按经办人聚合
    user_dict = {}
    for item in items:
        user_name = item.get("ygmc", "未知经办人") or "未知经办人"
        try:
            amt = float(item.get("ZJE", 0))
        except:
            amt = 0
        if user_name not in user_dict:
            user_dict[user_name] = {"amount": 0.0, "count": 0}
        user_dict[user_name]["amount"] += amt
        user_dict[user_name]["count"] += 1

    # 倒序取前10
    res_list = [
        {"name": k, "amount": round(v["amount"], 2), "count": v["count"]}
        for k, v in user_dict.items()
    ]
    res_list.sort(key=lambda x: x["amount"], reverse=True)
    return res_list[:10]


@router.get("/stats/month/total", summary="获取指定月份总金额、总票数（前端直出）")
def get_month_total(month: str, year: str = None):
    if not year:
        year = datetime.now().strftime("%Y")

    # 读取你现有的 全量月度明细（你已经存在Redis里了）
    key = f"report:detail:month:{year}"
    data = redis.get(key)
    if not data:
        raise HTTPException(status_code=404, detail="暂无月度统计数据")

    details = json.loads(data)
    month_text = f"{int(month)}月"  # 01 → 1月，和你现有结构匹配

    if month_text not in details:
        return {"amount": 0.0, "count": 0}

    # 从现有明细直接统计 → 写入Redis结构不变
    items = details[month_text]
    total_amount = 0.0
    total_count = len(items)

    for item in items:
        try:
            total_amount += float(item.get("ZJE", 0))
        except:
            pass

    return {
        "amount": round(total_amount, 2),
        "count": total_count
    }