"""Utility functions for the scheduler."""

import customtkinter as ctk
import os
from typing import List, Tuple, Optional

def show_error(message: str):
    """Show error message dialog."""
    ctk.CTkMessagebox(
        title="Error",
        message=message,
        icon="cancel"
    )

def save_results_to_file(
    execution_order: List[Tuple[int, float, float]],
    avg_tat: float,
    avg_wt: float,
    output_file: str,
    algorithm_name: str,
    arrival_times: Optional[List[float]] = None,
    burst_times: Optional[List[float]] = None,
    priorities: Optional[List[int]] = None
):
    """
    Save the scheduling results to a file.
    
    Args:
        execution_order: List of tuples (process_id, start_time, end_time)
        avg_tat: Average turnaround time
        avg_wt: Average waiting time
        output_file: Path to the output file
        algorithm_name: Name of the algorithm used
        arrival_times: List of arrival times (optional)
        burst_times: List of burst times (optional)
        priorities: List of priorities (optional)
    """
    file_exists = os.path.exists(output_file)
    
    with open(output_file, 'a' if file_exists else 'w') as f:
        if not file_exists and arrival_times is not None and burst_times is not None:
            f.write(f"Number of processes: {len(arrival_times)}\n\n")
            
            f.write("ID   ArrivalTime  BurstTime  Priority\n")
            for i in range(len(arrival_times)):
                priority = priorities[i] if priorities is not None else 0
                f.write(f"{i+1:<4} {arrival_times[i]:<12.1f} {burst_times[i]:<10.1f} {priority:<10}\n")
            f.write("\n")
        
        f.write(f"=== {algorithm_name} ===\n")
        f.write("Process Execution Order:\n")
        
        if execution_order:
            current_pid, current_start, current_end = execution_order[0]
            for pid, start, end in execution_order[1:]:
                if pid == current_pid and start == current_end:
                    current_end = end
                else:
                    f.write(f"P{current_pid+1} ({current_start:.1f} - {current_end:.1f})\n")
                    current_pid, current_start, current_end = pid, start, end
            
            f.write(f"P{current_pid+1} ({current_start:.1f} - {current_end:.1f})\n")
        
        f.write("\nPerformance Metrics:\n")
        f.write(f"Average Turnaround Time: {avg_tat:.2f}\n")
        f.write(f"Average Waiting Time: {avg_wt:.2f}\n\n\n")