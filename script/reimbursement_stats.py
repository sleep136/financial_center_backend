import pandas as pd
import datetime
import json
import logging
from redis import Redis
from models.Person import Person
from models.Department import Department
from models.Invoice import Invoice
from config.settings import settings
from db import financial_engine, reimbursement_engine
from sqlmodel import Session

logger = logging.getLogger(__name__)
redis = Redis.from_url(settings.REDIS_URL, decode_responses=True)

class ReimbursementStats:
    def __init__(self):
        self.year = datetime.datetime.now().strftime("%Y")
        self.month = datetime.datetime.now().strftime("%m")

    # ======================
    # 1. 加载数据
    # ======================
    def load_data(self):
        logger.info("==================== 开始加载数据 ====================")

        # 发票
        logger.info("加载发票数据...")
        with Session(reimbursement_engine) as session:
            now = datetime.datetime.now()
            year = now.strftime("%Y")
            start_date = int(f"{year}0101")
            invoices = Invoice.get_year_checked_invoices(start_date)
            df_invoice = pd.DataFrame([dict(i) for i in invoices])
            df_invoice = df_invoice.astype(str).fillna("")

        # 人员
        logger.info("加载人员数据...")
        with Session(financial_engine) as session:
            persons = Person.get_all_persons()
            df_person = pd.DataFrame([dict(p) for p in persons])

        # 部门
        logger.info("加载部门数据...")
        with Session(financial_engine) as session:
            depts = Department.get_all_departments()
            df_dept = pd.DataFrame([dict(d) for d in depts])

        dept_map = dict(zip(
            df_dept["bmdm"].astype(str).str.strip(),
            df_dept["bmmc"].astype(str).str.strip()
        ))

        logger.info(f"数据加载完成：发票{len(df_invoice)}条，人员{len(df_person)}人，部门{len(df_dept)}个")
        return df_invoice, df_person, dept_map

    # ======================
    # 2. 部门映射
    # ======================
    def map_dept_code(self, bmbh):
        mapping = {
            "39902": "20100", "111": "20100", "107": "20100",
            "39906": "20600", "106": "20600",
            "39904": "20400", "110": "20400",
            "102": "20300", "39903": "20300",
            "103": "21300",
            "120": "22200",
            "105": "20500", "39910": "20500",
            "39909": "22000", "119": "22000",
            "101": "20700", "39907": "20700",
            "39905": "31300",
            "104": "21000", "39908": "21000",
            "39901": "10900",
            "39912": "22100", "121": "22100",
            "116": "21200",
            "114": "21700",
            "109": "20800", "39911": "20800",
            "108": "21100",
            "4008/": "31400",
            "112": "20900",

        }
        return mapping.get(str(bmbh).strip(), str(bmbh).strip())

    # ======================
    # 3. 合并数据
    # ======================
    def merge_data(self, df_invoice, df_person, dept_map):
        df_person["final_bmbh"] = df_person.apply(
            lambda r: r["bmbh"] if r["bmbh"] and len(str(r["bmbh"]).strip()) > 4 else r["gzbmbh"], axis=1
        )
        df_person["final_bmbh"] = df_person["final_bmbh"].apply(self.map_dept_code)
        df_invoice["JBR"] = df_invoice["JBR"].astype(str).str.strip()
        df_person["ygbh"] = df_person["ygbh"].astype(str).str.strip()

        df_merged = pd.merge(
            df_invoice,
            df_person[["ygbh", "ygmc", "final_bmbh"]],
            left_on="JBR",
            right_on="ygbh",
            how="left"
        )
        df_merged["dept_name"] = df_merged["final_bmbh"].map(dept_map)
        df_merged["ZJE"] = pd.to_numeric(df_merged["ZJE"], errors="coerce").fillna(0)
        df_merged["KPRQ"] = df_merged["KPRQ"].astype(str)
        df_merged = df_merged.astype(str).fillna("")
        df_merged["ZJE"] = pd.to_numeric(df_merged["ZJE"], errors="coerce").fillna(0)

        return df_merged

    # ======================
    # 4. 供应商分析（>5）
    # ======================
    def analyze_supplier(self, df_merged, dept_map):
        supplier_counts = df_merged["KPDWMC"].value_counts()
        targets = supplier_counts[supplier_counts > 10].index
        result = []
        month_trend = {}
        supplier_details = {}

        for supplier in targets:
            sup_df = df_merged[df_merged["KPDWMC"] == supplier]
            total_amt = sup_df["ZJE"].sum()
            total_cnt = len(sup_df)

            top_dept = sup_df["final_bmbh"].value_counts().head(5)
            dept_str = " ".join([
                f"{dept_map.get(d, '未知')}占比{round(cnt/total_cnt*100,2)}%"
                for d, cnt in top_dept.items()
            ])

            top_person = sup_df["ygmc"].value_counts().head(5)
            person_str = " ".join([
                f"{name}占比{round(cnt/total_cnt*100,2)}%"
                for name, cnt in top_person.items()
            ])

            main_content = sup_df["FPNR"].value_counts().idxmax() if not sup_df.empty else ""

            month_data = {}
            current_month = int(self.month)
            for m in range(1, current_month + 1):
                m_str = f"{m:02d}"
                start = f"{self.year}{m_str}01"
                end = f"{self.year}{m_str}31"
                m_df = sup_df[(sup_df["KPRQ"] >= start) & (sup_df["KPRQ"] <= end)]
                month_data[f"{m}月"] = {
                    "amount": round(m_df["ZJE"].sum(), 2),
                    "count": len(m_df)
                }

            result.append({
                "供应商": supplier,
                "总金额": total_amt,
                "总次数": total_cnt,
                "top5学院": dept_str,
                "top5经办人": person_str,
                "主要内容": main_content,
                **month_data
            })
            month_trend[supplier] = month_data

            # 保存明细
            supplier_details[supplier] = sup_df.to_dict(orient="records")

        return pd.DataFrame(result), month_trend, supplier_details

    # ======================
    # 5. 学院分析（全量）
    # ======================
    def analyze_college(self, df_merged):
        college_stats = df_merged.groupby("dept_name").agg(
            总金额=("ZJE", "sum"),
            总次数=("ZJE", "count")
        ).round(2).to_dict("index")

        college_details = {}
        for college in df_merged["dept_name"].dropna().unique():
            college_details[college] = df_merged[df_merged["dept_name"] == college].to_dict("records")

        return college_stats, college_details

    # ======================
    # 6. 全量月度明细（全量）
    # ======================
    def analyze_month_detail(self, df_merged):
        month_details = {}
        current_month = int(self.month)
        for m in range(1, current_month + 1):
            m_str = f"{m:02d}"
            start = f"{self.year}{m_str}01"
            end = f"{self.year}{m_str}31"
            m_df = df_merged[(df_merged["KPRQ"] >= start) & (df_merged["KPRQ"] <= end)]
            month_details[f"{m}月"] = m_df.to_dict("records")
        return month_details

    # ======================
    # 7. 保存全部数据到 Redis
    # ======================
    def save_to_redis(
        self,
        df_result,
        month_trend,
        college_stats,
        supplier_details,
        college_details,
        month_details,
        df_merged
    ):
        # 总数
        redis.set(f"report:total:{self.year}", json.dumps({
            "total_amount": round(df_merged["ZJE"].sum(), 2),
            "total_count": len(df_merged)
        }))

        # 供应商
        redis.delete(f"rank:supplier:{self.year}")
        for _, row in df_result.iterrows():
            redis.zadd(f"rank:supplier:{self.year}", {row["供应商"]: row["总金额"]})

        # 趋势
        redis.set(f"report:month:trend:{self.year}", json.dumps(month_trend))

        # 学院
        redis.delete(f"report:college:{self.year}")
        for college, data in college_stats.items():
            redis.hset(f"report:college:{self.year}", college, json.dumps(data))

        # 明细
        redis.set(f"report:detail:supplier:{self.year}", json.dumps(supplier_details, ensure_ascii=False))
        redis.set(f"report:detail:college:{self.year}", json.dumps(college_details, ensure_ascii=False))
        redis.set(f"report:detail:month:{self.year}", json.dumps(month_details, ensure_ascii=False))

        logger.info("所有统计 + 明细已存入Redis")

    # ======================
    # 8. 运行
    # ======================
    def run(self):
        logger.info("开始执行统计...")
        df_invoice, df_person, dept_map = self.load_data()
        df_merged = self.merge_data(df_invoice, df_person, dept_map)
        df_result, month_trend, supplier_details = self.analyze_supplier(df_merged, dept_map)
        college_stats, college_details = self.analyze_college(df_merged)
        month_details = self.analyze_month_detail(df_merged)

        self.save_to_redis(
            df_result, month_trend, college_stats,
            supplier_details, college_details, month_details, df_merged
        )
        return "统计完成"