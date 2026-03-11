from dataclasses import dataclass
from datetime import time

@dataclass(frozen=True)
class TimeSlot:
    '''
    Represents a period of time. 
    To extend this to a multi-day calendar, change the type of 'start' and 'end' 
    from datetime.time to datetime.datetime.
    '''
    start: time
    end: time

@dataclass(frozen=True)
class StartWindow:
    '''
    Represents the valid range of start times for a meeting within a free slot.
    'earliest' is the first possible start time; 'latest' is the last possible
    start time that still allows the meeting to finish within the free slot.
    When earliest == latest, there is exactly one valid start time.
    '''
    earliest: time
    latest: time