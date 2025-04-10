"""
Scheduling algorithms implementation.
Contains all the CPU scheduling algorithms used in the application.
"""

def first_come_first_serve(processes):
    """
    First Come First Serve scheduling algorithm.
    Args:
        processes: List of Process objects
    Returns:
        tuple: (execution_order, avg_turnaround_time, avg_waiting_time)
    """
    pass

def round_robin(processes, quantum=2):
    """
    Round Robin scheduling algorithm.
    Args:
        processes: List of Process objects
        quantum: Time quantum for each process
    Returns:
        tuple: (execution_order, avg_turnaround_time, avg_waiting_time)
    """
    pass

def preemptive_srtf(processes):
    """
    Preemptive Shortest Remaining Time First scheduling algorithm.
    Args:
        processes: List of Process objects
    Returns:
        tuple: (execution_order, avg_turnaround_time, avg_waiting_time)
    """
    pass

def non_preemptive_priority(processes):
    """
    Non-preemptive Priority scheduling algorithm.
    Args:
        processes: List of Process objects
    Returns:
        tuple: (execution_order, avg_turnaround_time, avg_waiting_time)
    """
    pass 