"""
Data structures for the Process Scheduler.
Contains classes and data models used throughout the application.
"""

class Process:
    """
    Represents a process in the scheduling system.
    """
    def __init__(self, pid, arrival_time, burst_time, priority=0):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.priority = priority
        self.remaining_time = burst_time
        self.completion_time = 0
        self.turnaround_time = 0
        self.waiting_time = 0

    def __str__(self):
        return f"P{self.pid} (AT: {self.arrival_time}, BT: {self.burst_time}, P: {self.priority})" 