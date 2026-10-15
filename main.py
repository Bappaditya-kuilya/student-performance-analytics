"""Student Performance Analytics System — entry point."""

import sys
from pathlib import Path

from functions import (
    analyze_class,
    analyze_subjects,
    assign_grade,
    assign_pass_status,
    calculate_student_metrics,
    display_report,
    get_top_performers,
    load_data,
    validate_data,
)

SUBJECT_COLUMNS = ["python_marks", "mathematics_marks", "statistics_marks"]


def main() -> int:
    csv_path = Path(__file__).resolve().parent / "students.csv"

    try:
        df = load_data(str(csv_path))
        validate_data(df)
    except (FileNotFoundError, ValueError) as exc:
        print(exc)
        return 1

    df = calculate_student_metrics(df, SUBJECT_COLUMNS)

    grades: list[str] = []
    statuses: list[str] = []
    for _, row in df.iterrows():
        grades.append(assign_grade(float(row["average"])))
        statuses.append(assign_pass_status(row, SUBJECT_COLUMNS))
    df["grade"] = grades
    df["status"] = statuses

    # Inspection preview
    print(f"Records: {len(df)} | Columns: {len(df.columns)}")
    print(df.dtypes.to_string())
    print(f"Missing values: {int(df.isnull().sum().sum())}")
    print()

    class_summary = analyze_class(df)
    subject_summary = analyze_subjects(df, SUBJECT_COLUMNS)
    top_df = get_top_performers(df, count=5)

    display_report(df, class_summary, subject_summary, top_df)
    return 0


if __name__ == "__main__":
    sys.exit(main())
