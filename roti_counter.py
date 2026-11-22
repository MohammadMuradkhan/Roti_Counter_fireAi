"""Data loading and forecasting helpers for the Jhelum Mess Roti Counter."""

import csv
import math
from pathlib import Path
from typing import Any


TEMPLATE_PATH = Path(__file__).with_name("roti_observations_template.csv")
DATA_PATH = Path(__file__).with_name("data.csv")

CSV_FIELDS = [
    "date",
    "meal",
    "time_noted",
    "spot",
    "day_type",
    "students_eaten",
    "rotis_cooked",
    "rotis_left",
    "ran_out",
    "ran_out_time",
    "note",
]


def load_records(data_path: Path = DATA_PATH, template_path: Path = TEMPLATE_PATH) -> list[dict[str, str]]:
    """Load saved observations, or the provided sample observations on first run."""
    source = data_path if data_path.exists() else template_path
    with source.open(newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        missing_fields = set(CSV_FIELDS) - set(reader.fieldnames or [])
        if missing_fields:
            raise ValueError(f"{source.name} is missing columns: {', '.join(sorted(missing_fields))}")
        return list(reader)


def save_records(records: list[dict[str, Any]], data_path: Path = DATA_PATH) -> None:
    """Persist observations using the project's CSV data format."""
    with data_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerows(records)


def suggested_rotis(
    records: list[dict[str, Any]],
    meal: str,
    day_type: str,
    expected_students: int,
    buffer: float = 0.05,
) -> tuple[int, int]:
    """Estimate rotis from similar observations and return amount plus sample size."""
    matches = [
        row
        for row in records
        if row["meal"] == meal and row["day_type"] == day_type
    ]
    if not matches:
        matches = [row for row in records if row["meal"] == meal]
    if not matches:
        matches = records
    if not matches:
        return 0, 0

    students = sum(int(row["students_eaten"]) for row in matches)
    consumed = sum(int(row["rotis_cooked"]) - int(row["rotis_left"]) for row in matches)
    if students <= 0:
        return 0, len(matches)
    per_student = consumed / students
    return math.ceil(expected_students * per_student * (1 + buffer)), len(matches)
