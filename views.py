import customtkinter as ctk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from typing import Callable, List, Tuple, Optional, Dict, Any
import numpy as np
from utils import configure_treeview_styles, create_title

ALGORITHMS = ["FCFS", "Round Robin", "Preemptive SRTF", "Priority Scheduling"]

def create_algorithm_controls(self, parent, on_run: Callable, algorithm_var: ctk.StringVar):
    ctk.CTkButton(parent, text="Run Algorithm", command=on_run).pack(side="left", padx=10)
    ctk.CTkOptionMenu(parent, values=ALGORITHMS, variable=algorithm_var).pack(side="left")


class InputTab(ctk.CTkFrame):
    def __init__(self, master, on_generate: Callable, **kwargs):
        super().__init__(master, **kwargs)
        self.on_generate = on_generate
        self.create_widgets()
        self.pack(fill="both", expand=True)
    
    def create_widgets(self):
        # Create title
        create_title(self, "Process input.txt")

        # Button frame
        button_frame = ctk.CTkFrame(self)
        button_frame.pack(pady=10)

        # Buttons
        ctk.CTkButton(
            button_frame,
            text="Generate Processes",
            command=self.on_generate
        ).pack(side="left")

        # Now create your Treeview
        self.tree = ttk.Treeview(
            self,
            columns=("ID", "Arrival", "Burst", "Priority"),
            show="headings",
            style="Enhanced.Treeview"
        )


        self.tree.heading("ID", text="Process ID")
        self.tree.heading("Arrival", text="Arrival Time")
        self.tree.heading("Burst", text="Burst Time")
        self.tree.heading("Priority", text="Priority")
        self.tree.pack(fill="both", expand=True, padx=20, pady=10)

        configure_treeview_styles(self.tree)

    def update_process_table(self, arrival_times, burst_times, priorities):
        self.tree.delete(*self.tree.get_children())
        
        for i in range(len(arrival_times)):
            self.tree.insert(
                "",
                "end",
                values=(f"P{i+1}",
                        f"{arrival_times[i]:.2f}",
                        f"{burst_times[i]:.2f}",
                        f"{priorities[i]}")
            )



class ResultsTab(ctk.CTkFrame):
    def __init__(self, master, on_run: Callable, **kwargs):
        super().__init__(master, **kwargs)
        self.on_run = on_run
        self.algorithm_var = ctk.StringVar(value="FCFS")
        self.create_widgets()
        self.pack(fill="both", expand=True)
    
    def create_widgets(self):
        # Create title
        create_title(self, "Scheduling Results")

        # Button frame
        button_frame = ctk.CTkFrame(self)
        button_frame.pack(pady=10)

        # Button
        ctk.CTkButton(
            button_frame,
            text="Run Algorithm",
            command=self.on_run
        ).pack(side="left", padx=10)

        # Algorithm dropdown
        self.algorithm_menu = ctk.CTkOptionMenu(
            button_frame,
            values=ALGORITHMS,
            variable=self.algorithm_var
        )
        self.algorithm_menu.pack(side="left")
        
        # Results table
        self.tree = ttk.Treeview(
            self,
            columns=("ID", "Arrival", "Start", "End", "Turnaround"),
            show="headings",
            style="Enhanced.Treeview"
        )
        self.tree.heading("ID", text="Process ID")
        self.tree.heading("Arrival", text="Arrival Time")
        self.tree.heading("Start", text="Start Time")
        self.tree.heading("End", text="End Time")
        self.tree.heading("Turnaround", text="Turnaround Time")
        self.tree.pack(fill="both", expand=True, padx=20, pady=20)

        # Average times label
        self.avg_label = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=14))
        self.avg_label.pack(pady=10)

        configure_treeview_styles(self.tree)

    def display_results(self, results: List[Tuple[int, float, float, float, float]]):
        self.tree.delete(*self.tree.get_children())
        for pid, arrival, start, end, turnaround in results:
            self.tree.insert("", "end", 
                           values=(f"P{pid+1}", f"{arrival:.2f}", f"{start:.2f}", 
                                  f"{end:.2f}", f"{turnaround:.2f}"))

    def update_averages(self, avg_tat: float, avg_wt: float):
        self.avg_label.configure(
            text=f"Average Turnaround: {avg_tat:.2f} | Average Waiting: {avg_wt:.2f}"
        )

    def get_selected_algorithm(self) -> str:
        return self.algorithm_var.get()
    
    # def set_selected_algorithm(self, algorithm: str):
    #     self.algorithm_var.set(algorithm)


