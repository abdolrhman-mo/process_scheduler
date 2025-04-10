# utils.py
import customtkinter as ctk
import os

def show_error(message):
    ctk.CTkMessagebox(
        title="Error",
        message=message,
        icon="cancel"
    )

def save_results_to_file(execution_order, avg_tat, avg_wt, output_file, algorithm_name, arrival_times=None, burst_times=None, priorities=None):
    """
    Save the scheduling results to a file.
    
    Args:
        execution_order (list): List of tuples (process_id, start_time, end_time)
        avg_tat (float): Average turnaround time
        avg_wt (float): Average waiting time
        output_file (str): Path to the output file
        algorithm_name (str): Name of the algorithm used
        arrival_times (list, optional): List of arrival times
        burst_times (list, optional): List of burst times
        priorities (list, optional): List of priorities
    """
    # Check if file exists to determine if we need to write the header
    file_exists = os.path.exists(output_file)
    
    with open(output_file, 'a' if file_exists else 'w') as f:
        # Write header information if this is the first algorithm
        if not file_exists and arrival_times is not None and burst_times is not None:
            f.write(f"Number of processes: {len(arrival_times)}\n\n")
            
            # Write process details table
            f.write("ID   ArrivalTime  BurstTime  Priority\n")
            for i in range(len(arrival_times)):
                priority = priorities[i] if priorities is not None else 0
                f.write(f"{i+1:<4} {arrival_times[i]:<12.1f} {burst_times[i]:<10.1f} {priority:<10}\n")
            f.write("\n")
        
        # Write algorithm results
        f.write(f"=== {algorithm_name} ===\n")
        f.write("Process Execution Order:\n")
        
        # Group consecutive executions of the same process
        if execution_order:
            current_pid, current_start, current_end = execution_order[0]
            for pid, start, end in execution_order[1:]:
                if pid == current_pid and start == current_end:
                    # Same process continues immediately
                    current_end = end
                else:
                    # Different process or gap in execution
                    f.write(f"P{current_pid+1} ({current_start:.1f} - {current_end:.1f})\n")
                    current_pid, current_start, current_end = pid, start, end
            
            # Write the last process
            f.write(f"P{current_pid+1} ({current_start:.1f} - {current_end:.1f})\n")
        
        f.write("\nPerformance Metrics:\n")
        f.write(f"Average Turnaround Time: {avg_tat:.2f}\n")
        f.write(f"Average Waiting Time: {avg_wt:.2f}\n\n\n")