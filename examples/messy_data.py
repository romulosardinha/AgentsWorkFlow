import csv
from pathlib import Path


class DataProcessor:
    def __init__(self, source):
        self.source = Path(source)
        self.rows = []

    def load(self):
        with self.source.open(newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            self.rows = list(reader)
        return self

    def filter_by(self, column, value):
        self.rows = [r for r in self.rows if r.get(column) == value]
        return self

    def column_values(self, column):
        return [r[column] for r in self.rows if column in r]

    def save_as(self, target):
        target = Path(target)
        if not self.rows:
            target.write_text("", encoding="utf-8")
            return
        with target.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(self.rows[0].keys()))
            writer.writeheader()
            writer.writerows(self.rows)


def parse_int_column(rows, column):
    return [int(r[column]) for r in rows if r.get(column, "").strip()]


def summarize(values):
    if not values:
        return {"count": 0, "min": None, "max": None, "avg": None}
    return {
        "count": len(values),
        "min": min(values),
        "max": max(values),
        "avg": sum(values) / len(values),
    }
