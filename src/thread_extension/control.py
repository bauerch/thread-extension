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
    _INITIAL = State("initial")
    _RUNNING = State("running")
    _STOPPED = State("stopped")
    _PAUSED = State("paused")

    def __init__(self) -> None:
        self._running = Event()
        Machine.__init__(
            self,
            states=[
                self._INITIAL,
                self._RUNNING,
                self._STOPPED,
                self._PAUSED
            ],
            initial=self._INITIAL.name
        )
        self.add_transition(
            trigger="running",
            source=self._INITIAL.name,
            dest=self._RUNNING.name,
            before="_before_running_state"
        )
        self.add_transition(
            trigger="pause",
            source=self._PAUSED.name,
            dest="="
        )
        self.add_transition(
            trigger="pause",
            source=self._RUNNING.name,
            dest=self._PAUSED.name,
            before="_before_paused_state"
        )
        self.add_transition(
            trigger="resume",
            source=self._RUNNING.name,
            dest="="
        )
        self.add_transition(
            trigger="resume",
            source=self._PAUSED.name,
            dest=self._RUNNING.name,
            before="_before_running_state"
        )
        self.add_transition(
            trigger="stop",
            source=self._STOPPED.name,
            dest="="
        )
        self.add_transition(
            trigger="stop",
            source=[self._RUNNING.name, self._PAUSED.name],
            dest=self._STOPPED.name,
            after="_after_stopped_state"
        )

    def wait(self, timeout: Optional[float] = None) -> bool:
        return self._running.wait(timeout=timeout)

    def _after_stopped_state(self) -> None:
        if not self._running.is_set():
            # Release lock by setting event flag
            self._running.set()
        self._running.clear()

    def _before_running_state(self) -> None:
        self._running.set()

    def _before_paused_state(self) -> None:
        self._running.clear()
