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
                f"{job.job_id} could not be allocated; job is Waiting."
            )

            return False

        self.cpu_manager.add_job(job)

        self.log_event(
            f"{job.job_id} allocated "
            f"{job.memory_required}K at {block.start_address}K."
        )

        self.log_event(
            f"{job.job_id} added to FCFS ready queue."
        )

        return True

    def finish_job(self, job_id: str) -> bool:
        job = self.get_job(job_id)

        if job is None:
            return False

        released = self.memory_manager.deallocate(job)

        if not released:
            return False

        job.set_state(ProcessState.TERMINATED)

        self.cpu_manager.ready_queue = [
            queued_job
            for queued_job in self.cpu_manager.ready_queue
            if queued_job.job_id != job.job_id
        ]

        self.log_event(
            f"{job.job_id} terminated and released "
            f"{job.memory_required}K."
        )

        return True

    def get_job(self, job_id: str) -> Job | None:
        return next(
            (job for job in self.jobs if job.job_id == job_id),
            None
        )

    def log_event(self, message: str) -> None:
        self.event_log.append(message)