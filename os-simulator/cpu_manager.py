from enum import Enum
from typing import Optional

from models import Job, ProcessState


class SchedulingStrategy(Enum):
    FCFS = "FCFS"


class CPUManager:
    def __init__(self, strategy: SchedulingStrategy = SchedulingStrategy.FCFS) -> None:
        self.strategy = strategy
        self.ready_queue: list[Job] = []

    def add_job(self, job: Job) -> None:
        job.set_state(ProcessState.READY)
        self.ready_queue.append(job)
        self._order_ready_queue()

    def remove_job(self, job_id: str) -> bool:
        original_length = len(self.ready_queue)
        self.ready_queue = [
            job for job in self.ready_queue if job.job_id != job_id
        ]
        return len(self.ready_queue) != original_length

    def peek_next_job(self) -> Optional[Job]:
        if not self.ready_queue:
            return None
        return self.ready_queue[0]

    def get_ready_queue(self) -> list[Job]:
        return list(self.ready_queue)

    def _order_ready_queue(self) -> None:
        if self.strategy == SchedulingStrategy.FCFS:
            self.ready_queue.sort(key=lambda job: job.arrival_time)
            return

        raise ValueError(f"Unsupported scheduling strategy: {self.strategy}")
