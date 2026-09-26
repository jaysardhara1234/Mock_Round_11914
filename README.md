# Data Analysis Set C - Training Performance
**Student name:** Jay Sardhara  |  **Student ID:** 11914 |  **Assigned set:** Set C
Red & White Skill Education - Practical Exam (Data Analysis)

> All work in this repository is my own except where cited.

## 1. Business objective
Find **which course needs the most academic support** and **how performance differs across batches**, using 12 independent assessments (Jan-Mar).

**Q1.** Which course needs the most support? -> **Python (C4)**: lowest average score (**49.33**) and lowest pass rate (**1/3 = 33.33%**). At department level, **Technology** (avg 56.00, pass rate 50.00%) trails Business (avg 67.00, pass rate 83.33%).
**Q2.** How do batches differ? -> **Evening** is best (avg 67.00), then Morning (61.25); **Weekend** is lowest (56.25, pass rate 50.00%).

## 2. Data files and dictionary
| File | Rows | Notes |
|---|---|---|
| `data/raw/assessments.csv` | 13 (12 unique + 1 exact duplicate of assessment_id 12) | fact file |
| `data/raw/courses.csv` | 4 | lookup file (one course -> many assessments) |

| Column | Type | Meaning |
|---|---|---|
| assessment_id | integer | assessment row id |
| month | text (ordered Jan, Feb, Mar) | assessment month |
| course_id | text | lookup key to courses |
| batch | text | Morning / Evening / Weekend |
| score | number 0-100 | assessment score |
| attendance_pct | number 0-100 | attendance percentage |
| course, department | text | course name; Business or Technology |
| pass_flag | integer (derived) | 1 if score >= 50 else 0 |

## 3. Cleaning and metric definitions
- Exact duplicate row (12, Mar, C4, Weekend, 42, 65) removed in **every** module: 13 rows -> **12 rows**. Raw values never edited.
- `pass_flag = 1 when score >= 50` (exactly 50 = pass), otherwise 0.
- `Pass rate = passing assessments / total assessments` (from counts, never averaging percentages).
- Each row is an independent assessment, not a longitudinal student record.

## 4. Tools and versions
Excel: Microsoft 365 (fill your version) | Power BI Desktop: (fill latest version) | SQL: **SQLite 3.45.1** | Python 3.12.3, pandas 3.0.2, matplotlib 3.10.8

## 5. Folder structure
```
data-analysis-set-c-YOUR-STUDENT-ID/
|-- README.md  requirements.txt  .gitignore
|-- data/raw/        assessments.csv  courses.csv
|-- excel/           analysis.xlsx  (Raw, Lookup, Clean, Summary)
|-- sql/             setup.sql  queries.sql
|-- python/          analysis.py
|-- powerbi/         Dashboard.pbix  (+ M scripts, measures.dax, BUILD_GUIDE.md)
`-- outputs/         clean_data.csv  python_summary.csv  python_chart.png
                     powerbi_dashboard.png  sql/ (s2a, s2b, s2c, s3 CSVs)
```

## 6. How to run
**SQL (SQLite):** `sqlite3 analysis.db < sql/setup.sql` then `sqlite3 -header -csv analysis.db < sql/queries.sql`
Execution order: setup.sql (creates tables, loads 4 + 12 rows, prints row counts) -> queries.sql (S2a, S2b, S2c, S3 integrity check).
**Python (from repo root):** `pip install -r requirements.txt` then `python python/analysis.py`
**Excel:** open `excel/analysis.xlsx`. Raw = original 13 rows; Lookup = courses; Clean = 12 rows with `department` (INDEX/MATCH) and `pass_flag` (IF) formulas plus before/after counts; Summary = COUNTIFS pass count by batch, department x month average-score table/PivotTable and chart.
**Power BI refresh:** open `powerbi/dashboard.pbix` > Home > Transform data > Edit parameters > set `DataFolder` to the full path of your cloned `data\raw\` folder (ending with `\`) > OK > Refresh. Data-source path used while building: `C:\...\data\raw\` (fill yours).

## 7. Findings and recommendation
1. **Technology** average score is **56.00** vs Business **67.00**; Technology pass rate is **50.00%** (3/6) vs Business **83.33%** (5/6). Overall: average **61.50**, pass rate **66.67%** (8/12).
2. **Python (C4)** has the lowest pass rate: **1/3 = 33.33%** (avg 49.33). Batches: Evening 67.00, Morning 61.25, **Weekend 56.25** (pass rate 50.00%). Monthly average improves Jan 55.00 -> Feb 62.75 -> Mar 66.75.
3. **Recommendation:** give extra academic support (doubt sessions, practice labs) to Python and SQL, prioritising the Weekend batch, and share Evening-batch practices.
4. **Limitation:** only 12 independent assessments (3 per course, 4 per batch), so results are indicative, not statistically strong; rows are not tracked per student.
- Power BI slicer test: Weekend -> Assessment Count 4, Avg Score 56.25, Pass Rate 50.00%; filter cleared -> 12 / 61.50 / 66.67%.

## 8. Cross-tool reconciliation (Technology average score)
| Tool | Where | Value |
|---|---|---|
| Excel | Summary table/PivotTable, Technology Grand Total | 56.00 |
| SQL | `s2a_avg_score_by_department.csv` | 56.00 |
| Python | `outputs/python_summary.csv` | 56.00 |
| Power BI | Avg Score card filtered to Technology | 56.00 |
No rounding differences (exact value 336/6 = 56).


## 10. References
None (all code written by me).
