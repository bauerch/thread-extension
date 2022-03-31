"""
Thread based tracker.
"""
import glob
import os
import queue
import time
from typing import Set
from src.thread_extension.handler import CycleWorkerThread


class NewFileTracker(CycleWorkerThread):
    """
    This class checks periodically if new files of the given type are created
    in the given folder. As soon as new files are detected, they are put into
    `new_files` for further processing by other threads.
    """
    def __init__(
            self,
            folder: str,
            f_type: str = "*",
            scan_interval: float = 0.0
    ) -> None:
        """
        Initializes the file tracker.
        """
        super().__init__(delay=scan_interval, daemon=True)
        self.__f_queue = queue.Queue()  # type: queue.Queue
        self.__ignored = set()          # type: Set[str]
        self.__pattern = os.path.join(folder, f_type)
        self.__start_time = time.time()

    @property
    def new_files(self) -> queue.Queue:
        """
        Returns all newly detected files.

        Returns
        -------
        queue.Queue
            Object containing all new files found.
        """
        return self.__f_queue

    def preparation(self) -> None:
        """
        Called once at the beginning. Takes a snapshot of the current folder
        content, as a reference to distinguish new from old files.
        """
        self.__ignored = {file for file in glob.glob(self.__pattern) if
                          os.path.getctime(file) < self.__start_time}

    def work_routine(self) -> None:
        """
        Called periodically as soon as `scan_interval` has expired. Checks if
        new files of the given type are created.
        """
        files = set(glob.glob(self.__pattern))
        for file in files.difference(self.__ignored):
            self.__f_queue.put(file)
        self.__ignored = files
