import unittest
from timeit import default_timer as timer
from src.thread_extension import control


class ThreadControlMixinClass(unittest.TestCase):
    """
    This class represents a wrapper class for all unittests related to the
    ThreadControlMixin class within <src.thread_extension.control>.
    """
    def setUp(self):
        self._control = control.ThreadControlMixin()

    def tearDown(self):
        del self._control

    def test_additional_thread_control_states(self):
        """
        This test checks the correct transition into all possible states.
        """
        self.assertFalse(self._control.is_running())
        self.assertFalse(self._control.is_stopped())
        self.assertEqual(self._control.status, "initial")
        self._control.set_start_state()
        self.assertTrue(self._control.is_running())
        self.assertFalse(self._control.is_stopped())
        self.assertEqual(self._control.status, "running")
        self._control.pause()
        self.assertFalse(self._control.is_running())
        self.assertFalse(self._control.is_stopped())
        self.assertEqual(self._control.status, "paused")
        self._control.resume()
        self.assertTrue(self._control.is_running())
        self.assertFalse(self._control.is_stopped())
        self.assertEqual(self._control.status, "running")
        self._control.pause()
        self._control.stop()
        self.assertTrue(self._control.is_running())
        self.assertTrue(self._control.is_stopped())
        self.assertEqual(self._control.status, "stopped")
        self._control.set_end_state()
        self.assertFalse(self._control.is_running())
        self.assertTrue(self._control.is_stopped())
        self.assertEqual(self._control.status, "stopped")

    def test_paused_thread_timeout(self):
        """
        The test checks if a paused thread is released once the timeout occurs.
        """
        self._control.set_start_state()
        self._control.pause()
        start = timer()
        self._control.wait(timeout=1)
        end = timer()
        self.assertTrue(1.0 <= (end - start) < 1.1)

    def test_pre_start_exceptions(self):
        """
        This test checks all invalid calls before the thread is started.
        """
        with self.assertRaises(RuntimeError) as context:
            self._control.pause()
        exception = "Cannot pause thread before it is started"
        self.assertTrue(exception in str(context.exception))

        with self.assertRaises(RuntimeError) as context:
            self._control.resume()
        exception = "Cannot resume thread before it is started"
        self.assertTrue(exception in str(context.exception))

        with self.assertRaises(RuntimeError) as context:
            self._control.stop()
        exception = "Cannot stop thread before it is started"
        self.assertTrue(exception in str(context.exception))

        with self.assertRaises(RuntimeError) as context:
            self._control.wait(timeout=1)
        exception = "Cannot wait thread before it is started"
        self.assertTrue(exception in str(context.exception))

    def test_post_start_exceptions(self):
        """
        This test checks all invalid calls after the thread is stared.
        """
        self._control.set_start_state()

        with self.assertRaises(RuntimeError) as context:
            self._control.set_start_state()
        exception = "thread can only be started once"
        self.assertTrue(exception in str(context.exception))

        self._control.stop()

        with self.assertRaises(RuntimeError) as context:
            self._control.pause()
        exception = "Cannot pause thread after it is stopped"
        self.assertTrue(exception in str(context.exception))

        with self.assertRaises(RuntimeError) as context:
            self._control.resume()
        exception = "Cannot resume thread after it is stopped"
        self.assertTrue(exception in str(context.exception))

        with self.assertRaises(RuntimeError) as context:
            self._control.wait(timeout=1)
        exception = "Cannot wait thread after it is stopped"
        self.assertTrue(exception in str(context.exception))

        with self.assertRaises(RuntimeError) as context:
            self._control.stop()
        exception = "thread can only be stopped once"
        self.assertTrue(exception in str(context.exception))
