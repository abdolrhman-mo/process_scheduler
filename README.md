# Process Scheduler

A CPU scheduling simulator with a graphical user interface that implements various scheduling algorithms.

<!-- ## Overview

This application simulates CPU scheduling algorithms to help understand how different scheduling policies affect process execution and system performance. It provides a visual representation of process execution and calculates key performance metrics. -->

## Features

- **Multiple Scheduling Algorithms**:
  - First Come First Serve (FCFS)
  - Round Robin (RR)
  - Preemptive Shortest Remaining Time First (SRTF)
  - Non-preemptive Priority Scheduling

- **Performance Metrics**:
  - Average Turnaround Time
  - Average Waiting Time
  <!-- - Process Execution Timeline -->

<!-- - **Process Generation**:
  - Manual process entry
  - Random process generation with configurable parameters -->

## Project Structure

```
process_scheduler/
├── main.py          # Application entry point
├── algorithms.py    # Scheduling algorithm implementations
├── models.py        # Data structures (Process class)
├── views.py         # GUI components
└── utils.py         # Helper functions
```

### Component Descriptions

#### main.py
- Entry point for the application
- Initializes the main window and starts the application loop

#### algorithms.py
- Contains implementations of all scheduling algorithms
- Each algorithm returns execution order and performance metrics

#### models.py
- Defines the `Process` class that represents a process in the system
- Stores process attributes (PID, arrival time, burst time, priority)

#### views.py
- Contains all GUI components using customtkinter
- `MainWindow`: Main application window
- `ProcessInputFrame`: Frame for process input parameters
- `ResultsFrame`: Frame for displaying scheduling results

#### utils.py
- Helper functions for process generation and metrics calculation
- `generate_random_processes()`: Creates random processes for testing
- `calculate_metrics()`: Computes average turnaround and waiting times

## How to Use

1. **Setup**:
   - Ensure Python 3.6+ is installed
   - Install required packages: `pip install customtkinter numpy matplotlib`

2. **Running the Application**:
   - Navigate to the project directory
   - Run: `python main.py`

3. **Using the GUI**:
   - Enter process details or generate random processes
   - Select a scheduling algorithm
   - Click "Run" to see the results
   - View results in results tab or output.txt file

<!-- ## Scheduling Algorithms

### First Come First Serve (FCFS)
- Processes are executed in the order they arrive
- Non-preemptive algorithm
- Simple but may lead to high waiting times for short processes

### Round Robin (RR)
- Each process gets a fixed time slice (quantum)
- Processes are executed in a circular queue
- Prevents starvation but may have high overhead

### Preemptive Shortest Remaining Time First (SRTF)
- Process with shortest remaining time gets CPU
- Preemptive version of Shortest Job First
- Minimizes average waiting time

### Non-preemptive Priority Scheduling
- Processes are executed based on priority
- Higher priority processes execute first
- May lead to starvation of low priority processes

## Performance Metrics

- **Turnaround Time**: Total time from arrival to completion
- **Waiting Time**: Time spent waiting in ready queue
- **Average Turnaround Time**: Sum of turnaround times / number of processes
- **Average Waiting Time**: Sum of waiting times / number of processes -->

## Development

To extend the application:
1. Add new algorithms to `algorithms.py`
2. Create new GUI components in `views.py`
3. Update the main window to include new features

## Team Contributions

### Mohamed
- Developed the complete GUI from start to finish
- Integrated and collected code from all team members
- Managed the overall project structure and implementation

### Nadine
- Implemented Round Robin (RR) algorithm
- Implemented Preemptive Shortest Remaining Time First (SRTF) algorithm
<!-- - Our main Engineer -->

### Melissia
- Implemented Non-preemptive Priority Scheduling algorithm

### Abdelrahman
<!-- - Developed input & output file handling -->
<!-- - Implemented random value generation for the basic table -->
- Implemented First Come First Serve (FCFS) algorithm

## Requirements

- Python 3.6+
- customtkinter
- numpy 
- matplotlib