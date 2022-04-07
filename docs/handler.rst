:mod:`handler` --- threads
==========================

.. py:currentmodule:: src.thread_extension.handler


CycleWorker
-----------

.. code-block:: python

   import time
   from handler import CycleWorkerThread


   def run_routine(self) -> None:
       pass  # Put your code here

   worker = CycleWorkerThread(target=run_routine)
   worker.start()
   worker.join()

.. code-block:: python

   import time
   from handler import CycleWorkerThread

   class MyCycleWorker(CycleWorkerThread):
       def __init__(self) -> None:
           super().__init__()

       def run_routine(self) -> None:
           pass  # Put your code here

   worker = MyCycleWorker()
   worker.start()
   worker.join()

.. class:: CycleWorkerThread(delay=0.0, timeout= 1000.0, target=None, args=(), kwargs={}, daemon=False)

    This class represents a special thread type, which executes a predefined routine
    cyclically until a stop event is triggered.


   .. py:attribute:: delay

      Indicates how much time shall pass before the worker continues with
      the next cycle.

   .. py:attribute:: timeout

      Indicates how much time the worker is allowed to pause before the
      worker is automatically forced to stop.

   .. method:: run()

      Defines the worker's concrete workflow.

   .. method:: run_routine()

      Representing the worker's activity on each cycle.

      You may override this method in a subclass. The run_routine() method
      invokes the callable object passed to the object's constructor as the
      target argument, if any, with sequential and keyword arguments taken
      from the args and kwargs arguments, respectively.

   .. method:: is_working()

      Returns ```True``` if the worker is running a routine, ```False``` otherwise.

   .. method:: preparation()

      Optional preparatory steps for the worker to perform before starting.


   .. method:: post_processing()

      Optional follow-up steps for the worker to perform after stoppage.

TaskWorker
----------

.. code-block:: python

   import queue
   from handler import TaskWorkerThread

   class MyTaskWorker(TaskWorkerThread):
       def __init__(self, tasks: queue.Queue) -> None:
           super().__init__(tasks)

       def run_task(self, task: str) -> None:
           pass  # Put your code here

   my_tasks = queue.Queue()
   for nr in ["1", "2", "3"]:
       my_tasks.put(nr)
   worker = MyTaskWorker(my_tasks)
   worker.start()
   worker.join()

.. class:: TaskWorkerThread(tasks, delay=0.0, timeout= 1000.0, daemon=False)

    This class represents a special thread type, which processes a stack of
    similar tasks one after the other.

   .. py:attribute:: delay

      Indicates how much time shall pass before the worker continues with
      the next task.

   .. py:attribute:: timeout

      Indicates how much time the worker is allowed to pause before the
      worker is automatically forced to stop.

   .. method:: run()

      Defines the worker's concrete workflow.

   .. method:: run_task(task)

      Abstract method representing the worker's activity on all task.

   .. method:: is_working()

      Returns ```True``` if the worker is running a task, ```False``` otherwise.

   .. method:: preparation()

      Optional preparatory steps for the worker to perform before starting.

   .. method:: post_processing()

      Optional follow-up steps for the worker to perform after stoppage.
