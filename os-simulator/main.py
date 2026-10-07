from simulator import SystemSimulator
from models import Job


def main() -> None:
    simulator = SystemSimulator(330)

    while True:
        print("\n=== UMP OS Simulator ===")
        print("1. Add job")
        print("2. Finish job")
        print("3. Show memory")
        print("4. Show jobs")
        print("0. Exit")

        choice = input("Choose an option: ").strip()

        try:
            if choice == "1":
                job_id = input("Job ID: ").strip()
                memory = int(input("Memory required (K): "))
                burst = int(input("CPU burst: "))
                arrival = int(input("Arrival time: "))

                job = Job(job_id, memory, burst, arrival)

                if simulator.submit_job(job):
                    print("Job accepted.")
                else:
                    print("Job could not be allocated and is Waiting.")

            elif choice == "2":
                job_id = input("Job ID to finish: ").strip()

                if simulator.finish_job(job_id):
                    print("Job finished and memory released.")
                else:
                    print("Job not found or has no allocation.")

            elif choice == "3":
                for block in simulator.memory_manager.get_blocks():
                    owner = block.job_id or "FREE"

                    print(
                        f"{block.start_address}K - "
                        f"{block.start_address + block.size}K : "
                        f"{owner}"
                    )

            elif choice == "4":
                for job in simulator.jobs:
                    print(
                        job.job_id,
                        job.memory_required,
                        job.cpu_burst,
                        job.state.value
                    )

            elif choice == "0":
                break

            else:
                print("Invalid option.")

        except ValueError as error:
            print(f"Error: {error}")


if __name__ == "__main__":
    main()