class VisualizationTab(ctk.CTkFrame):
    def __init__(self, master, algorith_var: ctk.StringVar, on_run: Callable, **kwargs):
        super().__init__(master, **kwargs)
        self.on_run = on_run
        self.algorithm_var = algorith_var
        self.create_widgets()
        self.pack(fill="both", expand=True)
    
    def create_widgets(self):
        # Create title
        create_title(self, "Process Execution Timeline")

        # Button frame
        button_frame = ctk.CTkFrame(self)
        button_frame.pack(pady=10)

        # Button
        ctk.CTkButton(
            button_frame,
            text="Run Algorithm",
            command=self.on_run
        ).pack(side="left", padx=10)

        # Algorithm dropdown
        self.algorithm_menu = ctk.CTkOptionMenu(
            button_frame,
            values=ALGORITHMS,
            variable=self.algorithm_var # i wanna use it here
        )
        self.algorithm_menu.pack(side="left")

        
        # Main Frame
        self.figure = plt.Figure(figsize=(10, 5))
        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def update_visualization(self, execution_order: List[Tuple[int, float, float]], title: str):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        
        y_pos = range(len(execution_order))
        process_labels = [f"P{pid+1}" for pid, _, _ in execution_order]
        start_times = [start for _, start, _ in execution_order]
        durations = [end-start for _, start, end in execution_order]
        
        ax.barh(y_pos, durations, left=start_times, height=0.5, align='center')
        ax.set_yticks(y_pos)
        ax.set_yticklabels(process_labels)
        ax.set_xlabel('Time')
        ax.set_title(title)
        ax.grid(True)
        
        self.canvas.draw()


class ComparisonTab(ctk.CTkFrame):
    def __init__(self, master, algorithms: Dict[str, Callable], **kwargs):
        super().__init__(master, **kwargs)
        self.algorithms = algorithms
        self.pack(fill="both", expand=True)
        self.create_widgets()
    
    def create_widgets(self):
        # Create title
        create_title(self, "Algorithm Comparison")

        # Main frame
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Results table
        self.results_table = ttk.Treeview(
            main_frame,
            columns=("algorithm", "avg_tat", "avg_wt", "throughput"),
            show="headings",
            height=5,
            style="Enhanced.Treeview"
        )
        
        # Table headers
        self.results_table.heading("algorithm", text="Algorithm")
        self.results_table.heading("avg_tat", text="Avg Turnaround")
        self.results_table.heading("avg_wt", text="Avg Waiting")
        self.results_table.heading("throughput", text="Throughput")
        
        # Column configuration
        self.results_table.column("algorithm", width=150, anchor="center")
        self.results_table.column("avg_tat", width=120, anchor="center")
        self.results_table.column("avg_wt", width=120, anchor="center")
        self.results_table.column("throughput", width=120, anchor="center")
        
        self.results_table.pack(fill="x", pady=(0, 20))
        
        # Chart
        self.figure = plt.Figure(figsize=(8, 4), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, master=main_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        
        # Run button
        self.run_btn = ctk.CTkButton(
            self,
            text="Run All Algorithms",
            command=self.run_comparison,
            width=200,
            height=40,
            font=ctk.CTkFont(size=14)
        )
        self.run_btn.pack(pady=10)
        
        configure_treeview_styles(self.results_table)
    
    def run_comparison(self):
        """Run all algorithms and display comparison results"""
        results = {}
        
        # Sample data - in real app this should come from main app
        arrival = [0, 2, 4, 6, 8]
        burst = [5, 3, 7, 2, 4]
        priority = [1, 3, 2, 4, 1]
        
        for name, algo_func in self.algorithms.items():
            if name == "Priority Scheduling":
                execution_order, avg_tat, avg_wt = algo_func(arrival, burst, priority)
            else:
                execution_order, avg_tat, avg_wt = algo_func(arrival, burst)
            
            # Calculate throughput (processes per time unit)
            total_time = execution_order[-1][2] - execution_order[0][1]
            throughput = len(arrival) / total_time if total_time > 0 else 0
            
            results[name] = {
                "avg_tat": avg_tat,
                "avg_wt": avg_wt,
                "throughput": throughput
            }
        
        self.update_results(results)
    
    def update_results(self, results: Dict[str, Dict[str, float]]):
        """Update the table and chart with new results"""
        # Clear old data
        for item in self.results_table.get_children():
            self.results_table.delete(item)
        
        # Add new results
        for algo, data in results.items():
            self.results_table.insert("", "end", values=(
                algo,
                f"{data['avg_tat']:.2f}",
                f"{data['avg_wt']:.2f}",
                f"{data['throughput']:.2f}"
            ))
        
        # Update chart
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        
        algorithms = list(results.keys())
        avg_tat = [data['avg_tat'] for data in results.values()]
        avg_wt = [data['avg_wt'] for data in results.values()]
        
        x = range(len(algorithms))
        width = 0.35
        
        ax.bar(x, avg_tat, width, label='Avg Turnaround', color='#1f6aa5')
        ax.bar([p + width for p in x], avg_wt, width, label='Avg Waiting', color='#2b8cbe')
        
        ax.set_xticks([p + width/2 for p in x])
        ax.set_xticklabels(algorithms)
        ax.set_title("Algorithm Performance Comparison")
        ax.legend()
        ax.grid(True, linestyle='--', alpha=0.6)
        
        self.canvas.draw()