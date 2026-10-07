from dataclasses import dataclass
from enum import Enum
from typing import Optional


class ProcessState(Enum):
    NEW = "New"
    READY = "Ready"
    RUNNING = "Running"
    WAITING = "Waiting"
    TERMINATED = "Terminated"


@dataclass
class Job:
    job_id: str
    memory_required: int
    cpu_burst: int
    arrival_time: int = 0
    state: ProcessState = ProcessState.NEW
    memory_start: Optional[int] = None

    def __post_init__(self) -> None:
        if not self.job_id.strip():
            raise ValueError("Job ID cannot be blank.")
        if self.memory_required <= 0:
            raise ValueError("Memory required must be greater than 0.")
        if self.cpu_burst <= 0:
            raise ValueError("CPU burst must be greater than 0.")
        if self.arrival_time < 0:
            raise ValueError("Arrival time cannot be negative.")

    def set_state(self, state: ProcessState) -> None:
        self.state = state

    def set_memory_allocation(self, start_address: int) -> None:
        self.memory_start = start_address

    def clear_memory_allocation(self) -> None:
        self.memory_start = None


@dataclass
class MemoryBlock:
    start_address: int
    size: int
    job_id: Optional[str] = None

    def is_free(self) -> bool:
        return self.job_id is None

    def can_fit(self, size: int) -> bool:
        return self.is_free() and self.size >= size

    def allocate(self, job_id: str) -> None:
        if not self.is_free():
            raise ValueError("Memory block is already allocated.")
        self.job_id = job_id

    def release(self) -> None:
        self.job_id = None