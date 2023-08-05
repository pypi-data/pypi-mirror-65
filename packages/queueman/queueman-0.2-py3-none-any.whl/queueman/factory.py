"""QueueManager::factory"""

import logging
import asyncio

from queueman.exceptions import (
    QueueManagerExecutionStillInProgress,
    QueueManagerEmptyQueue,
)


class QueueManager:
    """The QueueManager class."""

    logger = logging.getLogger(__name__)

    running = False
    queue = []

    @property
    def pending_tasks(self):
        """Return a count of pending tasks in the queue."""
        return len(self.queue)

    def clear(self):
        """Clear the queue."""
        self.queue = []

    def add(self, task):
        """Add a task to the queue."""
        self.queue.append(task)

    async def execute(self, number_of_tasks=None):
        """Execute the tasks in the queue."""
        if self.running:
            print("Execution is allreay running")
            raise QueueManagerExecutionStillInProgress
        if len(self.queue) == 0:
            print("The queue is empty")
            raise QueueManagerEmptyQueue

        self.running = True

        print("Checking out tasks to execute")
        local_queue = []

        if number_of_tasks:
            for task in self.queue[:number_of_tasks]:
                local_queue.append(task)
        else:
            for task in self.queue:
                local_queue.append(task)

        for task in local_queue:
            self.queue.remove(task)

        print("Starting queue execution")
        await asyncio.gather(*local_queue)

        print("Queue execution finished")
        self.running = False
