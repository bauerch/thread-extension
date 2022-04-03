"""
Thread-control extensions.
"""
from threading import Event
from typing import Optional
from transitions import Machine, State


class ThreadControlMixin(Machine):
    """
    This class implements a state machine allowing thread objects to make use of
    additional control states to enable pause, resume and stop events at runtime.
    """
    INITIAL = State("initial")
    RUNNING = State("running")
    STOPPED = State("stopped")
    PAUSED = State("paused")

    def after_stopped_state(self) -> None:
        if not self._running.is_set():
            # Release lock by setting event flag
            self._running.set()
        self._running.clear()

    def before_running_state(self) -> None:
        self._running.set()

    def before_paused_state(self) -> None:
        self._running.clear()

    def wait(self, timeout: Optional[float] = None) -> bool:
        return self._running.wait(timeout=timeout)

    def __init__(self) -> None:
        self._running = Event()
        Machine.__init__(
            self,
            states=[
                self.INITIAL,
                self.RUNNING,
                self.STOPPED,
                self.PAUSED
            ],
            initial=self.INITIAL.name
        )
        self.add_transition(
            trigger="running",
            source=self.INITIAL.name,
            dest=self.RUNNING.name,
            before="before_running_state"
        )
        self.add_transition(
            trigger="pause",
            source=self.PAUSED.name,
            dest="="
        )
        self.add_transition(
            trigger="pause",
            source=self.RUNNING.name,
            dest=self.PAUSED.name,
            before="before_paused_state"
        )
        self.add_transition(
            trigger="resume",
            source=self.RUNNING.name,
            dest="="
        )
        self.add_transition(
            trigger="resume",
            source=self.PAUSED.name,
            dest=self.RUNNING.name,
            before="before_running_state"
        )
        self.add_transition(
            trigger="stop",
            source=self.STOPPED.name,
            dest="="
        )
        self.add_transition(
            trigger="stop",
            source=[self.RUNNING.name, self.PAUSED.name],
            dest=self.STOPPED.name,
            after="after_stopped_state"
        )
