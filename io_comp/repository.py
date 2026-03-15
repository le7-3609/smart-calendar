import csv
import os
from typing import Protocol, runtime_checkable
from datetime import time
from io_comp.models import TimeSlot, ResourceNotFoundError


@runtime_checkable
class CalendarRepository(Protocol):
    def get_events_for_people(self, person_list: list[str]) -> list[TimeSlot]:
        ...


class CSVCalendarRepository:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def get_events_for_people(self, person_list: list[str]) -> list[TimeSlot]:
        try:
            with open(self.file_path, mode='r', encoding='utf-8') as file:
                reader = csv.reader(file)
                relevant_rows = filter(lambda row: len(row) >= 4 and row[0] in person_list, reader)
                return [
                    TimeSlot(time.fromisoformat(row[2]), time.fromisoformat(row[3]))
                    for row in relevant_rows
                ]
        except FileNotFoundError:
            raise ResourceNotFoundError(f"File {self.file_path} not found")


def get_default_repository() -> CalendarRepository:
    """
    Factory for the default repository used by the application.

    By centralising the choice of storage backend and its configuration
    here, switching from CSV to another persistence mechanism (e.g. a
    database) only requires changing this function and the concrete
    repository implementation in this module.
    """
    base_dir = os.path.dirname(os.path.dirname(__file__))
    csv_path = os.path.join(base_dir, "resources", "calendar.csv")
    return CSVCalendarRepository(csv_path)