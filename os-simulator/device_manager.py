from collections import deque
from enum import Enum
from typing import Optional

from models import Job


class DeviceStatus(Enum):
    FREE = "Free"
    BUSY = "Busy"


class DeviceManager:
    """Manages one simulated printer and its waiting queue."""

    def __init__(self) -> None:
        self.device_name = "Printer"
        self.status = DeviceStatus.FREE
        self.current_job: Optional[Job] = None
        self.waiting_queue: deque[Job] = deque()

    def request_device(self, job: Job) -> bool:
        """Give the printer to the job, or queue it if the printer is busy."""
        if self.current_job is None:
            self.current_job = job
            self.status = DeviceStatus.BUSY
            return True

        if all(queued.job_id != job.job_id for queued in self.waiting_queue) and (
            self.current_job.job_id != job.job_id
        ):
            self.waiting_queue.append(job)

        return False

    def release_device(self) -> tuple[Optional[Job], Optional[Job]]:
        """Release the current job and assign the printer to the next queued job."""
        released_job = self.current_job

        if self.waiting_queue:
            next_job = self.waiting_queue.popleft()
            self.current_job = next_job
            self.status = DeviceStatus.BUSY
            return released_job, next_job

        self.current_job = None
        self.status = DeviceStatus.FREE
        return released_job, None

    def get_status(self) -> DeviceStatus:
        return self.status

    def get_current_job(self) -> Optional[Job]:
        return self.current_job

    def get_waiting_queue(self) -> list[Job]:
        return list(self.waiting_queue)