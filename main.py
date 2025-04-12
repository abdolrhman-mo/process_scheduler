"""Main application entry point for the Process Scheduler."""
import customtkinter as ctk  # Enhanced UI library
import os
import numpy as np
import sys
from algorithms import (  # Import scheduling algorithms
    first_come_first_serve,
    round_robin,
    preemptive_shortest_remaining_time_first,
    non_preemptive_priority
)
from views import InputTab, ResultsTab, VisualizationTab, ComparisonTab  # UI components
from utils import show_error, save_results_to_file  # Helper functions
import matplotlib.pyplot as plt

class ProcessSchedulerApp(ctk.CTk):
    def __init__(self):
        super().__init__()  # Initialize parent class
        
        # Configure main window
        self.title("Process Scheduling Simulator")
        self.geometry("1200x800")
        
        # Set dark mode and green theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")
        
        # Initialize process data storage
        self.arrival_times = None
        self.burst_times = None
        self.priorities = None
        
        # Create data directory if not exists
        self.data_dir = os.path.join(os.path.dirname(__file__), "data")
        os.makedirs(self.data_dir, exist_ok=True)
        
        # Set up window closing protocol
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Available scheduling algorithms
        self.algorithms = {
            "FCFS": first_come_first_serve,
            "Round Robin": round_robin,
            "Preemptive SRTF": preemptive_shortest_remaining_time_first,
            "Priority Scheduling": non_preemptive_priority
        }
        
        self.create_widgets()  # Build the UI
    
    def on_closing(self):
        """Handle window closing event"""
        # Clean up any resources if needed
        if hasattr(self, 'visualization_tab'):
            plt.close('all')  # Close any matplotlib figures
        self.destroy()  # Destroy the window
        sys.exit()  # Exit the application
    
    def create_widgets(self):
        """Create all UI components"""
        # Create tabbed interface
        self.tabview = ctk.CTkTabview(master=self)
        self.tabview.pack(fill="both", expand=True)
        
        # Add tabs
        self.tabview.add("Input")
        self.tabview.add("Results") 
        self.tabview.add("Visualization")
        self.tabview.add("Comparison")
        
        # Initialize each tab with its content
        self.input_tab = InputTab(
            master=self.tabview.tab("Input"),
            on_generate=self.generate_processes
        )
        
        self.results_tab = ResultsTab(
            master=self.tabview.tab("Results"),
            on_run=self.run_selected_algorithm
        )
        
        self.visualization_tab = VisualizationTab(
            master=self.tabview.tab("Visualization"),
            algorith_var=self.results_tab.algorithm_var,
            on_run=self.run_selected_algorithm
        )
        
        self.comparison_tab = ComparisonTab(
            master=self.tabview.tab("Comparison"), 
            algorithms=self.algorithms
        )

    def generate_processes(self):
        """Generate random processes using normal distribution"""
        try:
            input_file = os.path.join(self.data_dir, "input.txt")
            # Read configuration from file
            with open(input_file) as file:
                num_processes = int(file.readline())
                arrival_mean, arrival_sd = map(float, file.readline().split())
                burst_mean, burst_sd = map(float, file.readline().split())
                priority_lambda = float(file.readline())

            # Generate random process data
            self.arrival_times = np.abs(np.random.normal(arrival_mean, arrival_sd, num_processes))
            self.burst_times = np.abs(np.random.normal(burst_mean, burst_sd, num_processes))
            self.priorities = np.abs(np.random.poisson(priority_lambda, num_processes))

            # Update input tab display
            self.input_tab.update_process_table(self.arrival_times, self.burst_times, self.priorities)

            # Update comparison data
            self.comparison_tab.update_data(
                self.arrival_times.tolist(),
                self.burst_times.tolist(),
                self.priorities.tolist()
            )

        except Exception as e:
            show_error(f"Error reading from {input_file}: {str(e)}")

    def run_selected_algorithm(self):
        """Execute the selected scheduling algorithm"""
        if self.arrival_times is None:
            show_error("Please generate processes first.")
            return

        selected_algorithm = self.results_tab.get_selected_algorithm()
        output_file = os.path.join(self.data_dir, "output.txt")
        
        if os.path.exists(output_file):
            os.remove(output_file)
        
        # Run all algorithms for comparison
        self.run_algorithm("First Come First Serve", first_come_first_serve, 
                          self.arrival_times.tolist(), self.burst_times.tolist())
        
        self.run_algorithm("Non-Preemptive Highest Priority First", non_preemptive_priority,
                          self.arrival_times.tolist(), self.burst_times.tolist(), self.priorities.tolist())
        
        self.run_algorithm("Round Robin", round_robin,
                          self.arrival_times.tolist(), self.burst_times.tolist())
        
        self.run_algorithm("Preemptive Shortest Remaining Time First", preemptive_shortest_remaining_time_first,
                          self.arrival_times.tolist(), self.burst_times.tolist())
        
        # Run selected algorithm for display
        if selected_algorithm == "FCFS":
            execution_order, avg_tat, avg_wt = first_come_first_serve(self.arrival_times.tolist(), self.burst_times.tolist())
        elif selected_algorithm == "Round Robin":
            execution_order, avg_tat, avg_wt = round_robin(self.arrival_times.tolist(), self.burst_times.tolist())
        elif selected_algorithm == "Preemptive SRTF":
            execution_order, avg_tat, avg_wt = preemptive_shortest_remaining_time_first(self.arrival_times.tolist(), self.burst_times.tolist())
        elif selected_algorithm == "Priority Scheduling":
            execution_order, avg_tat, avg_wt = non_preemptive_priority(
                self.arrival_times.tolist(), self.burst_times.tolist(), self.priorities.tolist())
        
        # Prepare results for display
        results = []
        for i, start, end in execution_order:
            arrival = self.arrival_times[i]
            turnaround = end - arrival
            results.append((i, arrival, start, end, turnaround))
        
        # Update all views
        self.results_tab.display_results(results)
        self.results_tab.update_averages(avg_tat, avg_wt)
        self.visualization_tab.update_visualization(execution_order, selected_algorithm)
        self.comparison_tab.update_data(
            self.arrival_times.tolist(),
            self.burst_times.tolist(),
            self.priorities.tolist()
        )
    
    def run_algorithm(self, algorithm_name, algorithm_func, *args):
        """Run a specific algorithm and save results"""
        execution_order, avg_tat, avg_wt = algorithm_func(*args)
        output_file = os.path.join(self.data_dir, "output.txt")
        
        save_results_to_file(
            execution_order, 
            avg_tat, 
            avg_wt, 
            output_file, 
            algorithm_name,
            self.arrival_times.tolist(),
            self.burst_times.tolist(),
            self.priorities.tolist() if algorithm_name == "Priority Scheduling" else None
        )

if __name__ == "__main__":
    app = ProcessSchedulerApp()  # Create application instance
    app.mainloop()  # Start the event loop 