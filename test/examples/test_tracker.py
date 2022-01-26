import os
import time
import unittest
import unittest.mock as mock
from typing import Union
from src.examples import tracker


# As defined in os module
AnyPath = Union[str, bytes, os.PathLike[str], os.PathLike[bytes]]


class NewFileTrackerClass(unittest.TestCase):
    """
    This class represents a wrapper class for all unittests related to the
    Worker class within <src.examples.tracker>.
    """
    _MODULE_PATH = "src.examples.tracker"
    _ROOT = r"path\to\folder"
    _FILES = [
        rf"{_ROOT}\file1.txt",
        rf"{_ROOT}\file2.csv",
        rf"{_ROOT}\file3.xml"
    ]
    _CTIME_DELTA = {
        rf"{_ROOT}\file1.txt": -5.0,
        rf"{_ROOT}\file2.csv": +5.0,
        rf"{_ROOT}\file3.xml": +6.0
    }

    def test_file_tracker_empty_folder(self):
        """
        This test checks if no new files are identified, in case the folder
        is empty.
        """
        m = mock.Mock()
        with mock.patch(f"{self._MODULE_PATH}.glob.glob", m, create=True):
            m.return_value = []
            my_tracker = tracker.NewFileTracker("dir_path")
            my_tracker.start()
            time.sleep(0.1)
            new_files = my_tracker.new_files
            result = []
            while not new_files.empty():
                result.append(new_files.get())
            self.assertEqual(result, [])
            my_tracker.stop()
            my_tracker.join(timeout=2.0)

    def test_file_tracker_functionality(self):
        """
        This test checks if the file tracker is working properly, by:
        1) determining the correct initial state,
        2) storing newly created files,
        3) storing previously tracked files, which are deleted and recreated
        """
        m1 = mock.Mock()
        m2 = mock.Mock()
        with mock.patch(f"{self._MODULE_PATH}.os.path.getctime", m1, create=True),\
             mock.patch(f"{self._MODULE_PATH}.glob.glob", m2, create=True):
            # 1) ###############################################################
            m1.side_effect = self._mock_getctime
            m2.return_value = self._FILES
            my_tracker = tracker.NewFileTracker(self._ROOT)
            my_tracker.start()
            time.sleep(0.1)
            new_files = my_tracker.new_files
            result = []
            while not new_files.empty():
                result.append(new_files.get())
            self.assertCountEqual(result, self._FILES[1:])
            # 2) ###############################################################
            # Simulates the detection of previously tracked files
            # and one newly created file
            m2.return_value = self._FILES + [rf"{self._ROOT}\file4.py"]
            time.sleep(0.1)
            result = []
            while not new_files.empty():
                result.append(new_files.get())
            self.assertEqual(result, [rf"{self._ROOT}\file4.py"])
            # 3) ###############################################################
            # Simulates the deletion of previously tracked files
            m2.return_value = []
            time.sleep(0.1)
            result = []
            while not new_files.empty():
                result.append(new_files.get())
            self.assertEqual(result, [])
            # Simulates the recreation of previously deleted files
            m2.return_value = self._FILES
            time.sleep(0.1)
            result = []
            while not new_files.empty():
                result.append(new_files.get())
            self.assertCountEqual(result, self._FILES)
            my_tracker.stop()
            my_tracker.join(timeout=2.0)

    def _mock_getctime(self, filename: AnyPath) -> float:
        return time.time() + self._CTIME_DELTA[filename]


if __name__ == "__main__":
    unittest.main()
