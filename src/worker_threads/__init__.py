"""
Thread-based handler.
"""
from src.worker_threads.version import __version__
from src.worker_threads.control import ThreadControlMixin
from src.worker_threads.core import (
    CycleWorkerThread,
    TaskWorkerThread
)


__copyright__ = "Copyright (c) 2022 bauerch"
__license__ = "MIT"
__uri__ = "https://github.com/bauerch/thread-extension"
