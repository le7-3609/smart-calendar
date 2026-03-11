import pytest
from datetime import timedelta, time
from io_comp.models import TimeSlot, StartWindow
from io_comp.service import AvailabilityFinder
from io_comp.repository import CalendarRepository

class MockCalendarRepo(CalendarRepository):
    def __init__(self, events): self.events = events
    def get_events_for_people(self, person_list): return self.events

# --- HAPPY PATH TESTS ---

def test_full_day_available():
    """Test a case where there are no events at all - the whole day is free.
    With a 12-hour meeting filling the full 7:00-19:00 window, the only valid start is 7:00."""
    repo = MockCalendarRepo([])
    finder = AvailabilityFinder(repo)
    slots = finder.find_available_slots(["Alice"], timedelta(hours=12))
    assert len(slots) == 1
    assert slots[0].earliest == time(7, 0)
    assert slots[0].latest == time(7, 0) 

def test_typical_scenario():
    """Test a typical scenario with gaps between meetings.
    Free windows: 7:00-9:00 (latest start 8:00) and 10:00-19:00 (latest start 18:00)."""
    events = [TimeSlot(time(9, 0), time(10, 0))]
    finder = AvailabilityFinder(MockCalendarRepo(events))
    slots = finder.find_available_slots(["Alice"], timedelta(minutes=60))
    assert len(slots) == 2
    assert slots[0].earliest == time(7, 0)
    assert slots[0].latest == time(8, 0)   
    assert slots[1].earliest == time(10, 0)
    assert slots[1].latest == time(18, 0)  

# --- UNHAPPY / EDGE CASE TESTS ---

def test_no_available_slots():
    """Test a case where the day is fully booked - no slots should be returned"""
    events = [TimeSlot(time(7, 0), time(19, 0))]
    finder = AvailabilityFinder(MockCalendarRepo(events))
    slots = finder.find_available_slots(["Alice"], timedelta(minutes=15))
    assert len(slots) == 0

def test_duration_longer_than_gap():
    """Test a case where there is a free window but it is shorter than the requested duration"""
    events = [TimeSlot(time(7, 0), time(11, 0)), TimeSlot(time(12, 0), time(19, 0))]
    finder = AvailabilityFinder(MockCalendarRepo(events))
    slots = finder.find_available_slots(["Alice"], timedelta(minutes=90))
    assert len(slots) == 0

def test_overlapping_events_merge():
    """Test that the system correctly merges overlapping events.
    Merged busy: 8:00-11:00. Free windows: 7:00-8:00 and 11:00-19:00."""
    events = [
        TimeSlot(time(8, 0), time(10, 0)),
        TimeSlot(time(9, 0), time(11, 0)) 
    ]
    finder = AvailabilityFinder(MockCalendarRepo(events))
    slots = finder.find_available_slots(["Alice"], timedelta(minutes=60))
    assert slots[0].earliest == time(7, 0)
    assert slots[0].latest == time(7, 0)   
    assert slots[1].earliest == time(11, 0)
    assert slots[1].latest == time(18, 0) 

def test_person_not_in_system():
    """Test a case where the person is not in the system - the system should assume they are always available"""
    repo = MockCalendarRepo([]) 
    finder = AvailabilityFinder(repo)
    
    slots = finder.find_available_slots(["UnknownPerson"], timedelta(hours=12))
    
    assert len(slots) == 1
    assert slots[0].earliest == time(7, 0)
    assert slots[0].latest == time(7, 0)  

def test_no_mutual_availability():
    """Test a case where there is no mutual availability - an empty list should be returned"""
    events = [
        TimeSlot(time(7, 0), time(13, 0)), 
        TimeSlot(time(13, 0), time(19, 0)) 
    ]
    finder = AvailabilityFinder(MockCalendarRepo(events))
    
    slots = finder.find_available_slots(["Alice", "Bob"], timedelta(minutes=30))
    
    assert len(slots) == 0

def test_start_window_is_narrower_than_free_slot():
    """Test the core behaviour: a 90-min free window with a 60-min meeting gives a 30-min start window."""
    events = [TimeSlot(time(7, 0), time(8, 30)), TimeSlot(time(10, 0), time(19, 0))]
    finder = AvailabilityFinder(MockCalendarRepo(events))
    slots = finder.find_available_slots(["Alice"], timedelta(minutes=60))
    assert len(slots) == 1
    assert slots[0].earliest == time(8, 30)   
    assert slots[0].latest == time(9, 0)     