import csv
import tempfile
import unittest
from pathlib import Path

from roti_counter import CSV_FIELDS, load_records, save_records, suggested_rotis


class RotiCounterTests(unittest.TestCase):
    def test_loads_template_sample_data(self):
        records = load_records(
            data_path=Path("/path/that/does/not/exist/data.csv"),
            template_path=Path(__file__).with_name("roti_observations_template.csv"),
        )
        self.assertEqual(len(records), 20)
        self.assertEqual(records[0]["meal"], "Lunch")

    def test_suggested_rotis_uses_matching_meal_and_day(self):
        records = [
            {"meal": "Lunch", "day_type": "Weekday", "students_eaten": "100", "rotis_cooked": "400", "rotis_left": "0"},
            {"meal": "Dinner", "day_type": "Weekday", "students_eaten": "100", "rotis_cooked": "200", "rotis_left": "0"},
        ]
        amount, count = suggested_rotis(records, "Lunch", "Weekday", 100)
        self.assertEqual((amount, count), (420, 1))

    def test_suggested_rotis_falls_back_to_meal_when_day_has_no_records(self):
        records = [
            {"meal": "Lunch", "day_type": "Weekday", "students_eaten": "100", "rotis_cooked": "400", "rotis_left": "0"},
        ]
        amount, count = suggested_rotis(records, "Lunch", "Weekend", 50)
        self.assertEqual((amount, count), (210, 1))

    def test_saves_csv_in_expected_format(self):
        record = {field: "" for field in CSV_FIELDS}
        record.update(date="2026-11-22", meal="Lunch", students_eaten=100, rotis_cooked=350, rotis_left=5)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "data.csv"
            save_records([record], path)
            with path.open(newline="", encoding="utf-8") as csv_file:
                saved = list(csv.DictReader(csv_file))
        self.assertEqual(saved, [{field: str(value) for field, value in record.items()}])


if __name__ == "__main__":
    unittest.main()
