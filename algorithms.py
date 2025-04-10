"""Scheduling algorithms implementation."""

import numpy as np
from typing import List, Tuple

def first_come_first_serve(arrival_times: List[float], burst_times: List[float]) -> Tuple[List[Tuple[int, float, float]], float, float]:
    """
    First Come First Serve scheduling algorithm.
    Args:
        arrival_times: List of arrival times
        burst_times: List of burst times
    Returns:
        tuple: (execution_order, avg_turnaround_time, avg_waiting_time)
    """
    num_processes = len(arrival_times)
    sorted_processes = sorted(range(num_processes), key=lambda i: arrival_times[i])

    current_time = 0
    total_turnaround = 0
    total_waiting = 0
    execution_order = []

    for i in sorted_processes:
        if arrival_times[i] > current_time:
            current_time = arrival_times[i]
        execution_order.append((i, current_time, current_time + burst_times[i]))

        turnaround = (current_time + burst_times[i]) - arrival_times[i]
        waiting = turnaround - burst_times[i]
        total_turnaround += turnaround
        total_waiting += waiting

        current_time += burst_times[i]

    avg_turnaround = total_turnaround / num_processes
    avg_waiting = total_waiting / num_processes

    return execution_order, avg_turnaround, avg_waiting

def round_robin(arrival_times: List[float], burst_times: List[float], quantum: float = 2) -> Tuple[List[Tuple[int, float, float]], float, float]:
    """
    Round Robin scheduling algorithm.
    Args:
        arrival_times: List of arrival times
        burst_times: List of burst times
        quantum: Time quantum for each process
    Returns:
        tuple: (execution_order, avg_turnaround_time, avg_waiting_time)
    """
    n = len(arrival_times)
    remaining = burst_times.copy()
    complete = [False] * n
    time = 0
    execution_order = []
    waiting_time = [0] * n
    turnaround_time = [0] * n

    processes = [(i, arrival_times[i], burst_times[i]) for i in range(n)]
    processes.sort(key=lambda x: x[1])

    time = min(arrival_times)
    ready_queue = []
    visited = [False] * n

    while not all(complete):
        for i, arrival, _ in processes:
            if arrival <= time and not visited[i]:
                ready_queue.append(i)
                visited[i] = True

        if not ready_queue:
            time += 0.1
            time = round(time, 1)
            continue

        current = ready_queue.pop(0)

        exec_start = time
        exec_time = min(quantum, remaining[current])
        time += exec_time
        time = round(time, 1)
        remaining[current] -= exec_time
        execution_order.append((current, exec_start, time))

        for i, arrival, _ in processes:
            if arrival <= time and not visited[i]:
                ready_queue.append(i)
                visited[i] = True

        if remaining[current] > 0:
            ready_queue.append(current)
        else:
            complete[current] = True
            turnaround_time[current] = time - arrival_times[current]
            waiting_time[current] = turnaround_time[current] - burst_times[current]

    avg_turnaround_time = sum(turnaround_time) / n
    avg_waiting_time = sum(waiting_time) / n
    return execution_order, avg_turnaround_time, avg_waiting_time

def preemptive_shortest_remaining_time_first(arrival_times: List[float], burst_times: List[float]) -> Tuple[List[Tuple[int, float, float]], float, float]:
    """
    Preemptive Shortest Remaining Time First scheduling algorithm.
    Args:
        arrival_times: List of arrival times
        burst_times: List of burst times
    Returns:
        tuple: (execution_order, avg_turnaround_time, avg_waiting_time)
    """
    num_processes = len(arrival_times)
    remaining_burst = burst_times.copy()
    complete = [False] * num_processes
    current_time = min(arrival_times)
    execution_order = []
    waiting_time = [0] * num_processes
    turnaround_time = [0] * num_processes
    processes_completed = 0
    last_process = -1

    while processes_completed < num_processes:
        ready_queue = [i for i in range(num_processes)
                       if arrival_times[i] <= current_time and not complete[i]]

        if ready_queue:
            current_process = min(ready_queue, key=lambda i: remaining_burst[i])

            if last_process != current_process:
                execution_order.append((current_process, current_time))
            last_process = current_process

            remaining_burst[current_process] -= 0.1
            remaining_burst[current_process] = max(0, remaining_burst[current_process])

            if remaining_burst[current_process] == 0:
                complete[current_process] = True
                processes_completed += 1
                finish_time = current_time + 0.1
                turnaround_time[current_process] = finish_time - arrival_times[current_process]
                waiting_time[current_process] = turnaround_time[current_process] - burst_times[current_process]
                execution_order[-1] += (finish_time,)
                last_process = -1

        current_time += 0.1
        current_time = round(current_time, 2)

    execution_timeline = []
    for i in range(len(execution_order)):
        if len(execution_order[i]) == 2:
            execution_order[i] += (execution_order[i][1] + 0.1,)

    avg_turnaround_time = sum(turnaround_time) / num_processes
    avg_waiting_time = sum(waiting_time) / num_processes

    return execution_order, avg_turnaround_time, avg_waiting_time

def non_preemptive_priority(arrival_times: List[float], burst_times: List[float], priorities: List[int]) -> Tuple[List[Tuple[int, float, float]], float, float]:
    """
    Non-preemptive Priority scheduling algorithm.
    Args:
        arrival_times: List of arrival times
        burst_times: List of burst times
        priorities: List of priorities
    Returns:
        tuple: (execution_order, avg_turnaround_time, avg_waiting_time)
    """
    current_time = min(arrival_times)
    total_turnaround_time = 0
    total_waiting_time = 0
    processes_completed = 0
    num_processes = len(arrival_times)

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
        ready = []
        for i in range(num_processes):
            if process_list[i]['arrival'] <= current_time and not processes_done[i]:
                ready.append((i, process_list[i]))

        if not ready:
            current_time += 1
            continue

        ready.sort(key=lambda x: (-x[1]['priority'], x[1]['arrival']))
        i, process = ready[0]

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

    avg_turnaround_time = total_turnaround_time / num_processes
    avg_waiting_time = total_waiting_time / num_processes

    return execution_order, avg_turnaround_time, avg_waiting_time