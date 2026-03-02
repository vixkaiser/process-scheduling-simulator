import sys
import copy
from rich.console import Console
from rich.table import Table
from rich.text import Text
import matplotlib.pyplot as plt

console = Console()

class Process:
    def __init__(self, pid, arrival_time, burst_time, priority):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time # For Round Robin
        self.priority = priority
        self.finish_time = None
        self.turnaround_time = None
        self.waiting_time = None

def read_input_file(filename):
    processes = []

    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if line == "":
                continue

            parts = line.split(',')

            pid = parts[0].strip()
            arrival_time = int(parts[1].strip())
            burst_time = int(parts[2].strip())
            priority = int(parts[3].strip())

            processes.append(Process(pid, arrival_time, burst_time, priority))

    return processes


# FCFS - First Come First Serve Scheduling
def fcfs(processes):
    current_time = 0
    idle_time = 0
    gantt = []

    processes.sort(key=lambda p: p.arrival_time)

    for p in processes:
        if current_time < p.arrival_time:
            gantt.append(("Idle", current_time, p.arrival_time))
            idle_time += p.arrival_time - current_time
            current_time = p.arrival_time
        
        start_time = current_time
        current_time += p.burst_time

        gantt.append((p.pid, start_time, current_time))

        p.finish_time = current_time
        p.turnaround_time = p.finish_time - p.arrival_time
        p.waiting_time = p.turnaround_time - p.burst_time

    return idle_time, current_time, gantt


# SJF - Shortest Job First Scheduling
def sjf(processes):
    current_time = 0
    idle_time = 0
    completed = 0
    n = len(processes)
    gantt = []

    for p in processes:
        p.finish_time = None

    while completed < n:
        ready_queue = [p for p in processes 
                       if p.arrival_time <= current_time and p.finish_time is None]
        
        if not ready_queue:
            gantt.append(("Idle", current_time, current_time + 1))
            idle_time += 1
            current_time += 1
            continue

        current_process = min(
            ready_queue, 
            key=lambda p: (p.burst_time, p.arrival_time)
        )

        start_time = current_time
        current_time += current_process.burst_time
        end_time = current_time

        gantt.append((current_process.pid, start_time, end_time))

        current_process.finish_time = end_time
        current_process.turnaround_time = end_time - current_process.arrival_time
        current_process.waiting_time = current_process.turnaround_time - current_process.burst_time

        completed += 1
    
    return idle_time, current_time, gantt


# Priority Scheduling
def priority_scheduling(processes):
    current_time = 0
    idle_time = 0
    completed = 0
    n = len(processes)
    gantt = []

    for p in processes:
        p.finish_time = None

    while completed < n:
        ready_queue = [p for p in processes 
                       if p.arrival_time <= current_time and p.finish_time is None]
        
        if not ready_queue:
            gantt.append(("Idle", current_time, current_time + 1))
            idle_time += 1
            current_time += 1
            continue

        current_process = min(
            ready_queue, 
            key=lambda p: (p.priority, p.arrival_time)
        )

        start_time = current_time
        current_time += current_process.burst_time
        end_time = current_time

        gantt.append((current_process.pid, start_time, end_time))

        current_process.finish_time = end_time
        current_process.turnaround_time = end_time - current_process.arrival_time
        current_process.waiting_time = current_process.turnaround_time - current_process.burst_time

        completed += 1
    
    return idle_time, current_time, gantt


# Round Robin Scheduling
def round_robin(processes, time_quantum):
    current_time = 0
    idle_time = 0
    completed = 0
    n = len(processes)
    gantt = []

    for p in processes:
        p.remaining_time = p.burst_time
        p.finish_time = None

    ready_queue = []
    added = set()

    while completed < n:
        for p in processes:
            if p.arrival_time <= current_time and p.pid not in added and p.remaining_time > 0:
                ready_queue.append(p)
                added.add(p.pid)

        if not ready_queue:
            gantt.append(("Idle", current_time, current_time + 1))
            idle_time += 1
            current_time += 1
            continue

        current_process = ready_queue.pop(0)

        run_time = min(time_quantum, current_process.remaining_time)

        start_time = current_time
        current_process.remaining_time -= run_time
        current_time += run_time

        gantt.append((current_process.pid, start_time, current_time))

        for p in processes:
            if p.arrival_time <= current_time and p.pid not in added and p.remaining_time > 0:
                ready_queue.append(p)
                added.add(p.pid)
        
        if current_process.remaining_time == 0:
            current_process.finish_time = current_time
            current_process.turnaround_time = current_process.finish_time - current_process.arrival_time
            current_process.waiting_time = current_process.turnaround_time - current_process.burst_time
            completed += 1
        else:
            ready_queue.append(current_process)

    return idle_time, current_time, gantt


