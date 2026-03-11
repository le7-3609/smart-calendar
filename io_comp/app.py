import os
from datetime import timedelta
from io_comp.repository import CSVCalendarRepository
from io_comp.service import AvailabilityFinder

def main():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    csv_path = os.path.join(base_dir, 'resources', 'calendar.csv')
    
    repo = CSVCalendarRepository(csv_path)
    finder = AvailabilityFinder(repo)
    
    people = ["Alice","Bob","Jack"]
    duration = timedelta(minutes=60)
    
    available_slots = finder.find_available_slots(people, duration)
    
    for slot in available_slots:
        print(f"Starting Time of available slots: {slot.start.strftime('%H:%M')} - {slot.end.strftime('%H:%M')}")

if __name__ == "__main__":
    main()