from datetime import datetime, timedelta


class DateFormatter:
    "Always UTC"

    def __init__(self):
        super(DateFormatter, self).__init__()
        self.iso_8601 = "%Y-%M-%d"

    @staticmethod
    def get_yesterday() -> datetime:
        "in UTC"
        return datetime.utcnow().date() - timedelta(1)

    def format_iso_8601(self, date: datetime) -> str:
        return date.strftime(self.iso_8601)

    @staticmethod
    def check_date_format(date: str, fmt: str) -> str:
        new_date = datetime.strptime(date, fmt)
        new_date.strftime(fmt)
        return date

    def check_iso_8601(self, date: str) -> str:
        return self.check_date_format(date, self.iso_8601)

    @staticmethod
    def add_start_of_day_time(date: str) -> str:
        "Adds midnight to a date string"
        return f"{date}T00:00:00Z"

    @staticmethod
    def add_end_of_day_time(date: str) -> str:
        "Adds 11:59PM to a date string"
        return f"{date}T23:59:59Z"
