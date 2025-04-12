"""UI components for the scheduler application."""
import customtkinter as ctk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from typing import Callable, List, Tuple, Optional, Dict, Any
import numpy as np
from utils import configure_treeview_styles, create_title

# Available scheduling algorithms
ALGORITHMS = ["FCFS", "Round Robin", "Preemptive SRTF", "Priority Scheduling"]

class InputTab(ctk.CTkFrame):
    """Tab for process input generation and display"""
    def __init__(self, master, on_generate: Callable, **kwargs):
        super().__init__(master, **kwargs)
        self.on_generate = on_generate  # Callback for generate button
        self.create_widgets()
        self.pack(fill="both", expand=True)
    
    def create_widgets(self):
        """Create all UI elements for the input tab"""
        create_title(self, "Process Input")

        # Button frame with generate button
        button_frame = ctk.CTkFrame(self)
        button_frame.pack(pady=10)

        ctk.CTkButton(
            button_frame,
            text="Generate Processes",
            command=self.on_generate
        ).pack(side="left")

        # Process display table
        self.tree = ttk.Treeview(
            self,
            columns=("ID", "Arrival", "Burst", "Priority"),
            show="headings",
            style="Enhanced.Treeview"
        )

        # Configure table columns
        self.tree.heading("ID", text="Process ID")
        self.tree.heading("Arrival", text="Arrival Time")
        self.tree.heading("Burst", text="Burst Time")
        self.tree.heading("Priority", text="Priority")
        self.tree.pack(fill="both", expand=True, padx=20, pady=10)

        configure_treeview_styles(self.tree)

    def update_process_table(self, arrival_times, burst_times, priorities):
        """Update the table with new process data"""
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
    """Tab for displaying scheduling results"""
    def __init__(self, master, on_run: Callable, **kwargs):
        super().__init__(master, **kwargs)
        self.on_run = on_run
        self.algorithm_var = ctk.StringVar(value="FCFS")  # Default algorithm
        self.create_widgets()
        self.pack(fill="both", expand=True)
    
    def create_widgets(self):
        """Create all UI elements for results tab"""
        create_title(self, "Scheduling Results")

        # Control frame with run button and algorithm selection
        button_frame = ctk.CTkFrame(self)
        button_frame.pack(pady=10)

        ctk.CTkButton(
            button_frame,
            text="Run Algorithm",
            command=self.on_run
        ).pack(side="left", padx=10)

        # Algorithm selection dropdown
        self.algorithm_menu = ctk.CTkOptionMenu(
            button_frame,
            values=ALGORITHMS,
            variable=self.algorithm_var
        )
        self.algorithm_menu.pack(side="left")
        
        # Results display table
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

        # Averages display label
        self.avg_label = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=14))
        self.avg_label.pack(pady=10)

        configure_treeview_styles(self.tree)

    def display_results(self, results: List[Tuple[int, float, float, float, float]]):
        """Display scheduling results in the table"""
        self.tree.delete(*self.tree.get_children())
        for pid, arrival, start, end, turnaround in results:
            self.tree.insert("", "end", 
                           values=(f"P{pid+1}", f"{arrival:.2f}", f"{start:.2f}", 
                                  f"{end:.2f}", f"{turnaround:.2f}"))

    def update_averages(self, avg_tat: float, avg_wt: float):
        """Update the averages display"""
        self.avg_label.configure(
            text=f"Average Turnaround: {avg_tat:.2f} | Average Waiting: {avg_wt:.2f}"
        )

    def get_selected_algorithm(self) -> str:
        """Get currently selected algorithm"""
        return self.algorithm_var.get()

class VisualizationTab(ctk.CTkFrame):
    """Tab for visualizing the scheduling timeline"""
    def __init__(self, master, algorith_var: ctk.StringVar, on_run: Callable, **kwargs):
        super().__init__(master, **kwargs)
        self.on_run = on_run
        self.algorithm_var = algorith_var
        self.create_widgets()
        self.pack(fill="both", expand=True)
    
    def create_widgets(self):
        """Create visualization tab UI"""
        create_title(self, "Process Execution Timeline")

        # Control frame
        button_frame = ctk.CTkFrame(self)
        button_frame.pack(pady=10)

        ctk.CTkButton(
            button_frame,
            text="Run Algorithm",
            command=self.on_run
        ).pack(side="left", padx=10)

        # Algorithm selection
        self.algorithm_menu = ctk.CTkOptionMenu(
            button_frame,
            values=ALGORITHMS,
            variable=self.algorithm_var
        )
        self.algorithm_menu.pack(side="left")

        # Matplotlib figure for Gantt chart
        self.figure = plt.Figure(figsize=(10, 5))
        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def update_visualization(self, execution_order: List[Tuple[int, float, float]], title: str):
        """Update the Gantt chart with new data"""
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        
        # Set dark theme colors
        self.figure.patch.set_facecolor('#2b2b2b')
        ax.set_facecolor('#2b2b2b')
        
        # Prepare data for plotting
        y_pos = range(len(execution_order))
        process_labels = [f"P{pid+1}" for pid, _, _ in execution_order]
        start_times = [start for _, start, _ in execution_order]
        durations = [end-start for _, start, end in execution_order]
        
        # Create horizontal bars
        bars = ax.barh(y_pos, durations, left=start_times, height=0.5, align='center', color='#1f77b4')
        ax.set_yticks(y_pos)
        ax.set_yticklabels(process_labels)
        ax.set_xlabel('Time', color='white')
        ax.set_ylabel('Processes', color='white')
        ax.set_title(title, color='white')
        
        # Style ticks and labels
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')
        
        # Add duration labels on bars
        for bar in bars:
            width = bar.get_width()
            ax.text(bar.get_x() + width, bar.get_y() + bar.get_height()/2,
                    f'{width:.1f}',
                    ha='left', va='center',
                    color='white',
                    fontsize=8)
        
        ax.grid(True, color='#3b3b3b')
        self.canvas.draw()

