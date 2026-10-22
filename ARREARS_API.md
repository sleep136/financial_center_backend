# 欠费学生查询接口

## 两个年度维度的区别

| 维度 | 字段 | 来源表 | 含义 |
| --- | --- | --- | --- |
| 学生年级 | `RXND` | `PXSDM` | 入学年度，标识学生属于哪一届 |
| 收费年度 | `SFQJDM` | `SF_ZZ` | 收费期间代码，标识费用归属于哪一年（字典表 `PSFQJ`） |

两者是**相互独立**的维度：同一收费年度下的欠费学生可能来自多个年级。
例如收费年度 `2025` 的 119 名欠费学生，其年级分布为 2022 级 33 人、2023 级 34 人、2024 级 43 人、2025 级 9 人。

两个字段取值均为 4 位年份字符串（如 `"2025"`）。

## 接口列表

### 1. 获取欠费学生明细
**请求：**
```
GET /arrears-students/details/{grade}/{fee_year}
GET /arrears-students/details/2025/2025
```

**路径参数：**
- `grade`：学生年级（`PXSDM.RXND`）
- `fee_year`：收费年度（`SF_ZZ.SFQJDM`）

**响应示例：**
```json
{
  "grade": "2025",
  "fee_year": "2025",
  "total_count": 9,
  "students": [
    {
      "xh": "2022413120118",
      "xm": "刘圳",
      "rxnd": "2025",
      "bmdm": "102",
      "bmmc": "电信工程与智能化学院",
      "bjmc": "2025光信息1班",
      "xsxzdm": "0104",
      "xsztdm": "1",
      "yjje": 3605.00,
      "sjje": 0,
      "qfje": 3605.00
    }
  ]
}
```

### 2. 按年级统计欠费
**请求：**
```
GET /arrears-students/statistics/grade/{fee_year}
GET /arrears-students/statistics/grade/2025
```

**响应示例：**
```json
{
  "fee_year": "2025",
  "statistics": [
    { "rxnd": "2022", "student_count": 33 },
    { "rxnd": "2023", "student_count": 34 },
    { "rxnd": "2024", "student_count": 43 },
    { "rxnd": "2025", "student_count": 9 }
  ]
}
```

### 3. 按学院统计欠费
**请求：**
```
GET /arrears-students/statistics/department/{fee_year}
GET /arrears-students/statistics/department/2025
```

**响应示例：**
```json
{
  "fee_year": "2025",
  "statistics": [
    { "bmdm": "102", "bmmc": "电信工程与智能化学院", "student_count": 22 },
    { "bmdm": "112", "bmmc": "文学与传媒学院", "student_count": 14 }
  ]
}
```

### 4. 获取指定学院的欠费学生明细
**请求：**
```
GET /arrears-students/department/{grade}/{fee_year}/{department_code}
GET /arrears-students/department/2024/2025/102
```

**路径参数：**
- `grade`：学生年级（`PXSDM.RXND`）
- `fee_year`：收费年度（`SF_ZZ.SFQJDM`）
- `department_code`：学院代码（`PXSDM.BMDM`）

**响应示例：**
```json
{
  "grade": "2024",
  "fee_year": "2025",
  "department_code": "102",
  "total_count": 10,
  "students": []
}
```

`students` 数组元素结构同接口 1。

## 查询条件

- **收费项目过滤（默认）**：`SFXMDM IN ('01', '02')`，即只统计**学费**和**住宿费**，不含辅修学费(`03`)、退费(`04`)、结业复读生学费(`05`)、补缴学费(`06`)等
- **欠费条件**：应交金额 - 实缴金额 > 0（`SUM(SF_ZZ.YJJE) - SUM(SF_ZZ.SJJE) > 0`）
- **不再过滤学生性质、学生来源、学生状态**：`xsxzdm` / `xsztdm` 仅作为明细字段返回供展示，
  不参与筛选。因此助学贷款（`0103`）、参军入伍（`0102`）等政策性缓缴学生，以及毕业（`XSZTDM='4'`）、
  休学等状态的学生，只要在指定收费年度存在欠费，都会出现在结果中。

## 统计维度

1. **按年级统计**：指定收费年度下，每个年级（`RXND`）的欠费学生人数，按年级升序
2. **按学院统计**：指定收费年度下，每个学院（`BMDM`）的欠费学生人数，按人数降序

## 注意事项

1. 学年/收费年度参数格式均为 4 位年份字符串（如 `"2025"`）
2. 金额字段保留两位小数
3. SQL Server 不允许聚合函数嵌套聚合函数，统计类查询需先用子查询按学号算出欠费金额，
   外层再按年级/学院 `COUNT`（见 `models/ArrearsStudent.py` 的 `_arrears_students_subquery`）
4. 学生性质、学生状态代码含义见字典表 `PXSXZ` / `PXSZT`：
   性质 `0104`=正常、`0103`=助学贷款、`0102`=参军入伍、`0101`=建档立卡；
   状态 `1`=在学、`2`=休学、`3`=退学、`4`=毕业
