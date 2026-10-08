from enum import Enum
from typing import Optional

from models import Job, MemoryBlock


class AllocationStrategy(Enum):
    FIRST_FIT = "First-Fit"
    BEST_FIT = "Best-Fit"


class MemoryManager:
    def __init__(
        self,
        total_memory: int,
        strategy: AllocationStrategy = AllocationStrategy.FIRST_FIT,
    ) -> None:
        if total_memory <= 0:
            raise ValueError("Total memory must be greater than 0.")

        self.total_memory = total_memory
        self.strategy = strategy
        self.blocks = [MemoryBlock(start_address=0, size=total_memory)]

    def set_strategy(self, strategy: AllocationStrategy) -> None:
        self.strategy = strategy

    def allocate(self, job: Job) -> Optional[MemoryBlock]:
        block = self._find_available_block(job.memory_required)

        if block is None:
            return None

        original_size = block.size
        block.allocate(job.job_id)
        job.set_memory_allocation(block.start_address)

        # Split the block when unused space remains.
        remaining = original_size - job.memory_required

        if remaining > 0:
            allocated = MemoryBlock(
                start_address=block.start_address,
                size=job.memory_required,
                job_id=job.job_id,
            )

            free_block = MemoryBlock(
                start_address=block.start_address + job.memory_required,
                size=remaining,
            )

            index = self.blocks.index(block)
            self.blocks[index:index + 1] = [
                allocated,
                free_block,
            ]

            block = allocated
        else:
            block.size = job.memory_required

        return block

    def deallocate(self, job: Job) -> bool:
        for block in self.blocks:
            if block.job_id == job.job_id:
                block.release()
                job.clear_memory_allocation()
                self._merge_adjacent_free_blocks()
                return True

        return False

    def get_blocks(self) -> list[MemoryBlock]:
        return list(self.blocks)

    def get_total_free_memory(self) -> int:
        return sum(
            block.size
            for block in self.blocks
            if block.is_free()
        )

    def get_largest_free_block(self) -> int:
        free_blocks = [
            block.size
            for block in self.blocks
            if block.is_free()
        ]

        return max(free_blocks, default=0)

    def is_external_fragmentation(self, required_size: int) -> bool:
        total_free = self.get_total_free_memory()
        largest_free = self.get_largest_free_block()

        return (
            total_free >= required_size
            and largest_free < required_size
        )

    def get_allocation_failure_reason(
        self,
        required_size: int,
    ) -> str:
        total_free = self.get_total_free_memory()
        largest_free = self.get_largest_free_block()

        if self.is_external_fragmentation(required_size):
            return (
                f"External fragmentation: {total_free}K is free "
                f"in total, but the largest contiguous block is "
                f"only {largest_free}K and {required_size}K is required."
            )

        return (
            f"Insufficient contiguous memory: largest free block "
            f"is {largest_free}K, but {required_size}K is required."
        )

    def _find_available_block(
        self,
        required_size: int,
    ) -> Optional[MemoryBlock]:

        if self.strategy == AllocationStrategy.FIRST_FIT:
            return self._first_fit(required_size)

        if self.strategy == AllocationStrategy.BEST_FIT:
            return self._best_fit(required_size)

        raise ValueError(
            f"Unsupported allocation strategy: {self.strategy}"
        )

    def _first_fit(
        self,
        required_size: int,
    ) -> Optional[MemoryBlock]:

        for block in self.blocks:
            if block.can_fit(required_size):
                return block

        return None

    def _best_fit(
        self,
        required_size: int,
    ) -> Optional[MemoryBlock]:

        suitable_blocks = [
            block
            for block in self.blocks
            if block.can_fit(required_size)
        ]

        if not suitable_blocks:
            return None

        return min(
            suitable_blocks,
            key=lambda block: block.size,
        )

    def _merge_adjacent_free_blocks(self) -> None:
        merged: list[MemoryBlock] = []

        for block in self.blocks:
            if (
                merged
                and merged[-1].is_free()
                and block.is_free()
                and merged[-1].start_address
                + merged[-1].size
                == block.start_address
            ):
                merged[-1].size += block.size
            else:
                merged.append(block)

        self.blocks = merged