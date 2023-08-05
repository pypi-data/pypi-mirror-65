"""QueueManager::exceptions"""


class QueueManagerBaseException(Exception):
    """Base exception for QueueManager."""


class QueueManagerEmptyQueue(QueueManagerBaseException):
    """Exception to raise if the queue is empty."""


class QueueManagerExecutionStillInProgress(QueueManagerBaseException):
    """Exception to raise if execution is still in progress."""
