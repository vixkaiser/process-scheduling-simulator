# Process Scheduling Simulator

This project is a CPU process scheduling simulator written in Python.  
It simulates different CPU scheduling algorithms, calculates their performance
metrics, and compares the results.

## Implemented Algorithms
- First Come First Serve (FCFS)
- Shortest Job First (SJF)
- Priority Scheduling
- Round Robin (Time Quantum = 3)
- Shortest Remaining Time First (SRTF)

## Requirements
- Python 3.x
- matplotlib
- rich

## How to Run
python process_scheduling_sim.py processes.txt 3

## Output
For each scheduling algorithm, the program outputs:
- A colored Gantt chart in the terminal
- A table showing finish time, turnaround time, and waiting time
- Average turnaround time, average waiting time, and CPU utilization

The program also generates the following PNG files in the same directory:
- avg_turnaround_time.png
- avg_waiting_time.png
- cpu_utilization.png

## Starvation Test
The starvation.txt file is included to demonstrate starvation behavior, particularly in priority-based scheduling.

## Author: Ece Bayyar