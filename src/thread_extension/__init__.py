"""
Thread-based handler.
"""
from .version import __version__
from .control import ThreadControlMixin
from .handler import (
    CycleWorkerThread,
    TaskWorkerThread
)


__copyright__ = "Copyright (c) 2022 bauerch"
__license__ = "MIT"
__uri__ = "https://github.com/bauerch/thread-extension"
