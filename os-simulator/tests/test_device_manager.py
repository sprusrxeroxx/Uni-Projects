import unittest

from device_manager import DeviceManager, DeviceStatus
from models import Job, ProcessState
from simulator import SystemSimulator


class TestDeviceManager(unittest.TestCase):
    def test_printer_starts_free(self):
        manager = DeviceManager()
        self.assertEqual(manager.get_status(), DeviceStatus.FREE)
        self.assertIsNone(manager.get_current_job())

    def test_first_job_gets_printer(self):
        manager = DeviceManager()
        job = Job("J1", 20, 5)

        self.assertTrue(manager.request_device(job))
        self.assertEqual(manager.get_status(), DeviceStatus.BUSY)
        self.assertEqual(manager.get_current_job(), job)

    def test_later_jobs_enter_waiting_queue(self):
        manager = DeviceManager()
        j1 = Job("J1", 20, 5)
        j2 = Job("J2", 20, 5)

        manager.request_device(j1)
        self.assertFalse(manager.request_device(j2))
        self.assertEqual(manager.get_waiting_queue(), [j2])
        self.assertEqual(manager.get_current_job(), j1)

    def test_release_assigns_printer_to_next_job(self):
        manager = DeviceManager()
        j1 = Job("J1", 20, 5)
        j2 = Job("J2", 20, 5)

        manager.request_device(j1)
        manager.request_device(j2)
        released, next_job = manager.release_device()

        self.assertEqual(released, j1)
        self.assertEqual(next_job, j2)
        self.assertEqual(manager.get_current_job(), j2)
        self.assertEqual(manager.get_waiting_queue(), [])

    def test_release_when_queue_empty_makes_printer_free(self):
        manager = DeviceManager()
        j1 = Job("J1", 20, 5)
        manager.request_device(j1)

        released, next_job = manager.release_device()

        self.assertEqual(released, j1)
        self.assertIsNone(next_job)
        self.assertEqual(manager.get_status(), DeviceStatus.FREE)


class TestSimulatorDeviceIntegration(unittest.TestCase):
    def test_busy_printer_moves_job_to_waiting_and_release_reactivates_it(self):
        simulator = SystemSimulator(total_memory=100)
        j1 = Job("J1", 20, 5)
        j2 = Job("J2", 20, 5, arrival_time=1)
        simulator.submit_job(j1)
        simulator.submit_job(j2)

        self.assertTrue(simulator.request_printer("J1"))
        self.assertEqual(j1.state, ProcessState.WAITING)
        self.assertNotIn(j1, simulator.cpu_manager.get_ready_queue())

        self.assertFalse(simulator.request_printer("J2"))
        self.assertEqual(j2.state, ProcessState.WAITING)
        self.assertNotIn(j2, simulator.cpu_manager.get_ready_queue())

        self.assertTrue(simulator.release_printer())
        self.assertEqual(j1.state, ProcessState.READY)
        self.assertEqual(j2.state, ProcessState.WAITING)
        self.assertEqual(simulator.device_manager.get_current_job(), j2)
        self.assertEqual(
            [job.job_id for job in simulator.cpu_manager.get_ready_queue()],
            ["J1"],
        )

        self.assertTrue(simulator.release_printer())
        self.assertEqual(j2.state, ProcessState.READY)
        self.assertEqual(simulator.device_manager.get_status(), DeviceStatus.FREE)
        self.assertEqual(
            [job.job_id for job in simulator.cpu_manager.get_ready_queue()],
            ["J1", "J2"],
        )

    def test_request_unknown_job_fails(self):
        simulator = SystemSimulator(total_memory=100)
        self.assertFalse(simulator.request_printer("J99"))

    def test_current_printer_owner_cannot_request_again(self):
        simulator = SystemSimulator(total_memory=100)
        job = Job("J1", 20, 5)
        simulator.submit_job(job)
        self.assertTrue(simulator.request_printer("J1"))
        self.assertFalse(simulator.request_printer("J1"))
        self.assertEqual(simulator.device_manager.get_current_job(), job)


if __name__ == "__main__":
    unittest.main()
