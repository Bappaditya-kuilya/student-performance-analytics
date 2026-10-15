# Project Documentation — Student Performance Analytics System

## 1. Project title and student details

- Project: Student Performance Analytics System
- Course: Python with AI
- Student name / ID: as provided in the EWB Google Form submission
- Date: October 2026

## 2. Objective

Automate student mark + attendance analysis: per-student totals/averages/grades/pass-fail, class stats, subject comparison, top-performer ranking. Solves manual reading of mark rows being slow and error-prone.

## 3. Technologies used

Python 3.12, Pandas 3.0.6 (`read_csv`, DataFrames, filtering, sorting), NumPy 2.5.4 (`sum`, `mean`, `max`, `min`), CSV, pip + `requirements.txt`, Markdown, Git + GitHub (public repository, see §10).

## 4. Dataset description

`students.csv`, 20 records, columns: `student_id,name,department,python_marks,mathematics_marks,statistics_marks,attendance`. Mark scale 0–100, attendance 0–100 (reported only). IDs `STU001`–`STU020` unique, no missing values. Deliberate edge cases: STU010 average exactly 80.00 (grade boundary), STU005 / STU012 / STU015 each fail exactly one subject, STU008 attendance 100, STU015 attendance 55.

## 5. Implementation

- `load_data(path)` — `pd.read_csv`, clear `FileNotFoundError` with expected path.
- `validate_data(df)` — required columns, ≥15 rows, unique IDs, no nulls (never `fillna(0)`), numeric + range checks for marks and attendance.
- `calculate_student_metrics` — NumPy `sum`/`mean` over subject matrix, adds `total` (int) and `average` (2-dec).
- Loop over rows with `assign_grade` (threshold chain ≥90/80/70/60/50) and `assign_pass_status` (any subject <40 → Fail).
- `analyze_class` — NumPy mean/max/min over averages, pass counts, pass %.
- `analyze_subjects` — per-subject mean/max/min/passed via NumPy.
- `get_top_performers(df, 5)` — sort by average desc + `student_id` asc, include ties at cutoff.
- `main.py` — locates CSV next to script, orchestrates, prints dtype/missing inspection then formatted report. Errors print message + exit 1.

## 6. Key features

Data loading + inspection, per-student total/average/grade/pass-fail, class summary (count, avg, high/low, pass/fail, %), subject summary (avg/high/low/passed), top-5 ranking with ties, clear labeled output, explicit validation errors.

## 7. Output / screenshots

Real run (`python -m pip install -r requirements.txt`, then `python main.py`):

```text
Total students: 20
Class average: 72.82
Highest average: 96.67 | Lowest average: 41.67
Students passed: 17 | Students failed: 3
Pass percentage: 85.00%

TOP PERFORMERS
STU008 | Ishita Nair | 96.67 | A+
STU002 | Diya Sharma | 94.33 | A+
STU011 | Aditya Rao | 91.67 | A+
STU017 | Nikhil Bose | 90.00 | A+
STU006 | Sneha Kulkarni | 87.33 | A

SUBJECT SUMMARY
python_marks | 71.35 | 98 | 38 | 19
mathematics_marks | 72.30 | 95 | 35 | 19
statistics_marks | 74.80 | 97 | 39 | 19
```

See `screenshots/analysis-output.png` (rendered from this exact output).

## 8. Final outcome

Program runs in a clean virtual environment via `python main.py`, all checks pass: 20 rows, manual totals match (STU001 246/82.00, STU008 290/96.67), grade boundaries correct at 50/60/70/80/90, 3 single-subject fails detected (STU005, STU012, STU015), counts sum to 20, top-5 correctly ordered, error paths produce clear messages.

## 9. Challenges and learning

1. `uv init` in a non-empty folder — used `--bare --vcs none --no-readme` to get only `pyproject.toml`, avoiding README overwrite. (Local tooling only; `pyproject.toml` is not part of the submitted repo, which installs via `requirements.txt`.)
2. Leftover ugly ternary in `validate_data` duplicate-ID branch — caught on re-read, simplified to one f-string before testing.
3. Pandas 3.0 dtype output shows `str` instead of `object` — kept as-is, inspection print still satisfies the requirement.

## 10. GitHub repository

Pushed to https://github.com/Bappaditya-kuilya/student-performance-analytics (public, branch `main`). Submit this URL through the EWB Google Form, then confirm the form submission is complete.
