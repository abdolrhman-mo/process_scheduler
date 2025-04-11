"""Main application entry point for the Process Scheduler."""

import customtkinter as ctk
import os
import numpy as np
from algorithms import (
    first_come_first_serve,
    round_robin,
    preemptive_shortest_remaining_time_first,
    non_preemptive_priority
)
from views import InputTab, ResultsTab, VisualizationTab, ComparisonTab
from utils import show_error, save_results_to_file

class ProcessSchedulerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Process Scheduling Simulator")
        self.geometry("1200x800")
        
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")
        
        self.arrival_times = None
        self.burst_times = None
        self.priorities = None
        
        self.data_dir = os.path.join(os.path.dirname(__file__), "data")
        os.makedirs(self.data_dir, exist_ok=True)
        
        self.algorithms = {
            "FCFS": first_come_first_serve,
            "Round Robin": round_robin,
            "Preemptive SRTF": preemptive_shortest_remaining_time_first,
            "Priority Scheduling": non_preemptive_priority
        }
        
        self.create_widgets()
    
    def create_widgets(self):
        self.tabview = ctk.CTkTabview(master=self)
        self.tabview.pack(fill="both", expand=True)
        
        self.tabview.add("Input")
        self.tabview.add("Results") 
        self.tabview.add("Visualization")
        self.tabview.add("Comparison")
        
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
        try:
            input_file = os.path.join(self.data_dir, "input.txt")
            with open(input_file) as file:
                num_processes = int(file.readline())
                arrival_mean, arrival_sd = map(float, file.readline().split())
                burst_mean, burst_sd = map(float, file.readline().split())
                priority_lambda = float(file.readline())

            self.arrival_times = np.abs(np.random.normal(arrival_mean, arrival_sd, num_processes))
            self.burst_times = np.abs(np.random.normal(burst_mean, burst_sd, num_processes))
            self.priorities = np.abs(np.random.poisson(priority_lambda, num_processes))

            self.input_tab.update_process_table(self.arrival_times, self.burst_times, self.priorities)

            # Update comparison tab with new data
            self.comparison_tab.update_data(
                self.arrival_times.tolist(),
                self.burst_times.tolist(),
                self.priorities.tolist()
            )

        except Exception as e:
            show_error(f"Error reading from {input_file}: {str(e)}")

    def run_selected_algorithm(self):
        if self.arrival_times is None:
            show_error("Please generate processes first.")
            return

        selected_algorithm = self.results_tab.get_selected_algorithm()
        output_file = os.path.join(self.data_dir, "output.txt")
        
        if os.path.exists(output_file):
            os.remove(output_file)
        
        # Run all algorithms and save results
        self.run_algorithm("First Come First Serve", first_come_first_serve, 
                          self.arrival_times.tolist(), self.burst_times.tolist())
        
        self.run_algorithm("Non-Preemptive Highest Priority First", non_preemptive_priority,
                          self.arrival_times.tolist(), self.burst_times.tolist(), self.priorities.tolist())
        
        self.run_algorithm("Round Robin", round_robin,
                          self.arrival_times.tolist(), self.burst_times.tolist())
        
        self.run_algorithm("Preemptive Shortest Remaining Time First", preemptive_shortest_remaining_time_first,
                          self.arrival_times.tolist(), self.burst_times.tolist())
        
        # Run the selected algorithm for display
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
        
        # Update the views
        self.results_tab.display_results(results)
        self.results_tab.update_averages(avg_tat, avg_wt)
        self.visualization_tab.update_visualization(execution_order, selected_algorithm)
        
        # Update comparison tab
        self.comparison_tab.update_data(
            self.arrival_times.tolist(),
            self.burst_times.tolist(),
            self.priorities.tolist()
        )
    
    def run_algorithm(self, algorithm_name, algorithm_func, *args):
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
    app = ProcessSchedulerApp()
    app.mainloop()