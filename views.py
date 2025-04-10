# views.py
import customtkinter as ctk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from typing import Callable, List, Tuple, Optional

class InputTab(ctk.CTkFrame):
    def __init__(self, master, on_generate: Callable, on_run: Callable, **kwargs):
        super().__init__(master, **kwargs)
        self.on_generate = on_generate
        self.on_run = on_run
        self.algorithm_var = ctk.StringVar(value="FCFS")
        self.create_widgets()
        self.pack(fill="both", expand=True)  # Important for visibility
    
    def create_widgets(self):
        # Information label
        info_label = ctk.CTkLabel(
            self,
            text="Enter data in input.txt",
            font=ctk.CTkFont(size=14)
        )
        info_label.pack(pady=10)

        # Button frame
        button_frame = ctk.CTkFrame(self)
        button_frame.pack(pady=10)

        # Buttons
        ctk.CTkButton(
            button_frame,
            text="Generate Processes",
            command=self.on_generate
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            button_frame,
            text="Run Algorithm",
            command=self.on_run
        ).pack(side="left", padx=10)

        # Algorithm dropdown
        self.algorithm_menu = ctk.CTkOptionMenu(
            button_frame,
            values=["FCFS", "Round Robin", "Preemptive SRTF", "Priority Scheduling"],
            variable=self.algorithm_var
        )
        self.algorithm_menu.pack(side="left", padx=10)

        # Process table
        self.tree = ttk.Treeview(
            self,
            columns=("ID", "Arrival", "Burst", "Priority"),
            show="headings"
        )
        self.tree.heading("ID", text="Process ID")
        self.tree.heading("Arrival", text="Arrival Time")
        self.tree.heading("Burst", text="Burst Time")
        self.tree.heading("Priority", text="Priority")
        self.tree.pack(fill="both", expand=True, padx=20, pady=10)

        # Configure styles
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview",
                      background="#2b2b2b",
                      foreground="white",
                      fieldbackground="#2b2b2b",
                      rowheight=25,
                      font=('Segoe UI', 12))
        style.configure("Treeview.Heading",
                      background="#1f1f1f",
                      foreground="white",
                      font=('Segoe UI', 13, 'bold'))

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

    def get_selected_algorithm(self) -> str:
        return self.algorithm_var.get()


class ResultsTab(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.create_widgets()
        self.pack(fill="both", expand=True)
    
    def create_widgets(self):
        # Results table
        self.tree = ttk.Treeview(
            self,
            columns=("ID", "Arrival", "Start", "End", "Turnaround"),
            show="headings"
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

        # Configure styles
        style = ttk.Style()
        style.configure("Treeview",
                      background="#2b2b2b",
                      foreground="white",
                      fieldbackground="#2b2b2b",
                      rowheight=25,
                      font=('Segoe UI', 12))
        style.configure("Treeview.Heading",
                      background="#1f1f1f",
                      foreground="white",
                      font=('Segoe UI', 13, 'bold'))

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


class VisualizationTab(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.create_widgets()
        self.pack(fill="both", expand=True)
    
    def create_widgets(self):
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