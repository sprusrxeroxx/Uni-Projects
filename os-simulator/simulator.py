from cpu_manager import CPUManager
from memory_manager import MemoryManager
from models import Job, ProcessState


class SystemSimulator:
    def __init__(self, total_memory: int = 330) -> None:
        self.jobs: list[Job] = []
        self.memory_manager = MemoryManager(total_memory)
        self.cpu_manager = CPUManager()
        self.event_log: list[str] = []

    def submit_job(self, job: Job) -> bool:
        if any(existing.job_id == job.job_id for existing in self.jobs):
            raise ValueError(f"Job '{job.job_id}' already exists.")

        self.jobs.append(job)

        block = self.memory_manager.allocate(job)
        if block is None:
            job.set_state(ProcessState.WAITING)
            self.log_event(
                f"{job.job_id} could not be allocated {job.memory_required}K; job is Waiting."
            )
            return False

        self.cpu_manager.add_job(job)
        self.log_event(
            f"{job.job_id} allocated {job.memory_required}K at "
            f"{block.start_address}K using {self.memory_manager.strategy.value}."
        )
        self.log_event(f"{job.job_id} added to FCFS ready queue.")
        return True

    def finish_job(self, job_id: str) -> bool:
        job = self.get_job(job_id)
        if job is None:
            return False

        released = self.memory_manager.deallocate(job)
        if not released:
            return False

        job.set_state(ProcessState.TERMINATED)
        self.cpu_manager.remove_job(job.job_id)

        self.log_event(
            f"{job.job_id} terminated and released {job.memory_required}K."
        )

        self._admit_waiting_jobs()
        return True

    def _admit_waiting_jobs(self) -> None:
        for job in self.jobs:
            if job.state != ProcessState.WAITING:
                continue

            block = self.memory_manager.allocate(job)
            if block is None:
                continue

            self.cpu_manager.add_job(job)
            self.log_event(
                f"{job.job_id} was Waiting and is now allocated "
                f"{job.memory_required}K at {block.start_address}K."
            )
            self.log_event(f"{job.job_id} added to FCFS ready queue.")

    def get_job(self, job_id: str) -> Job | None:
        return next((job for job in self.jobs if job.job_id == job_id), None)

    def log_event(self, message: str) -> None:
        self.event_log.append(message)

    def show_memory(self) -> None:
        print("\nMemory Map")
        print("-" * 40)
        for block in self.memory_manager.get_blocks():
            owner = block.job_id if block.job_id else "FREE"
            end = block.start_address + block.size
            print(f"{block.start_address:>3}K - {end:>3}K | {owner:<8} | {block.size}K")

    def show_jobs(self) -> None:
        print("\nJobs")
        print("-" * 60)
        for job in self.jobs:
            memory = f"{job.memory_start}K" if job.memory_start is not None else "-"
            print(
                f"{job.job_id:<8} {job.memory_required:>5}K "
                f"CPU={job.cpu_burst:<3} State={job.state.value:<10} Start={memory}"
            )

    def show_ready_queue(self) -> None:
        queue = self.cpu_manager.get_ready_queue()
        ids = " -> ".join(job.job_id for job in queue) or "EMPTY"
        print(f"\n{self.cpu_manager.strategy.value} Ready Queue: {ids}")

    def show_log(self) -> None:
        print("\nEvent Log")
        print("-" * 60)
        for event in self.event_log:
            print(event)
