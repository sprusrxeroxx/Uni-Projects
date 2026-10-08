import unittest

from models import Job, ProcessState
from cpu_manager import SchedulingStrategy
from simulator import SystemSimulator


class TestSystemSimulator(unittest.TestCase):
    def test_waiting_job_is_admitted_after_memory_is_freed(self):
        simulator = SystemSimulator(total_memory=100)

        j1 = Job("J1", 60, 5, arrival_time=0)
        j2 = Job("J2", 30, 5, arrival_time=1)
        j3 = Job("J3", 20, 5, arrival_time=2)

        self.assertTrue(simulator.submit_job(j1))
        self.assertTrue(simulator.submit_job(j2))
        self.assertFalse(simulator.submit_job(j3))
        self.assertEqual(j3.state, ProcessState.WAITING)

        self.assertTrue(simulator.finish_job("J2"))

        self.assertEqual(j3.state, ProcessState.READY)
        self.assertIsNotNone(j3.memory_start)
        self.assertEqual(j3.memory_start, 60)
        self.assertEqual(
            [job.job_id for job in simulator.cpu_manager.get_ready_queue()],
            ["J1", "J3"],
        )

    def test_waiting_job_remains_waiting_when_no_block_is_large_enough(self):
        simulator = SystemSimulator(total_memory=100)

        j1 = Job("J1", 40, 5)
        j2 = Job("J2", 40, 5)
        j3 = Job("J3", 50, 5)

        simulator.submit_job(j1)
        simulator.submit_job(j2)
        self.assertFalse(simulator.submit_job(j3))

        simulator.finish_job("J1")

        self.assertEqual(j3.state, ProcessState.WAITING)

    def test_run_cpu_executes_ready_jobs_and_releases_memory(self):
        simulator = SystemSimulator(total_memory=100)

        j1 = Job("J1", 40, 7, arrival_time=0)
        j2 = Job("J2", 30, 4, arrival_time=1)
        j3 = Job("J3", 20, 3, arrival_time=2)

        simulator.submit_job(j1)
        simulator.submit_job(j2)
        simulator.submit_job(j3)

        timeline = simulator.run_cpu()

        self.assertEqual(
            timeline,
            [("J1", 0, 7), ("J2", 7, 11), ("J3", 11, 14)],
        )
        self.assertTrue(all(job.state == ProcessState.TERMINATED for job in [j1, j2, j3]))
        self.assertEqual(len(simulator.memory_manager.get_blocks()), 1)
        self.assertTrue(simulator.memory_manager.get_blocks()[0].is_free())
        self.assertEqual(simulator.memory_manager.get_blocks()[0].size, 100)

    def test_run_cpu_uses_selected_round_robin_strategy(self):
        simulator = SystemSimulator(total_memory=100)
        simulator.cpu_manager.set_strategy(SchedulingStrategy.ROUND_ROBIN)
        simulator.cpu_manager.time_quantum = 2

        j1 = Job("J1", 30, 5, arrival_time=0)
        j2 = Job("J2", 30, 3, arrival_time=0)
        simulator.submit_job(j1)
        simulator.submit_job(j2)

        timeline = simulator.run_cpu()

        self.assertEqual(
            timeline,
            [("J1", 0, 2), ("J2", 2, 4), ("J1", 4, 6), ("J2", 6, 7), ("J1", 7, 8)],
        )
        self.assertTrue(all(job.state == ProcessState.TERMINATED for job in [j1, j2]))


if __name__ == "__main__":
    unittest.main()
