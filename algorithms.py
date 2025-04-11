"""Scheduling algorithms implementation."""
import numpy as np
from typing import List, Tuple

def first_come_first_serve(arrival_times: List[float], burst_times: List[float]) -> Tuple[List[Tuple[int, float, float]], float, float]:
    """
    First Come First Serve scheduling algorithm.
    Processes are executed in order of arrival.
    """
    num_processes = len(arrival_times)
    # Sort processes by arrival time
    sorted_processes = sorted(range(num_processes), key=lambda i: arrival_times[i])

    current_time = 0
    total_turnaround = 0
    total_waiting = 0
    execution_order = []

    for i in sorted_processes:
        # Handle idle time between processes
        if arrival_times[i] > current_time:
            current_time = arrival_times[i]
        
        # Record execution period
        execution_order.append((i, current_time, current_time + burst_times[i]))

        # Calculate metrics
        turnaround = (current_time + burst_times[i]) - arrival_times[i]
        waiting = turnaround - burst_times[i]
        total_turnaround += turnaround
        total_waiting += waiting

        current_time += burst_times[i]  # Move to next process

    # Calculate averages
    avg_turnaround = total_turnaround / num_processes
    avg_waiting = total_waiting / num_processes

    return execution_order, avg_turnaround, avg_waiting

def round_robin(arrival_times: List[float], burst_times: List[float], quantum: float = 2) -> Tuple[List[Tuple[int, float, float]], float, float]:
    """
    Round Robin scheduling algorithm.
    Each process gets a fixed time quantum before switching.
    """
    n = len(arrival_times)
    remaining = burst_times.copy()  # Track remaining burst time
    complete = [False] * n  # Completion status
    time = 0
    execution_order = []
    waiting_time = [0] * n
    turnaround_time = [0] * n

    # Prepare process list sorted by arrival time
    processes = [(i, arrival_times[i], burst_times[i]) for i in range(n)]
    processes.sort(key=lambda x: x[1])

    time = min(arrival_times)  # Start at first arrival
    ready_queue = []
    visited = [False] * n  # Track if process entered queue

    while not all(complete):
        # Add newly arrived processes to queue
        for i, arrival, _ in processes:
            if arrival <= time and not visited[i]:
                ready_queue.append(i)
                visited[i] = True

        if not ready_queue:
            time += 0.1  # No processes ready, increment time
            time = round(time, 1)
            continue

        current = ready_queue.pop(0)  # Get next process

        # Execute for quantum or remaining time
        exec_start = time
        exec_time = min(quantum, remaining[current])
        time += exec_time
        time = round(time, 1)
        remaining[current] -= exec_time
        execution_order.append((current, exec_start, time))

        # Check for new arrivals during execution
        for i, arrival, _ in processes:
            if arrival <= time and not visited[i]:
                ready_queue.append(i)
                visited[i] = True

        if remaining[current] > 0:
            ready_queue.append(current)  # Requeue if not finished
        else:
            complete[current] = True  # Mark complete
            turnaround_time[current] = time - arrival_times[current]
            waiting_time[current] = turnaround_time[current] - burst_times[current]

    # Calculate averages
    avg_turnaround_time = sum(turnaround_time) / n
    avg_waiting_time = sum(waiting_time) / n
    return execution_order, avg_turnaround_time, avg_waiting_time

def preemptive_shortest_remaining_time_first(arrival_times: List[float], burst_times: List[float]) -> Tuple[List[Tuple[int, float, float]], float, float]:
    """
    Preemptive Shortest Remaining Time First algorithm.
    Always executes the process with shortest remaining time.
    """
    num_processes = len(arrival_times)
    remaining_burst = burst_times.copy()
    complete = [False] * num_processes
    current_time = min(arrival_times)
    execution_order = []
    waiting_time = [0] * num_processes
    turnaround_time = [0] * num_processes
    processes_completed = 0
    last_process = -1  # Track last executed process

    while processes_completed < num_processes:
        # Get ready processes
        ready_queue = [i for i in range(num_processes)
                       if arrival_times[i] <= current_time and not complete[i]]

        if ready_queue:
            # Select process with shortest remaining time
            current_process = min(ready_queue, key=lambda i: remaining_burst[i])

            # Record context switch
            if last_process != current_process:
                execution_order.append((current_process, current_time))
            last_process = current_process

            # Execute for 0.1 time unit
            remaining_burst[current_process] -= 0.1
            remaining_burst[current_process] = max(0, remaining_burst[current_process])

            # Check if process completed
            if remaining_burst[current_process] == 0:
                complete[current_process] = True
                processes_completed += 1
                finish_time = current_time + 0.1
                turnaround_time[current_process] = finish_time - arrival_times[current_process]
                waiting_time[current_process] = turnaround_time[current_process] - burst_times[current_process]
                execution_order[-1] += (finish_time,)  # Add end time
                last_process = -1

        current_time += 0.1
        current_time = round(current_time, 2)

    # Ensure all execution periods have end times
    for i in range(len(execution_order)):
        if len(execution_order[i]) == 2:
            execution_order[i] += (execution_order[i][1] + 0.1,)

    # Calculate averages
    avg_turnaround_time = sum(turnaround_time) / num_processes
    avg_waiting_time = sum(waiting_time) / num_processes

    return execution_order, avg_turnaround_time, avg_waiting_time

def non_preemptive_priority(arrival_times: List[float], burst_times: List[float], priorities: List[int]) -> Tuple[List[Tuple[int, float, float]], float, float]:
    """
    Non-preemptive Priority scheduling algorithm.
    Executes highest priority process first (lower number = higher priority).
    """
    current_time = min(arrival_times)
    total_turnaround_time = 0
    total_waiting_time = 0
    processes_completed = 0
    num_processes = len(arrival_times)

    # Create process dictionary list
    process_list = []
    for i in range(num_processes):
        process_list.append({
            'arrival': arrival_times[i],
            'burst': burst_times[i],
            'priority': priorities[i]
        })

    processes_done = [False] * num_processes
    execution_order = []

    while processes_completed < num_processes:
        # Find ready processes
        ready = []
        for i in range(num_processes):
            if process_list[i]['arrival'] <= current_time and not processes_done[i]:
                ready.append((i, process_list[i]))

        if not ready:
            current_time += 1  # No processes ready
            continue

        # Sort by priority (descending) and arrival time
        ready.sort(key=lambda x: (-x[1]['priority'], x[1]['arrival']))
        i, process = ready[0]  # Get highest priority process

        # Execute entire process (non-preemptive)
        process['start'] = current_time
        process['finish'] = current_time + process['burst']
        process['turnaround'] = process['finish'] - process['arrival']
        process['waiting'] = process['start'] - process['arrival']

        total_turnaround_time += process['turnaround']
        total_waiting_time += process['waiting']

        execution_order.append((i, process['start'], process['finish']))

        current_time = process['finish']
        processes_done[i] = True
        processes_completed += 1

    # Calculate averages
    avg_turnaround_time = total_turnaround_time / num_processes
    avg_waiting_time = total_waiting_time / num_processes

    return execution_order, avg_turnaround_time, avg_waiting_time