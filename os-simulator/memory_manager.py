from typing import Optional

from models import Job, MemoryBlock


class MemoryManager:
    def __init__(self, total_memory: int) -> None:
        if total_memory <= 0:
            raise ValueError("Total memory must be greater than 0.")

        self.total_memory = total_memory
        self.blocks = [MemoryBlock(0, total_memory)]

    def allocate(self, job: Job) -> Optional[MemoryBlock]:
        # Temporary rule for Phase 1:
        # use the first suitable free block.
        block = self._find_available_block(job.memory_required)

        if block is None:
            return None

        original_size = block.size

        block.allocate(job.job_id)
        job.set_memory_allocation(block.start_address)

        remaining = original_size - job.memory_required

        if remaining > 0:
            allocated = MemoryBlock(
                block.start_address,
                job.memory_required,
                job.job_id
            )

            free_block = MemoryBlock(
                block.start_address + job.memory_required,
                remaining
            )

            index = self.blocks.index(block)
            self.blocks[index:index + 1] = [allocated, free_block]

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

    def _find_available_block(
        self,
        required_size: int
    ) -> Optional[MemoryBlock]:

        for block in self.blocks:
            if block.can_fit(required_size):
                return block

        return None

    def _merge_adjacent_free_blocks(self) -> None:
        merged = []

        for block in self.blocks:
            if (
                merged
                and merged[-1].is_free()
                and block.is_free()
                and merged[-1].start_address + merged[-1].size
                == block.start_address
            ):
                merged[-1].size += block.size
            else:
                merged.append(block)

        self.blocks = merged