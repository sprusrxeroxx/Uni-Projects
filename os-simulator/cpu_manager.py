from models import Job, ProcessState


class CPUManager:
    def __init__(self) -> None:
        self.strategy = "FCFS"
        self.ready_queue: list[Job] = []

    def add_job(self, job: Job) -> None:
        job.set_state(ProcessState.READY)
        self.ready_queue.append(job)

    def get_ready_queue(self) -> list[Job]:
        return list(self.ready_queue)