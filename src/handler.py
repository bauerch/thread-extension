"""
Thread based handlers.
"""
import abc
import queue
import time
from threading import Thread, Event
from typing import (
    Any,
    Callable,
    Optional
)
from src.control import ThreadControlMixin


class CycleWorkerThread(Thread, ThreadControlMixin):
    """
    This class represents a special thread type, which executes a predefined
    routine cyclically until a stop event is triggered.
    """
    def __init__(
            self,
            delay: float = 0.0,
            timeout: float = 1000.0,
            target: Optional[Callable] = None,
            args: tuple = (),
            kwargs=None,
            daemon: Optional[bool] = False
    ) -> None:
        """
        Initializes CycleWorkerThread class.
        """
        Thread.__init__(self, daemon=daemon)
        ThreadControlMixin.__init__(self)
        self._timeout = timeout
        self._delay = delay
        self._target = target
        self._args = args
        self._kwargs = kwargs if kwargs is not None else {}
        self._task_done = Event()
        self._task_done.set()

    def __repr__(self) -> str:
        string = super().__repr__()
        if self.is_alive():
            string = string[:-2] + f", {repr(self.status)})>"
        return string

    def run(self) -> None:
        """
        Defines the worker's concrete workflow.
        """
        self.set_start_state()
        try:
            self.preparation()
            while not self.is_stopped():
                if not self.wait(self._timeout):
                    self.stop()  # Force stoppage
                    break
                self._task_done.clear()
                try:
                    self.work_routine()
                finally:
                    self._task_done.set()
                time.sleep(self._delay)
            self.post_processing()
        finally:
            self.set_end_state()
            # Avoid a refcycle if the thread is running a function with
            # an argument that has a member that points to the thread.
            del self._target, self._args, self._kwargs

    def work_routine(self) -> None:
        """
        Representing the worker's activity on each cycle.

        You may override this method in a subclass. The work_routine() method
        invokes the callable object passed to the object's constructor as the
        target argument, if any, with sequential and keyword arguments taken
        from the args and kwargs arguments, respectively.
        """
        if self._target:
            self._target(*self._args, **self._kwargs)
        else:
            self.stop()

    def is_working(self):
        return not self._task_done.is_set()

    @property
    def delay(self) -> float:
        """
        Indicates how much time shall pass before the worker continues with
        the next work cycle.
        """
        return self._delay

    @delay.setter
    def delay(self, delay: float) -> None:
        if delay < 0.0:
            raise ValueError("Delay must be non-negative")
        self._delay = delay

    @property
    def timeout(self) -> float:
        """
        Indicates how much time the worker is allowed to pause before
        the worker is automatically forced to stop.
        """
        return self._timeout

    @timeout.setter
    def timeout(self, timeout: float) -> None:
        if timeout < 0.0:
            raise ValueError("Timeout must be non-negative")
        self._timeout = timeout

    def preparation(self) -> None:
        """
        Optional preparatory steps for the worker to perform before starting.
        """

    def post_processing(self) -> None:
        """
        Optional follow-up steps for the worker to perform after stoppage.
        """


class TaskWorkerThread(Thread, ThreadControlMixin):
    """
    This class represents a special thread type, which processes a stack of
    similar tasks one after the other.
    """
    def __init__(
            self,
            tasks: queue.Queue,
            delay: float = 0.0,
            timeout: float = 1000.0,
            daemon: Optional[bool] = False
    ) -> None:
        """
        Initializes TaskWorkerThread class.
        """
        Thread.__init__(self, daemon=daemon)
        ThreadControlMixin.__init__(self)
        self._timeout = timeout
        self._delay = delay
        self._queue = tasks
        self._task_done = Event()
        self._task_done.set()

    def __repr__(self) -> str:
        string = super().__repr__()
        if self.is_alive():
            string = string[:-2] + f", {repr(self.status)})>"
        return string

    def run(self) -> None:
        """
        Defines the worker's concrete workflow.
        """
        self.set_start_state()
        try:
            self.preparation()
            while not self.is_stopped():
                if self._queue.empty() or not \
                        self.wait(self._timeout):
                    self.stop()  # Force stoppage
                    break
                self._task_done.clear()
                try:
                    task = self._queue.get()
                    self.work_on_task(task)
                except queue.Empty:
                    self.stop()
                else:
                    self._queue.task_done()
                finally:
                    self._task_done.set()
                time.sleep(self._delay)
            self.post_processing()
        finally:
            self.set_end_state()

    @abc.abstractmethod
    def work_on_task(self, task: Any) -> None:
        """
        Abstract method representing the worker's activity on all task.
        """

    def is_working(self):
        return not self._task_done.is_set()

    @property
    def delay(self) -> float:
        """
        Indicates how much time shall pass before the worker continues with
        the next work cycle.
        """
        return self._delay

    @delay.setter
    def delay(self, delay: float) -> None:
        if delay < 0.0:
            raise ValueError("Delay must be non-negative")
        self._delay = delay

    @property
    def timeout(self) -> float:
        """
        Indicates how much time the worker is allowed to pause before
        the worker is automatically forced to stop.
        """
        return self._timeout

    @timeout.setter
    def timeout(self, timeout: float) -> None:
        if timeout < 0.0:
            raise ValueError("Timeout must be non-negative")
        self._timeout = timeout

    def preparation(self) -> None:
        """
        Optional preparatory steps for the worker to perform before starting.
        """

    def post_processing(self) -> None:
        """
        Optional follow-up steps for the worker to perform after stoppage.
        """
