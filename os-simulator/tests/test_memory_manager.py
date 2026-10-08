import unittest

from memory_manager import AllocationStrategy, MemoryManager
from models import Job


class TestMemoryManager(unittest.TestCase):
    def test_default_strategy_is_first_fit(self):
        manager = MemoryManager(330)
        self.assertEqual(manager.strategy, AllocationStrategy.FIRST_FIT)

    def test_first_fit_selects_first_suitable_hole(self):
        manager = MemoryManager(330)
        jobs = [
            Job("J1", 100, 1),
            Job("J2", 50, 1),
            Job("J3", 70, 1),
            Job("J4", 30, 1),
        ]
        for job in jobs:
            manager.allocate(job)

        manager.deallocate(jobs[0])
        manager.deallocate(jobs[2])

        j5 = Job("J5", 60, 1)
        manager.allocate(j5)

        self.assertEqual(j5.memory_start, 0)

    def test_best_fit_selects_smallest_suitable_hole(self):
        manager = MemoryManager(330, AllocationStrategy.BEST_FIT)
        jobs = [
            Job("J1", 100, 1),
            Job("J2", 50, 1),
            Job("J3", 70, 1),
            Job("J4", 30, 1),
        ]
        for job in jobs:
            manager.allocate(job)

        manager.deallocate(jobs[0])
        manager.deallocate(jobs[2])

        j5 = Job("J5", 60, 1)
        manager.allocate(j5)

        self.assertEqual(j5.memory_start, 150)

    def test_deallocation_still_merges_adjacent_free_blocks(self):
        manager = MemoryManager(170)
        j1 = Job("J1", 75, 1)
        manager.allocate(j1)
        manager.deallocate(j1)

        blocks = manager.get_blocks()
        self.assertEqual(len(blocks), 1)
        self.assertTrue(blocks[0].is_free())
        self.assertEqual(blocks[0].size, 170)


    def test_detects_external_fragmentation(self):
        manager = MemoryManager(200)
        j1 = Job("J1", 50, 1)
        j2 = Job("J2", 100, 1)
        j3 = Job("J3", 50, 1)

        manager.allocate(j1)
        manager.allocate(j2)
        manager.allocate(j3)
        manager.deallocate(j1)
        manager.deallocate(j3)

        self.assertEqual(manager.get_total_free_memory(), 100)
        self.assertEqual(manager.get_largest_free_block(), 50)
        self.assertTrue(manager.is_external_fragmentation(80))

    def test_not_external_fragmentation_when_contiguous_block_is_large_enough(self):
        manager = MemoryManager(200)
        j1 = Job("J1", 50, 1)
        manager.allocate(j1)

        self.assertFalse(manager.is_external_fragmentation(100))
        self.assertEqual(manager.get_largest_free_block(), 150)

    def test_strategy_can_be_changed(self):
        manager = MemoryManager(330)
        manager.set_strategy(AllocationStrategy.BEST_FIT)
        self.assertEqual(manager.strategy, AllocationStrategy.BEST_FIT)


if __name__ == "__main__":
    unittest.main()
