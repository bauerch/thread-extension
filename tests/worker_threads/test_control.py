import unittest
from timeit import default_timer as timer
from transitions.core import MachineError
from src.worker_threads.control import ThreadControlMixin


class ThreadControlMixinClass(unittest.TestCase):
    """
    This class represents a wrapper class for all unittests related to the
    ThreadControlMixin class within <src.worker_threads.control>.
    """
    def setUp(self):
        self._mixin = ThreadControlMixin()

    def tearDown(self):
        del self._mixin

    def test_standard_state_transitions(self):
        """
        This test checks the correct transition into all possible states.
        """
        self.assertEqual(self._mixin.state, "initial")
        self.assertFalse(self._mixin._running.is_set())
        self._mixin.running()
        self.assertEqual(self._mixin.state, "running")
        self.assertTrue(self._mixin._running.is_set())
        self._mixin.pause()
        self.assertEqual(self._mixin.state, "paused")
        self.assertFalse(self._mixin._running.is_set())
        self._mixin.pause()
        self.assertEqual(self._mixin.state, "paused")
        self.assertFalse(self._mixin._running.is_set())
        self._mixin.resume()
        self.assertEqual(self._mixin.state, "running")
        self.assertTrue(self._mixin._running.is_set())
        self._mixin.resume()
        self.assertEqual(self._mixin.state, "running")
        self.assertTrue(self._mixin._running.is_set())
        self._mixin.stop()
        self.assertEqual(self._mixin.state, "stopped")
        self.assertFalse(self._mixin._running.is_set())
        self._mixin.stop()
        self.assertEqual(self._mixin.state, "stopped")
        self.assertFalse(self._mixin._running.is_set())

    def test_wait_timeout(self):
        """
        The test checks if the wait block is released once the timeout occurs.
        """
        start = timer()
        self._mixin.wait(timeout=1)
        end = timer()
        self.assertTrue(1.0 <= (end - start) < 1.1)

    def test_initial_state_triggers_exceptions(self):
        """
        This test checks all invalid triggers while the state machine is in INITIAL state.
        """
        with self.assertRaises(MachineError) as context:
            self._mixin.pause()
        exception = "Can't trigger event pause from state initial!"
        self.assertTrue(exception in str(context.exception))

        with self.assertRaises(MachineError) as context:
            self._mixin.resume()
        exception = "Can't trigger event resume from state initial!"
        self.assertTrue(exception in str(context.exception))

        with self.assertRaises(MachineError) as context:
            self._mixin.stop()
        exception = "Can't trigger event stop from state initial!"
        self.assertTrue(exception in str(context.exception))

    def test_running_state_triggers_exceptions(self):
        """
        This test checks all invalid triggers while the state machine is in RUNNING state.
        """
        self._mixin.running()
        with self.assertRaises(MachineError) as context:
            self._mixin.running()
        exception = "Can't trigger event running from state running!"
        self.assertTrue(exception in str(context.exception))

    def test_paused_state_triggers_exceptions(self):
        """
        This test checks all invalid triggers while the state machine is in PAUSED state.
        """
        self._mixin.running()
        self._mixin.pause()
        with self.assertRaises(MachineError) as context:
            self._mixin.running()
        exception = "Can't trigger event running from state paused!"
        self.assertTrue(exception in str(context.exception))

    def test_stopped_state_triggers_exceptions(self):
        """
        This test checks all invalid triggers while the state machine is in STOPPED state.
        """
        self._mixin.running()
        self._mixin.pause()
        self._mixin.stop()

        with self.assertRaises(MachineError) as context:
            self._mixin.running()
        exception = "Can't trigger event running from state stopped!"
        self.assertTrue(exception in str(context.exception))

        with self.assertRaises(MachineError) as context:
            self._mixin.pause()
        exception = "Can't trigger event pause from state stopped!"
        self.assertTrue(exception in str(context.exception))

        with self.assertRaises(MachineError) as context:
            self._mixin.resume()
        exception = "Can't trigger event resume from state stopped!"
        self.assertTrue(exception in str(context.exception))
