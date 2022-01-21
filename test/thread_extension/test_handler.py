import time
import unittest
from src.thread_extension import handler


class CycleWorkerThreadClass(unittest.TestCase):
    """
    This class represents a wrapper class for all unittests related to the
    CycleWorkerThread class within <src.thread_extension.handler>.
    """
    @staticmethod
    def work_routine() -> None:
        """
        Simulating a specific worker, that needs 100 ms to finish it's
        work routine.
        """
        time.sleep(0.1)

    def setUp(self):
        self.__worker = handler.CycleWorkerThread(target=self.work_routine)

    def tearDown(self):
        del self.__worker

    def test_property_delay(self):
        """
        This test checks if the property delay is set correctly.
        """
        self.assertEqual(self.__worker.delay, 0.0)
        self.__worker.delay = 1.0
        self.assertEqual(self.__worker.delay, 1.0)
        with self.assertRaises(ValueError) as context:
            self.__worker.delay = -1.0
        self.assertTrue("Delay must be non-negative" in str(context.exception))

    def test_property_timeout(self):
        """
        This test checks if the property timeout is set correctly.
        """
        self.assertEqual(self.__worker.timeout, 1000.0)
        self.__worker.timeout = 500.0
        self.assertEqual(self.__worker.timeout, 500.0)
        with self.assertRaises(ValueError) as context:
            self.__worker.timeout = -500.0
        self.assertTrue("Timeout must be non-negative" in str(context.exception))

    def test_start_pause_resume_stop(self):
        """
        This test checks if an active worker can transition into all states.
        """
        self._verify_initial_state()

        self.__worker.start()
        self._verify_operative_state()

        self.__worker.pause()
        self._verify_pause_state()

        self.__worker.resume()
        self._verify_operative_state()

        self.__worker.stop()
        self._verify_stopped_state()

    def test_start_pause_stop(self):
        """
        This test checks if an active worker can be forced to stop working
        permanently during pause.
        """
        self.__worker.timeout = 1.0
        self._verify_initial_state()

        self.__worker.start()
        self._verify_operative_state()

        self.__worker.pause()
        self._verify_pause_state()

        self.__worker.stop()
        self._verify_stopped_state()

    def test_start_pause_timeout(self):
        """
        This test checks if an active worker automatically stops working
        permanently once the maximum pause time passed.
        """
        self.__worker.timeout = 1.0
        self._verify_initial_state()

        self.__worker.start()
        self._verify_operative_state()

        self.__worker.pause()
        self._verify_stopped_state()

    def test_target_None(self):
        """
        This test checks if an activate worker without a given work routine
        is permanently stopped immediately.
        """
        self.__worker = handler.CycleWorkerThread(target=None)
        self._verify_initial_state()
        self.__worker.start()
        self._verify_stopped_state()

    def _verify_initial_state(self):
        self.assertFalse(self.__worker.is_alive())
        self.assertFalse(self.__worker.is_working())
        self.assertFalse(self.__worker._control.is_running())
        self.assertFalse(self.__worker._control.is_stopped())
        self.assertIn("initial", repr(self.__worker))

    def _verify_operative_state(self):
        self.assertTrue(self.__worker.is_alive())
        self.assertTrue(self.__worker._control.is_running())
        self.assertFalse(self.__worker._control.is_stopped())
        self.assertIn("started", repr(self.__worker))
        self.assertIn("running", repr(self.__worker))

    def _verify_pause_state(self):
        while self.__worker.is_working():
            time.sleep(0.005)
        self.assertTrue(self.__worker.is_alive())
        self.assertFalse(self.__worker.is_working())
        self.assertFalse(self.__worker._control.is_running())
        self.assertFalse(self.__worker._control.is_stopped())
        self.assertIn("started", repr(self.__worker))
        self.assertIn("paused", repr(self.__worker))

    def _verify_stopped_state(self):
        self.__worker.join(timeout=2.0)
        self.assertFalse(self.__worker.is_alive())
        self.assertFalse(self.__worker.is_working())
        self.assertFalse(self.__worker._control.is_running())
        self.assertTrue(self.__worker._control.is_stopped())
        self.assertIn("stopped", repr(self.__worker))
