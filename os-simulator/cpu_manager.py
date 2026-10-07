from enum import Enum
from typing import Optional

from models import Job, ProcessState


class SchedulingStrategy(Enum):
    FCFS = "FCFS"


class CPUManager:
    def __init__(self, strategy: SchedulingStrategy = SchedulingStrategy.FCFS) -> None:
        self.strategy = strategy
        self.ready_queue: list[Job] = []
        self.gantt_timeline: list[tuple[str, int, int]] = []
        self.completed_jobs: list[Job] = []

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

    def run_fcfs(self) -> list[tuple[str, int, int]]:
        """Execute the current ready queue in FCFS order."""
        if self.strategy != SchedulingStrategy.FCFS:
            raise ValueError(f"Unsupported scheduling strategy: {self.strategy}")

        current_time = 0
        timeline: list[tuple[str, int, int]] = []
        jobs_to_run = list(self.ready_queue)
        self.completed_jobs = []

        for job in jobs_to_run:
            start_time = max(current_time, job.arrival_time)

            if start_time > current_time:
                timeline.append(("IDLE", current_time, start_time))

            completion_time = start_time + job.cpu_burst

            job.set_state(ProcessState.RUNNING)
            job.set_execution_times(start_time, completion_time)
            timeline.append((job.job_id, start_time, completion_time))
            job.set_state(ProcessState.TERMINATED)
            self.completed_jobs.append(job)

            current_time = completion_time

        self.ready_queue.clear()
        self.gantt_timeline = timeline
        return list(self.gantt_timeline)

    def get_gantt_timeline(self) -> list[tuple[str, int, int]]:
        return list(self.gantt_timeline)

    def get_average_waiting_time(self) -> float:
        if not self.completed_jobs:
            return 0.0
        return sum(job.waiting_time or 0 for job in self.completed_jobs) / len(self.completed_jobs)

    def get_average_turnaround_time(self) -> float:
        if not self.completed_jobs:
            return 0.0
        return sum(job.turnaround_time or 0 for job in self.completed_jobs) / len(self.completed_jobs)

    def _order_ready_queue(self) -> None:
        if self.strategy == SchedulingStrategy.FCFS:
            self.ready_queue.sort(key=lambda job: job.arrival_time)
            return

        raise ValueError(f"Unsupported scheduling strategy: {self.strategy}")
