"""
GUI components for the Process Scheduler.
Contains all the visual elements and user interface components.
"""

import customtkinter as ctk
from models import Process

class MainWindow:
    """
    Main window of the application.
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Process Scheduler")
        self.root.geometry("800x600")
        
        # Configure the grid
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        
        # Create main frame
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        # Initialize UI components
        self._init_ui()

    def _init_ui(self):
        """Initialize all UI components"""
        # Add your UI components here
        pass

class ProcessInputFrame(ctk.CTkFrame):
    """
    Frame for process input parameters.
    """
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self._init_ui()

    def _init_ui(self):
        """Initialize UI components for process input"""
        pass

class ResultsFrame(ctk.CTkFrame):
    """
    Frame for displaying scheduling results.
    """
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self._init_ui()

    def _init_ui(self):
        """Initialize UI components for results display"""
        pass 