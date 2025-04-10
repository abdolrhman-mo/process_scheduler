"""
Helper functions and utilities for the Process Scheduler.
Contains common functions used across the application.
"""

import random
import numpy as np

def generate_random_processes(num_processes, arrival_mean=5, arrival_std=2,
                            burst_mean=3, burst_std=1, priority_lambda=3):
    """
    Generate random processes for testing.
    Args:
        num_processes: Number of processes to generate
        arrival_mean: Mean arrival time
        arrival_std: Standard deviation of arrival time
        burst_mean: Mean burst time
        burst_std: Standard deviation of burst time
        priority_lambda: Lambda for priority generation
    Returns:
        list: List of Process objects
    """
    from models import Process
    
    arrival_times = np.random.normal(arrival_mean, arrival_std, num_processes)
    burst_times = np.random.normal(burst_mean, burst_std, num_processes)
    priorities = np.random.poisson(priority_lambda, num_processes)
    
    # Ensure all values are positive
    arrival_times = np.abs(arrival_times)
    burst_times = np.abs(burst_times)
    priorities = np.abs(priorities)
    
    # Create Process objects
    processes = []
    for i in range(num_processes):
        processes.append(Process(
            pid=i+1,
            arrival_time=arrival_times[i],
            burst_time=burst_times[i],
            priority=priorities[i]
        ))
    
    return processes

def calculate_metrics(processes):
    """
    Calculate average turnaround and waiting times.
    Args:
        processes: List of Process objects
    Returns:
        tuple: (avg_turnaround_time, avg_waiting_time)
    """
    if not processes:
        return 0, 0
        
    total_turnaround = sum(p.turnaround_time for p in processes)
    total_waiting = sum(p.waiting_time for p in processes)
    n = len(processes)
    
    return total_turnaround/n, total_waiting/n 