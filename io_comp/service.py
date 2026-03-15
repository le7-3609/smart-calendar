from datetime import time, timedelta, datetime
from config import DAY_START, DAY_END
from io_comp.models import TimeSlot, StartWindow
from io_comp.repository import CalendarRepository

class AvailabilityFinder:
    '''
    Service responsible for calculating valid meeting start windows.
    
    To support multiple days:
    1. Update the DAY_START and DAY_END constants or pass them as parameters.
    2. Ensure the repository returns events with full datetime objects.
    3. The logic in _calculate_free_slots remains the same as long as 
       the comparison operators (>=, -) are compatible with datetime objects.
    '''

    def __init__(self, repository: CalendarRepository):
        self.repository = repository

    def find_available_slots(self, person_list: list[str], duration: timedelta) -> list[StartWindow]:
        '''
        Finds gaps between merged busy slots that are at least 'duration' long,
        and returns the valid start window (earliest to latest start time) for each gap.
        Processes people one at a time and exits early as soon as no shared time remains.
        Currently operates on a single-day basis using datetime.time.
        '''
        if not person_list or duration.total_seconds() <= 0:
            return []  # Early exit - no people, no meeting, or non-positive duration

        combined_busy: list[TimeSlot] = []
        available: list[StartWindow] = []

        for person in person_list:
            person_events = self.repository.get_events_for_people([person])
            combined_busy.extend(person_events)
            busy_slots = self._merge_busy_slots(combined_busy)
            available = self._calculate_free_slots(busy_slots, duration)
            if not available:
                return []  # Early exit - no shared time remains after adding this person

        return available

    def _merge_busy_slots(self, slots: list[TimeSlot]) -> list[TimeSlot]:
        if not slots: return []
        sorted_slots = sorted(slots, key=lambda x: x.start)
        merged = [sorted_slots[0]]
        for current in sorted_slots[1:]:
            last = merged[-1]
            if current.start <= last.end:
                merged[-1] = TimeSlot(last.start, max(last.end, current.end))
            else:
                merged.append(current)
        return merged

    def _calculate_free_slots(self, busy_slots: list[TimeSlot], duration: timedelta) -> list[StartWindow]:
        available_slots = []
        current_time = DAY_START
        
        for slot in busy_slots:
            if self._is_gap_sufficient(current_time, slot.start, duration):
                latest_start = self._subtract_duration(slot.start, duration)
                available_slots.append(StartWindow(current_time, latest_start))
            current_time = max(current_time, slot.end)
            
        if self._is_gap_sufficient(current_time, DAY_END, duration):
            latest_start = self._subtract_duration(DAY_END, duration)
            available_slots.append(StartWindow(current_time, latest_start))
        return available_slots

    def _is_gap_sufficient(self, start: time, end: time, duration: timedelta) -> bool:
        if start >= end: return False
        gap = datetime.combine(datetime.today(), end) - datetime.combine(datetime.today(), start)
        return gap >= duration

    def _subtract_duration(self, t: time, duration: timedelta) -> time:
        return (datetime.combine(datetime.today(), t) - duration).time()