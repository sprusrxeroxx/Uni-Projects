import shlex
import os
import subprocess
import socket

from simulator import SystemSimulator
from models import Job
from cpu_manager import SchedulingStrategy
from memory_manager import AllocationStrategy

hostname = socket.gethostname()
PROMPT = f"{hostname}@sim_os:$ "

def print_banner() -> None:
    print(r"""             _.-;;-._
      '-..-'|   ||   |
      '-..-'|_.-;;-._|
      '-..-'|   ||   |
      '-..-'|_.-''-._|        
      
      welcome to SIM OS
""")

def print_definitions() -> None:
    print(r"""  Definitions:

    Fragmentation: When a job is allocated memory, it may leave small gaps of free memory that are too small to be used by other jobs.
    
    First-Fit: An allocation strategy where the memory manager will allocate the first block of memory that is large enough to fit the job.
    
    Best-Fit: An allocation strategy where the memory manager will allocate the smallest block of memory that is large enough.
    
    Scheduling: The process of deciding which job in the ready queue will be executed next by the CPU.

    Deallocation: The process of releasing memory that was previously allocated to a job.

    Process States: The different states a process can be in during its lifetime, such as running, waiting, or terminated.
""")
def print_help() -> None:
    print("""
Available commands:

  add <id> <memory> <burst> <arrival>   Add a job
  end <id>                              Finish a job
  run                                   Run the CPU

  show jobs                             Show all jobs
  show memory                           Show memory map
  show ready                            Show ready queue
  show gantt                            Show Gantt timeline
  show log                              Show event log
  show devices                          Show printer status

  set memory ff                         Use First-Fit
  set memory bf                         Use Best-Fit
  set cpu fcfs                          Use FCFS
  set cpu rr <quantum>                  Use Round Robin

  request printer <id>                 Request the printer
  release printer                      Release the printer

  help                                  Show this help
  exit                                  Exit the simulator
  clear                                 Clear the screen
  definitions                           Show definitions
""")


def handle_command(simulator: SystemSimulator, parts: list[str]) -> bool:
    if not parts:
        return True

    command = parts[0].lower()

    if command == "help":
        print_help()
        return True
    
    if command == "definitions":
        print_definitions()
        return True
    
    if command == "clear":
        command = "cls" if os.name == "nt" else "clear"
        subprocess.run(command, shell=True)
        return True

    if command == "exit":
        print("Goodbye.")
        return False

    if command == "add":
        if len(parts) != 5:
            print("Usage: add <id> <memory> <burst> <arrival>")
            return True

        job_id = parts[1]
        memory = int(parts[2])
        burst = int(parts[3])
        arrival = int(parts[4])

        job = Job(job_id, memory, burst, arrival)
        allocated = simulator.submit_job(job)

        if allocated:
            print(f"{job.job_id} accepted and allocated memory.")
        else:
            print(f"{job.job_id} could not be allocated and is Waiting.")
            print(
                simulator.memory_manager.get_allocation_failure_reason(
                    job.memory_required
                )
            )

        return True

    if command == "end":
        if len(parts) != 2:
            print("Usage: end <id>")
            return True

        job_id = parts[1]
        if simulator.finish_job(job_id):
            print(f"{job_id} finished and memory was released.")
        else:
            print(f"Could not finish '{job_id}'.")

        return True

    if command == "run":
        if len(parts) != 1:
            print("Usage: run")
            return True

        timeline = simulator.run_cpu()
        if timeline:
            print(f"{simulator.cpu_manager.strategy.value} execution complete.")
        else:
            print("Ready queue is empty.")

        return True

    if command == "show":
        if len(parts) != 2:
            print("Usage: show <jobs|memory|ready|gantt|log|devices>")
            return True

        view = parts[1].lower()

        if view == "jobs":
            simulator.show_jobs()
        elif view == "memory":
            simulator.show_memory()
        elif view == "ready":
            simulator.show_ready_queue()
        elif view == "gantt":
            simulator.show_gantt()
        elif view == "log":
            simulator.show_log()
        elif view == "devices":
            simulator.show_device()
        else:
            print(f"Unknown view: {view}")

        return True

    if command == "set":
        if len(parts) < 3:
            print("Usage: set <memory|cpu> <strategy> [quantum]")
            return True

        target = parts[1].lower()
        strategy = parts[2].lower()

        if target == "memory":
            if len(parts) != 3:
                print("Usage: set memory <ff|bf>")
                return True

            if strategy == "ff":
                simulator.memory_manager.set_strategy(AllocationStrategy.FIRST_FIT)
                print("Memory allocation strategy set to First-Fit.")
            elif strategy == "bf":
                simulator.memory_manager.set_strategy(AllocationStrategy.BEST_FIT)
                print("Memory allocation strategy set to Best-Fit.")
            else:
                print("Unknown memory strategy. Use first-fit or best-fit.")

            return True

        if target == "cpu":
            if strategy == "fcfs" and len(parts) == 3:
                simulator.cpu_manager.set_strategy(SchedulingStrategy.FCFS)
                print("CPU scheduling strategy set to FCFS.")
                return True

            if strategy == "rr" and len(parts) == 4:
                quantum = int(parts[3])
                if quantum <= 0:
                    raise ValueError("Time quantum must be greater than 0.")

                simulator.cpu_manager.set_strategy(SchedulingStrategy.ROUND_ROBIN)
                simulator.cpu_manager.time_quantum = quantum
                print(
                    f"CPU scheduling strategy set to Round Robin "
                    f"(quantum={quantum})."
                )
                return True

            print("Usage: set cpu <fcfs|rr> [quantum]")
            return True

        print(f"Unknown setting: {target}")
        return True

    if command == "request":
        if len(parts) != 3 or parts[1].lower() != "printer":
            print("Usage: request <device> <id>")
            return True

        job_id = parts[2]
        if simulator.request_printer(job_id):
            print(f"{job_id} received the printer.")
        else:
            job = simulator.get_job(job_id)
            if job is None:
                print(f"Job '{job_id}' was not found.")
            else:
                print(f"{job_id} is waiting for the printer.")

        return True

    if command == "release":
        if len(parts) != 2 or parts[1].lower() != "printer":
            print("Usage: release <device>")
            return True

        if simulator.release_printer():
            print("Printer released.")
        else:
            print("Printer is already free.")

        return True

    print(f"Unknown command: {parts[0]}")
    print("Type 'help' to see available commands.")
    return True


def main() -> None:
    simulator = SystemSimulator(total_memory=330)
    print_banner()
    print("Type 'help' to see available commands.")

    while True:
        try:
            command = input(PROMPT).strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye.")
            break

        try:
            parts = shlex.split(command)
            if not handle_command(simulator, parts):
                break
        except ValueError as error:
            print(f"Error: {error}")


if __name__ == "__main__":
    main()
