import unittest

from cpu_manager import CPUManager, SchedulingStrategy
from models import Job, ProcessState


class TestCPUManager(unittest.TestCase):
    def test_default_strategy_is_fcfs(self):
        manager = CPUManager()
        self.assertEqual(manager.strategy, SchedulingStrategy.FCFS)

    def test_add_job_moves_job_to_ready(self):
        manager = CPUManager()
        job = Job("J1", 20, 5)

        manager.add_job(job)

        self.assertEqual(job.state, ProcessState.READY)
        self.assertEqual(manager.get_ready_queue(), [job])

    def test_fcfs_orders_by_arrival_time(self):
        manager = CPUManager()
        j2 = Job("J2", 20, 5, arrival_time=2)
        j1 = Job("J1", 20, 5, arrival_time=1)

        manager.add_job(j2)
        manager.add_job(j1)

        self.assertEqual(
            [job.job_id for job in manager.get_ready_queue()],
            ["J1", "J2"],
        )

    def test_peek_returns_next_fcfs_job_without_removing_it(self):
        manager = CPUManager()
        j1 = Job("J1", 20, 5, arrival_time=0)
        j2 = Job("J2", 20, 5, arrival_time=1)

        manager.add_job(j1)
        manager.add_job(j2)

        self.assertEqual(manager.peek_next_job(), j1)
        self.assertEqual(len(manager.get_ready_queue()), 2)

    def test_remove_job(self):
        manager = CPUManager()
        j1 = Job("J1", 20, 5)
        manager.add_job(j1)

        self.assertTrue(manager.remove_job("J1"))
        self.assertEqual(manager.get_ready_queue(), [])

    def test_fcfs_execution_and_metrics(self):
        manager = CPUManager()
        jobs = [
            Job("P1", 20, 7, arrival_time=0),
            Job("P2", 20, 4, arrival_time=1),
            Job("P3", 20, 9, arrival_time=2),
            Job("P4", 20, 5, arrival_time=4),
        ]

        for job in jobs:
            manager.add_job(job)

        timeline = manager.run_fcfs()

        self.assertEqual(
            timeline,
            [
                ("P1", 0, 7),
                ("P2", 7, 11),
                ("P3", 11, 20),
                ("P4", 20, 25),
            ],
        )
        self.assertEqual(jobs[0].waiting_time, 0)
        self.assertEqual(jobs[1].waiting_time, 6)
        self.assertEqual(jobs[2].waiting_time, 9)
        self.assertEqual(jobs[3].waiting_time, 16)
        self.assertEqual(jobs[0].turnaround_time, 7)
        self.assertEqual(jobs[1].turnaround_time, 10)
        self.assertEqual(jobs[2].turnaround_time, 18)
        self.assertEqual(jobs[3].turnaround_time, 21)
        self.assertAlmostEqual(manager.get_average_waiting_time(), 7.75)
        self.assertAlmostEqual(manager.get_average_turnaround_time(), 14.0)
        self.assertEqual(manager.get_ready_queue(), [])
        self.assertTrue(all(job.state == ProcessState.TERMINATED for job in jobs))

    def test_fcfs_adds_idle_time_when_first_job_arrives_late(self):
        manager = CPUManager()
        job = Job("J1", 20, 2, arrival_time=3)
        manager.add_job(job)

        self.assertEqual(manager.run_fcfs(), [("IDLE", 0, 3), ("J1", 3, 5)])
        self.assertEqual(job.waiting_time, 0)
        self.assertEqual(job.turnaround_time, 2)

    def test_strategy_can_be_changed_to_round_robin(self):
        manager = CPUManager()
        manager.set_strategy(SchedulingStrategy.ROUND_ROBIN)
        self.assertEqual(manager.strategy, SchedulingStrategy.ROUND_ROBIN)

    def test_round_robin_execution_and_metrics(self):
        manager = CPUManager(strategy=SchedulingStrategy.ROUND_ROBIN)
        manager.time_quantum = 3
        jobs = [
            Job("P1", 20, 7, arrival_time=0),
            Job("P2", 20, 4, arrival_time=1),
            Job("P3", 20, 9, arrival_time=2),
            Job("P4", 20, 5, arrival_time=4),
        ]

        for job in jobs:
            manager.add_job(job)

        timeline = manager.run_round_robin()

        self.assertEqual(
            timeline,
            [
                ("P1", 0, 3),
                ("P2", 3, 6),
                ("P3", 6, 9),
                ("P1", 9, 12),
                ("P4", 12, 15),
                ("P2", 15, 16),
                ("P3", 16, 19),
                ("P1", 19, 20),
                ("P4", 20, 22),
                ("P3", 22, 25),
            ],
        )
        self.assertEqual(jobs[0].waiting_time, 13)
        self.assertEqual(jobs[1].waiting_time, 11)
        self.assertEqual(jobs[2].waiting_time, 14)
        self.assertEqual(jobs[3].waiting_time, 13)
        self.assertEqual(jobs[0].turnaround_time, 20)
        self.assertEqual(jobs[1].turnaround_time, 15)
        self.assertEqual(jobs[2].turnaround_time, 23)
        self.assertEqual(jobs[3].turnaround_time, 18)
        self.assertAlmostEqual(manager.get_average_waiting_time(), 12.75)
        self.assertAlmostEqual(manager.get_average_turnaround_time(), 19.0)
        self.assertEqual(manager.get_ready_queue(), [])
        self.assertTrue(all(job.state == ProcessState.TERMINATED for job in jobs))

    def test_round_robin_handles_cpu_idle_time(self):
        manager = CPUManager(strategy=SchedulingStrategy.ROUND_ROBIN)
        manager.time_quantum = 2
        job = Job("J1", 20, 3, arrival_time=3)
        manager.add_job(job)

        self.assertEqual(
            manager.run_round_robin(),
            [("IDLE", 0, 3), ("J1", 3, 5), ("J1", 5, 6)],
        )
        self.assertEqual(job.waiting_time, 0)
        self.assertEqual(job.turnaround_time, 3)

    def test_round_robin_rejects_invalid_time_quantum(self):
        manager = CPUManager(strategy=SchedulingStrategy.ROUND_ROBIN)
        manager.time_quantum = 0
        manager.add_job(Job("J1", 20, 3))

        with self.assertRaises(ValueError):
            manager.run_round_robin()


if __name__ == "__main__":
    unittest.main()
