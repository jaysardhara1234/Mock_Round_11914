"""Data Analysis Set C - Training Performance (Python module).
Run from the repository root:  python python/analysis.py
"""
from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent   
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

# ---------- P1: load, clean, merge ----------
asm = pd.read_csv(ROOT / "data/raw/assessments.csv",
                  dtype={"month": str, "course_id": str, "batch": str})
courses = pd.read_csv(ROOT / "data/raw/courses.csv", dtype=str)
print("Raw assessments rows :", len(asm))

for c in ["score", "attendance_pct"]:
    asm[c] = pd.to_numeric(asm[c])
asm["assessment_id"] = asm["assessment_id"].astype(int)
assert pd.api.types.is_numeric_dtype(asm["score"])
assert pd.api.types.is_numeric_dtype(asm["attendance_pct"])
print("Dtypes:", dict(asm.dtypes.astype(str)))

asm = asm.drop_duplicates().reset_index(drop=True)
print("Clean assessments rows:", len(asm))

df = asm.merge(courses, on="course_id", how="left")
assert len(df) == 12, f"expected 12 rows, got {len(df)}"
assert df["department"].isna().sum() == 0, "unmatched course_id found"
print("Merge OK: 12 rows, 0 unmatched course_id (0 NaN in department)")

month_order = ["Jan", "Feb", "Mar"]
df["month"] = pd.Categorical(df["month"], categories=month_order, ordered=True)

# ---------- P2: derived field & department analysis ----------
df["pass_flag"] = (df["score"] >= 50).astype(int)      # 50 exactly = pass

dept = (df.groupby("department")
          .agg(total_assessments=("assessment_id", "count"),
               passing_assessments=("pass_flag", "sum"),
               avg_score=("score", "mean"))
          .reset_index())
dept["pass_rate_pct"] = (dept["passing_assessments"] / dept["total_assessments"] * 100).round(2)
dept["avg_score"] = dept["avg_score"].round(2)
print("\nDepartment summary:\n", dept.to_string(index=False))

course = (df.groupby(["course_id", "course"])
            .agg(total_assessments=("assessment_id", "count"),
                 passing_assessments=("pass_flag", "sum"))
            .reset_index())
course["pass_rate_pct"] = (course["passing_assessments"] / course["total_assessments"] * 100).round(2)
print("\nCourse pass rates:\n", course.to_string(index=False))
lowest = course[course["pass_rate_pct"] == course["pass_rate_pct"].min()]   # all ties
for _, r in lowest.iterrows():
    print(f"\nLowest pass rate: {r['course_id']} ({r['course']}) = "
          f"{int(r['passing_assessments'])}/{int(r['total_assessments'])} = {r['pass_rate_pct']:.2f}%")

overall_pass = df["pass_flag"].sum() / len(df) * 100
print(f"Overall pass rate = {int(df['pass_flag'].sum())}/{len(df)} = {overall_pass:.2f}%")
print(f"Overall average score = {df['score'].mean():.2f}")

batch = df.groupby("batch")["score"].mean().round(2).sort_values(ascending=False)
print("\nAverage score by batch:\n", batch.to_string())

# ---------- P3: chart & exports ----------
monthly = df.groupby("month", observed=False)["score"].mean().reindex(month_order)
fig, ax = plt.subplots(figsize=(7, 4.5))
bars = ax.bar(monthly.index.astype(str), monthly.values, color="#1f77b4")
ax.bar_label(bars, fmt="%.2f")
ax.set_title("Monthly Average Score (Jan - Mar)")
ax.set_xlabel("Month")
ax.set_ylabel("Average score (0-100)")
ax.set_ylim(0, 100)
fig.tight_layout()
fig.savefig(OUT / "python_chart.png", dpi=150)
plt.close(fig)

df.astype({"score": float, "attendance_pct": float}).to_csv(
    OUT / "clean_data.csv", index=False, float_format="%.2f")
dept.to_csv(OUT / "python_summary.csv", index=False, float_format="%.2f")
print("\nExports saved to outputs/: python_chart.png, clean_data.csv, python_summary.csv")
