"""Reusable calculations for Student Performance Analytics System."""

import numpy as np
import pandas as pd

REQUIRED_COLUMNS = [
    "student_id",
    "name",
    "department",
    "python_marks",
    "mathematics_marks",
    "statistics_marks",
    "attendance",
]

PASS_MARK = 40


def load_data(path: str) -> pd.DataFrame:
    """Read CSV at path. Raises FileNotFoundError with clear path on miss."""
    try:
        return pd.read_csv(path)
    except FileNotFoundError:
        raise FileNotFoundError(
            f"Error: students.csv not found at {path}. "
            "Expected next to main.py."
        )


def validate_data(df: pd.DataFrame) -> None:
    """Check columns, row count, duplicates, numeric ranges. Raises ValueError."""
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Error: missing columns: {missing}")

    if len(df) < 15:
        raise ValueError(
            f"Error: dataset has {len(df)} records, need at least 15."
        )

    if df["student_id"].duplicated().any():
        dupes = df.loc[df["student_id"].duplicated(), "student_id"].tolist()
        raise ValueError(f"Error: duplicate student_id values: {dupes}")

    if df[REQUIRED_COLUMNS].isnull().any().any():
        bad = df[df[REQUIRED_COLUMNS].isnull().any(axis=1)]["student_id"].tolist()
        raise ValueError(
            f"Error: missing values found in rows: {bad}. "
            "Missing marks are not replaced with zero."
        )

    mark_cols = ["python_marks", "mathematics_marks", "statistics_marks"]
    for col in mark_cols:
        if not pd.api.types.is_numeric_dtype(df[col]):
            raise ValueError(f"Error: column '{col}' must be numeric.")
        bad_rows = df[(df[col] < 0) | (df[col] > 100)]
        if not bad_rows.empty:
            ids = bad_rows["student_id"].tolist()
            raise ValueError(
                f"Error: column '{col}' out of range 0-100 in rows: {ids}."
            )

    if not pd.api.types.is_numeric_dtype(df["attendance"]):
        raise ValueError("Error: column 'attendance' must be numeric.")
    bad_att = df[(df["attendance"] < 0) | (df["attendance"] > 100)]
    if not bad_att.empty:
        ids = bad_att["student_id"].tolist()
        raise ValueError(
            f"Error: attendance out of range 0-100 in rows: {ids}."
        )


def calculate_student_metrics(
    df: pd.DataFrame, subject_columns: list[str]
) -> pd.DataFrame:
    """Add total and average columns using NumPy. Returns new DataFrame."""
    out = df.copy()
    marks = out[subject_columns].to_numpy(dtype=float)
    out["total"] = np.sum(marks, axis=1).astype(int)
    out["average"] = np.mean(marks, axis=1).round(2)
    return out


def assign_grade(average: float) -> str:
    """Return grade for average using locked thresholds."""
    if average >= 90:
        return "A+"
    if average >= 80:
        return "A"
    if average >= 70:
        return "B"
    if average >= 60:
        return "C"
    if average >= 50:
        return "D"
    return "F"


def assign_pass_status(row, subject_columns: list[str]) -> str:
    """Pass iff every subject mark >= 40."""
    for col in subject_columns:
        if row[col] < PASS_MARK:
            return "Fail"
    return "Pass"


def analyze_subjects(df: pd.DataFrame, subject_columns: list[str]) -> dict:
    """Per-subject average, highest, lowest, passed count."""
    summary: dict = {}
    for col in subject_columns:
        values = df[col].to_numpy(dtype=float)
        summary[col] = {
            "average": round(float(np.mean(values)), 2),
            "highest": int(np.max(values)),
            "lowest": int(np.min(values)),
            "passed": int((df[col] >= PASS_MARK).sum()),
        }
    return summary


def analyze_class(df: pd.DataFrame) -> dict:
    """Class-level stats from per-student averages."""
    averages = df["average"].to_numpy(dtype=float)
    passed = int((df["status"] == "Pass").sum())
    total = len(df)
    failed = total - passed
    return {
        "total_students": total,
        "class_average": round(float(np.mean(averages)), 2) if total else 0.0,
        "highest_average": round(float(np.max(averages)), 2) if total else 0.0,
        "lowest_average": round(float(np.min(averages)), 2) if total else 0.0,
        "passed": passed,
        "failed": failed,
        "pass_percentage": round(passed / total * 100, 2) if total else 0.0,
    }


def get_top_performers(df: pd.DataFrame, count: int = 5) -> pd.DataFrame:
    """Top students by average desc, ties at cutoff included."""
    ranked = df.sort_values(
        by=["average", "student_id"], ascending=[False, True]
    ).reset_index(drop=True)
    if len(ranked) <= count:
        return ranked
    cutoff = ranked.loc[count - 1, "average"]
    return ranked[ranked["average"] >= cutoff].reset_index(drop=True)


def display_report(
    df: pd.DataFrame,
    class_summary: dict,
    subject_summary: dict,
    top_df: pd.DataFrame,
) -> None:
    """Print formatted class, top-performer, and subject reports."""
    print("STUDENT PERFORMANCE ANALYTICS")
    print("--------------------------------")
    print(f"Total students: {class_summary['total_students']}")
    print(f"Class average: {class_summary['class_average']:.2f}")
    print(
        f"Highest average: {class_summary['highest_average']:.2f} | "
        f"Lowest average: {class_summary['lowest_average']:.2f}"
    )
    print(
        f"Students passed: {class_summary['passed']} | "
        f"Students failed: {class_summary['failed']}"
    )
    print(f"Pass percentage: {class_summary['pass_percentage']:.2f}%")
    print()
    print("TOP PERFORMERS (top 5, ties included)")
    print("Student ID | Name | Average | Grade")
    for _, row in top_df.iterrows():
        print(
            f"{row['student_id']} | {row['name']} | "
            f"{row['average']:.2f} | {row['grade']}"
        )
    print()
    print("SUBJECT SUMMARY")
    print("Subject | Average | Highest | Lowest | Passed")
    for subject, stats in subject_summary.items():
        print(
            f"{subject} | {stats['average']:.2f} | "
            f"{stats['highest']} | {stats['lowest']} | {stats['passed']}"
        )
