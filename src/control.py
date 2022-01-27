# pylint: disable=missing-function-docstring
"""
Thread-control extensions.
"""
from threading import Event
from typing import Optional


class ThreadControlMixin:
    """
    This class extends a thread of control by providing events to pause and
    stop a thread at runtime.
    """
    def __init__(self) -> None:
        self.__started = Event()
        self.__stopped = Event()
        self.__running = Event()

    def __repr__(self) -> str:
        status = "running" if self.is_running() else "paused"
        if not self.__started.is_set():
            status = "initial"
        if self.is_stopped():
            status = "stopped"
        return status

    def is_running(self) -> bool:
        return self.__running.is_set()

    def is_stopped(self) -> bool:
        return self.__stopped.is_set()

    def pause(self) -> None:
        if not self.__started.is_set():
            raise RuntimeError("Cannot pause thread before it is started")
        if self.is_stopped():
            raise RuntimeError("Cannot pause thread after it is stopped")
        self.__running.clear()

    def resume(self) -> None:
        if not self.__started.is_set():
            raise RuntimeError("Cannot resume thread before it is started")
        if self.is_stopped():
            raise RuntimeError("Cannot resume thread after it is stopped")
        self.__running.set()

    def stop(self) -> None:
        if not self.__started.is_set():
            raise RuntimeError("Cannot stop thread before it is started")
        if self.is_stopped():
            raise RuntimeError("thread can only be stopped once")
        self.__stopped.set()
        if not self.is_running():
            # Release lock by setting event flag
            self.__running.set()

    def wait(self, timeout: Optional[float] = None) -> bool:
        if not self.__started.is_set():
            raise RuntimeError("Cannot wait thread before it is started")
        if self.is_stopped():
            raise RuntimeError("Cannot wait thread after it is stopped")
        return self.__running.wait(timeout=timeout)

    def set_start_state(self) -> None:
        if self.__started.is_set():
            raise RuntimeError("thread can only be started once")
        self.__started.set()
        self.__running.set()

    def set_end_state(self) -> None:
        if self.is_stopped():
            self.__running.clear()
