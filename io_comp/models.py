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