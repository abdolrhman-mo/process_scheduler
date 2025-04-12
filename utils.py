"""Utility functions for the scheduler."""
import customtkinter as ctk
import os
from typing import List, Tuple, Optional
from tkinter import ttk
from CTkMessagebox import CTkMessagebox

def show_error(message: str):
    """Show error message dialog"""
    CTkMessagebox(
        title="Error",
        message=message,
        icon="cancel"
    )

def create_title(parent, text, font_size=18):
    """
    Create a consistent title label for tabs.
    
    Args:
        parent: The parent widget
        text: The title text
        font_size: Font size for the title (default: 18)
    
    Returns:
        The created title label widget
    """
    title_label = ctk.CTkLabel(
        parent,
        text=text,
        font=ctk.CTkFont(size=font_size, weight="bold")
    )
    title_label.pack(pady=10)
    return title_label

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
        execution_order: List of (process_id, start_time, end_time)
        avg_tat: Average turnaround time
        avg_wt: Average waiting time
        output_file: Path to output file
        algorithm_name: Name of algorithm used
        arrival_times: Optional arrival times
        burst_times: Optional burst times
        priorities: Optional priorities
    """
    file_exists = os.path.exists(output_file)
    
    with open(output_file, 'a' if file_exists else 'w') as f:
        # Write process data if new file
        if not file_exists and arrival_times is not None and burst_times is not None:
            f.write(f"Number of processes: {len(arrival_times)}\n\n")
            
            f.write("ID   ArrivalTime  BurstTime  Priority\n")
            for i in range(len(arrival_times)):
                priority = priorities[i] if priorities is not None else 0
                f.write(f"{i+1:<4} {arrival_times[i]:<12.1f} {burst_times[i]:<10.1f} {priority:<10}\n")
            f.write("\n")
        
        # Write algorithm results
        f.write(f"=== {algorithm_name} ===\n")
        f.write("Process Execution Order:\n")
        
        if execution_order:
            # Combine continuous execution periods
            current_pid, current_start, current_end = execution_order[0]
            for pid, start, end in execution_order[1:]:
                if pid == current_pid and start == current_end:
                    current_end = end
                else:
                    f.write(f"P{current_pid+1} ({current_start:.1f} - {current_end:.1f})\n")
                    current_pid, current_start, current_end = pid, start, end
            
            f.write(f"P{current_pid+1} ({current_start:.1f} - {current_end:.1f})\n")
        
        # Write performance metrics
        f.write("\nPerformance Metrics:\n")
        f.write(f"Average Turnaround Time: {avg_tat:.2f}\n")
        f.write(f"Average Waiting Time: {avg_wt:.2f}\n\n\n")

def configure_treeview_styles(tree):
    """Configure styling for Treeview widgets"""
    style = ttk.Style()
    style.theme_use('default')

    # Main treeview style
    style.configure("Enhanced.Treeview",
        background="#3b3b3b",
        foreground="white",
        rowheight=38,
        fieldbackground="#2a2d2e",
        bordercolor="#3b3b3b",
        borderwidth=0,
        font=('Segoe UI', 12),
        padding=(10, 5),
        anchor="center"                
    )

    # Header style
    style.configure("Enhanced.Treeview.Heading",
        background="#1a1a1a",
        foreground="white",
        relief="flat",
        font=('Segoe UI', 12, 'bold'),
        padding=(12, 8),
        anchor="center"
    )

    # Selected row styling
    style.map("Enhanced.Treeview",
        background=[('selected', '#3b3b3b')],
        foreground=[('selected', 'white')]
    )

    style.map("Enhanced.Treeview.Heading",
        background=[('hover', '#3b3b3b')]
    )

    # Center align all columns
    for col in tree["columns"]:
        tree.column(col, anchor="center")
        tree.heading(col, anchor="center") 