# SRTF - Shortest Remaining Time First Scheduling
def srtf(processes):
    current_time = 0
    idle_time = 0
    completed = 0
    n = len(processes)
    gantt = []

    for p in processes:
        p.remaining_time = p.burst_time
        p.finish_time = None

    last_process = None
    start_time = None

    while completed < n:
        ready_queue = [p for p in processes 
                       if p.arrival_time <= current_time and p.remaining_time > 0]
        
        if not ready_queue:
            gantt.append(("Idle", current_time, current_time + 1))
            idle_time += 1
            current_time += 1
            continue

        current_process = min(
            ready_queue, 
            key=lambda p: (p.remaining_time, p.arrival_time)
        )

        if last_process != current_process:
            if last_process is not None:
                gantt.append((last_process.pid, start_time, current_time))
            start_time = current_time
            last_process = current_process

        current_process.remaining_time -= 1
        current_time += 1

        if current_process.remaining_time == 0:
            current_process.finish_time = current_time
            current_process.turnaround_time = current_process.finish_time - current_process.arrival_time
            current_process.waiting_time = current_process.turnaround_time - current_process.burst_time
            completed += 1

    if last_process is not None:
        gantt.append((last_process.pid, start_time, current_time))

    return idle_time, current_time, gantt


def print_results(name, processes, gantt, idle_time, total_time):
    console.rule(f"[bold cyan]{name}")

    console.print("[bold]Gantt Chart:[/bold]", end=" ")
    console.print("[0]", end="")
    for pid, start, end in gantt:
        color = "red" if pid == "Idle" else "green"
        console.print(f"--{pid}--[{end}]", style=color, end="")
    console.print()

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Process")
    table.add_column("Finish Time")
    table.add_column("Turnaround Time")
    table.add_column("Waiting Time")

    total_ta = total_wt = 0

    for p in processes:
        table.add_row(
            p.pid,
            str(p.finish_time),
            str(p.turnaround_time),
            str(p.waiting_time)
        )
        total_ta += p.turnaround_time
        total_wt += p.waiting_time

    console.print(table)

    avg_ta = total_ta / len(processes)
    avg_wt = total_wt / len(processes)
    cpu_util = ((total_time - idle_time) / total_time) * 100

    console.print(f"[bold yellow]Average Turnaround Time:[/bold yellow] {avg_ta:.2f}")
    console.print(f"[bold yellow]Average Waiting Time:[/bold yellow] {avg_wt:.2f}")
    console.print(f"[bold yellow]CPU Utilization:[/bold yellow] {cpu_util:.2f}%")


def save_results(results, name, processes, idle_time, total_time):
    total_ta = sum(p.turnaround_time for p in processes)
    total_wt = sum(p.waiting_time for p in processes)

    results[name] = {
        "avg_ta": total_ta / len(processes),
        "avg_wt": total_wt / len(processes),
        "cpu": ((total_time - idle_time) / total_time) * 100
    }


def generate_pngs(results):
    names = list(results.keys())

    plt.figure()
    plt.bar(names, [results[n]["avg_ta"] for n in names])
    plt.ylabel("Average Turnaround Time")
    plt.title("Average Turnaround Time Comparison")
    plt.savefig("avg_turnaround_time.png")
    plt.close()

    plt.figure()
    plt.bar(names, [results[n]["avg_wt"] for n in names])
    plt.ylabel("Average Waiting Time")
    plt.title("Average Waiting Time Comparison")
    plt.savefig("avg_waiting_time.png")
    plt.close()

    plt.figure()
    plt.bar(names, [results[n]["cpu"] for n in names])
    plt.ylabel("CPU Utilization (%)")
    plt.title("CPU Utilization Comparison")
    plt.savefig("cpu_utilization.png")
    plt.close()


if __name__ == "__main__":
    input_file = sys.argv[1]
    base_processes = read_input_file(input_file)

    results = {}

    processes = copy.deepcopy(base_processes)
    idle, total, gantt = fcfs(processes)
    print_results("FCFS", processes, gantt, idle, total)
    save_results(results, "FCFS", processes, idle, total)

    processes = copy.deepcopy(base_processes)
    idle, total, gantt = sjf(processes)
    print_results("SJF", processes, gantt, idle, total)
    save_results(results, "SJF", processes, idle, total)

    processes = copy.deepcopy(base_processes)
    idle, total, gantt = priority_scheduling(processes)
    print_results("Priority", processes, gantt, idle, total)
    save_results(results, "Priority", processes, idle, total)

    if len(sys.argv) >= 3:
        tq = int(sys.argv[2])
        processes = copy.deepcopy(base_processes)
        idle, total, gantt = round_robin(processes, tq)
        print_results(f"RR (TQ={tq})", processes, gantt, idle, total)
        save_results(results, "RR", processes, idle, total)

    processes = copy.deepcopy(base_processes)
    idle, total, gantt = srtf(processes)
    print_results("SRTF", processes, gantt, idle, total)
    save_results(results, "SRTF", processes, idle, total)

    generate_pngs(results)