"""
Main application entry point for the Process Scheduler.
This file handles the application initialization and main loop.
"""

import customtkinter as ctk
from views import MainWindow
from models import Process
from algorithms import (
    first_come_first_serve,
    round_robin,
    preemptive_srtf,
    non_preemptive_priority
)

def main():
    # Initialize the main window
    root = ctk.CTk()
    app = MainWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main() 