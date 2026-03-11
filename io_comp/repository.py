import csv
from abc import ABC, abstractmethod
from datetime import time
from io_comp.models import TimeSlot

class CalendarRepository(ABC):
    @abstractmethod
    def get_events_for_people(self, person_list: list[str]) -> list[TimeSlot]:
        pass

class CSVCalendarRepository(CalendarRepository):
    def __init__(self, file_path: str):
        self.file_path = file_path

    def get_events_for_people(self, person_list: list[str]) -> list[TimeSlot]:
        events = []
        try:
            with open(self.file_path, mode='r', encoding='utf-8') as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) < 4: continue
                    name, _, start, end = row
                    if name in person_list:
                        events.append(TimeSlot(time.fromisoformat(start), time.fromisoformat(end)))
        except FileNotFoundError:
            print(f"Error: File {self.file_path} not found.")
        return events