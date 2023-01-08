from dataclasses import dataclass
from datetime import datetime, timedelta, date


@dataclass(frozen=True)
class DateFormatter:
    "Always UTC"

    @property
    def iso_8601(self):
        return "%Y-%M-%d"

    @staticmethod
    def get_yesterday() -> date:
        "in UTC"
        return datetime.utcnow().date() - timedelta(1)

    def format_iso_8601(self, dt: datetime) -> str:
        return dt.strftime(self.iso_8601)

    @staticmethod
    def check_date_format(date_str: str, fmt: str) -> str:
        new_date = datetime.strptime(date_str, fmt)
        new_date.strftime(fmt)
        return date_str

    def check_iso_8601(self, date_str: str) -> str:
        return self.check_date_format(date_str, self.iso_8601)

    @staticmethod
    def add_start_of_day_time(date_str: str) -> str:
        "Adds midnight to a date string"
        return f"{date_str}T00:00:00Z"

    @staticmethod
    def add_end_of_day_time(date_str: str) -> str:
        "Adds 11:59PM to a date string"
        return f"{date_str}T23:59:59Z"
