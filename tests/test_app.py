import pytest
from datetime import timedelta, time
from io_comp.models import TimeSlot
from io_comp.service import AvailabilityFinder
from io_comp.repository import CalendarRepository

class MockCalendarRepo(CalendarRepository):
    def __init__(self, events): self.events = events
    def get_events_for_people(self, person_list): return self.events

# --- HAPPY PATH TESTS ---

def test_full_day_available():
    """Test a case where there are no events at all - the whole day is free"""
    repo = MockCalendarRepo([])
    finder = AvailabilityFinder(repo)
    slots = finder.find_available_slots(["Alice"], timedelta(hours=12))
    assert len(slots) == 1
    assert slots[0].start == time(7, 0)
    assert slots[0].end == time(19, 0)

def test_typical_scenario():
    """Test a typical scenario with gaps between meetings"""
    events = [TimeSlot(time(9, 0), time(10, 0))]
    finder = AvailabilityFinder(MockCalendarRepo(events))
    slots = finder.find_available_slots(["Alice"], timedelta(minutes=60))
    assert len(slots) == 2
    assert slots[0].start == time(7, 0)
    assert slots[1].start == time(10, 0)

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
    """Test that the system correctly merges overlapping events"""
    events = [
        TimeSlot(time(8, 0), time(10, 0)),
        TimeSlot(time(9, 0), time(11, 0)) 
    ]
    finder = AvailabilityFinder(MockCalendarRepo(events))
    slots = finder.find_available_slots(["Alice"], timedelta(minutes=60))
    assert slots[0].end == time(8, 0)
    assert slots[1].start == time(11, 0)

def test_person_not_in_system():
    """Test a case where the person is not in the system - the system should assume they are always available"""
    repo = MockCalendarRepo([]) 
    finder = AvailabilityFinder(repo)
    
    slots = finder.find_available_slots(["UnknownPerson"], timedelta(hours=12))
    
    assert len(slots) == 1
    assert slots[0].start == time(7, 0)
    assert slots[0].end == time(19, 0)

def test_no_mutual_availability():
    """Test a case where there is no mutual availability - an empty list should be returned"""
    events = [
        TimeSlot(time(7, 0), time(13, 0)), 
        TimeSlot(time(13, 0), time(19, 0)) 
    ]
    finder = AvailabilityFinder(MockCalendarRepo(events))
    
    slots = finder.find_available_slots(["Alice", "Bob"], timedelta(minutes=30))
    
    assert len(slots) == 0