from simulator import SystemSimulator
from models import Job
from cpu_manager import SchedulingStrategy
from memory_manager import AllocationStrategy


def main() -> None:
    simulator = SystemSimulator(total_memory=330)

    while True:
        print("\n=== UMP OS Simulator - Phase 6 ===")
        print(f"Memory Strategy: {simulator.memory_manager.strategy.value}")
        print(f"CPU Strategy: {simulator.cpu_manager.strategy.value}")
        print("1. Add job")
        print("2. Finish job")
        print("3. Run CPU")
        print("4. Show memory")
        print("5. Show jobs")
        print("6. Show FCFS ready queue")
        print("7. Show Gantt timeline")
        print("8. Show event log")
        print("9. Set memory allocation strategy")
        print("10. Set CPU scheduling strategy")
        print("11. Request printer")
        print("12. Release printer")
        print("13. Show device status")
        print("0. Exit")

        choice = input("Choose an option: ").strip()

        try:
            if choice == "1":
                job_id = input("Job ID: ").strip()
                memory = int(input("Memory required (K): "))
                burst = int(input("CPU burst: "))
                arrival = int(input("Arrival time: "))

                job = Job(job_id, memory, burst, arrival)
                allocated = simulator.submit_job(job)

                if allocated:
                    print(f"{job.job_id} accepted and allocated memory.")
                else:
                    print(f"{job.job_id} could not be allocated and is Waiting.")

            elif choice == "2":
                job_id = input("Job ID to finish: ").strip()
                if simulator.finish_job(job_id):
                    print(f"{job_id} finished and memory was released.")
                else:
                    print(f"Could not finish '{job_id}'.")

            elif choice == "3":
                timeline = simulator.run_cpu()
                if timeline:
                    print(f"{simulator.cpu_manager.strategy.value} execution complete.")
                else:
                    print("Ready queue is empty.")

            elif choice == "4":
                simulator.show_memory()

            elif choice == "5":
                simulator.show_jobs()

            elif choice == "6":
                simulator.show_ready_queue()

            elif choice == "7":
                simulator.show_gantt()

            elif choice == "8":
                simulator.show_log()

            elif choice == "9":
                print("\n1. First-Fit")
                print("2. Best-Fit")
                strategy_choice = input("Choose strategy: ").strip()

                if strategy_choice == "1":
                    simulator.memory_manager.set_strategy(AllocationStrategy.FIRST_FIT)
                    print("Memory allocation strategy set to First-Fit.")
                elif strategy_choice == "2":
                    simulator.memory_manager.set_strategy(AllocationStrategy.BEST_FIT)
                    print("Memory allocation strategy set to Best-Fit.")
                else:
                    print("Invalid strategy.")

            elif choice == "10":
                print("\n1. FCFS")
                print("2. Round Robin")
                strategy_choice = input("Choose strategy: ").strip()

                if strategy_choice == "1":
                    simulator.cpu_manager.set_strategy(SchedulingStrategy.FCFS)
                    print("CPU scheduling strategy set to FCFS.")
                elif strategy_choice == "2":
                    simulator.cpu_manager.set_strategy(SchedulingStrategy.ROUND_ROBIN)
                    quantum = int(input("Time quantum: "))
                    if quantum <= 0:
                        raise ValueError("Time quantum must be greater than 0.")
                    simulator.cpu_manager.time_quantum = quantum
                    print(f"CPU scheduling strategy set to Round Robin (quantum={quantum}).")
                else:
                    print("Invalid strategy.")

            elif choice == "11":
                job_id = input("Job ID requesting printer: ").strip()
                if simulator.request_printer(job_id):
                    print(f"{job_id} received the printer.")
                else:
                    job = simulator.get_job(job_id)
                    if job is None:
                        print(f"Job '{job_id}' was not found.")
                    elif simulator.device_manager.get_current_job() is job:
                        print(f"{job_id} already has the printer.")
                    else:
                        print(f"{job_id} is waiting for the printer.")

            elif choice == "12":
                if simulator.release_printer():
                    print("Printer released.")
                else:
                    print("Printer is already free.")

            elif choice == "13":
                simulator.show_device()

            elif choice == "0":
                print("Goodbye.")
                break

            else:
                print("Invalid option.")

        except ValueError as error:
            print(f"Error: {error}")


if __name__ == "__main__":
    main()