class ComparisonTab(ctk.CTkFrame):
    """Tab for comparing algorithm performance"""
    def __init__(self, master, algorithms: Dict[str, Callable], **kwargs):
        super().__init__(master, **kwargs)
        self.algorithms = algorithms
        self.arrival_times = []
        self.burst_times = []
        self.priorities = []
        self.create_widgets()
        self.pack(fill="both", expand=True)
    
    def create_widgets(self):
        """Create comparison tab UI"""
        create_title(self, "Algorithm Comparison")

        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Results comparison table
        self.results_table = ttk.Treeview(
            main_frame,
            columns=("algorithm", "avg_tat", "avg_wt", "throughput"),
            show="headings",
            height=5,
            style="Enhanced.Treeview"
        )
        
        # Configure table columns
        self.results_table.heading("algorithm", text="Algorithm")
        self.results_table.heading("avg_tat", text="Avg Turnaround")
        self.results_table.heading("avg_wt", text="Avg Waiting")
        self.results_table.heading("throughput", text="Throughput")
        
        self.results_table.column("algorithm", width=150, anchor="center")
        self.results_table.column("avg_tat", width=120, anchor="center")
        self.results_table.column("avg_wt", width=120, anchor="center")
        self.results_table.column("throughput", width=120, anchor="center")
        
        self.results_table.pack(fill="x", pady=(0, 20))
        
        # Comparison chart figure
        self.figure = plt.Figure(figsize=(8, 4), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, master=main_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        
        configure_treeview_styles(self.results_table)
    
    def update_data(self, arrival_times: List[float], burst_times: List[float], priorities: List[int]):
        """Update process data and run comparison"""
        self.arrival_times = arrival_times
        self.burst_times = burst_times
        self.priorities = priorities
        self.run_comparison()
    
    def run_comparison(self):
        """Run all algorithms and compare results"""
        if not self.arrival_times or len(self.arrival_times) == 0:
            return
            
        results = {}
        
        # Run each algorithm and store results
        for name, algo_func in self.algorithms.items():
            try:
                if name == "Priority Scheduling":
                    execution_order, avg_tat, avg_wt = algo_func(
                        self.arrival_times.copy(),
                        self.burst_times.copy(),
                        self.priorities.copy()
                    )
                else:
                    execution_order, avg_tat, avg_wt = algo_func(
                        self.arrival_times.copy(),
                        self.burst_times.copy()
                    )
                
                # Calculate throughput
                if execution_order:
                    total_time = max(end for _, _, end in execution_order) - min(self.arrival_times)
                    throughput = len(self.arrival_times) / total_time if total_time > 0 else 0
                else:
                    throughput = 0
                    
                results[name] = {
                    "avg_tat": round(avg_tat, 2),
                    "avg_wt": round(avg_wt, 2),
                    "throughput": round(throughput, 4)
                }
            except Exception as e:
                print(f"Error running {name}: {str(e)}")
                continue
        
        self.update_results(results)
    
    def update_results(self, results: Dict[str, Dict[str, float]]):
        """Update the comparison table and chart"""
        self.results_table.delete(*self.results_table.get_children())
        
        # Populate table with results
        for algo, data in results.items():
            self.results_table.insert("", "end", values=(
                algo,
                f"{data['avg_tat']:.2f}",
                f"{data['avg_wt']:.2f}",
                f"{data['throughput']:.4f}"
            ))
        
        # Update comparison chart
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        
        # Set dark theme
        self.figure.patch.set_facecolor('#2b2b2b')
        ax.set_facecolor('#2b2b2b')
        
        # Prepare data for bar chart
        algorithms = list(results.keys())
        avg_tat = [data['avg_tat'] for data in results.values()]
        avg_wt = [data['avg_wt'] for data in results.values()]
        
        x = range(len(algorithms))
        width = 0.35
        
        # Create bars
        tat_bars = ax.bar(x, avg_tat, width, label='Avg Turnaround', color='#1f77b4')
        wt_bars = ax.bar([p + width for p in x], avg_wt, width, label='Avg Waiting', color='#ff7f0e')
        
        # Configure chart
        ax.set_xticks([p + width/2 for p in x])
        ax.set_xticklabels(algorithms, ha='center', color='white')
        ax.set_ylabel('Time', color='white')
        ax.set_title("Algorithm Performance Comparison", color='white')
        
        ax.tick_params(axis='y', colors='white')
        
        # Add value labels on bars
        for bars, values in [(tat_bars, avg_tat), (wt_bars, avg_wt)]:
            for bar, value in zip(bars, values):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                        f'{value:.1f}',
                        ha='center', va='bottom',
                        color='white',
                        fontsize=10,
                        bbox=dict(facecolor='#3b3b3b', edgecolor='none', pad=1))
        
        # Configure legend
        legend = ax.legend(bbox_to_anchor=(1, 1))
        for text in legend.get_texts():
            text.set_color('white')
        
        ax.grid(True, linestyle='--', alpha=0.6, color='#3b3b3b')
        
        plt.tight_layout()
        self.canvas.draw() 