:mod:`control` --- thread control mixin
=======================================

.. py:currentmodule:: src.thread_extension.control

The :class:`ThreadControlMixin` class extends typical `Threads objects <https://docs.
python.org/3/library/threading.html#thread-objects>`_ by adding additional events to
pause and stop threads at runtime. This is especially useful in case of continuous
running activities e.g. monitoring tasks or batch jobs processed in the background.

The following state diagram illustrates the control flow of the mixin.

.. _link-status-diagram:

.. image:: resources/state_diagram_thread_control_mixin.png
  :scale: 54%
  :alt: State Diagram

To make use of this functionality simply create a new custom thread and subclass the
:class:`ThreadControlMixin` class as shown in the following example. From this point
on everything works like a conventional thread.

.. code-block:: python

   from threading import Thread
   from control import ThreadControlMixin


   class MyThread(Thread, ThreadControlMixin):
       def __init__(self):
           Thread.__init__(self)
           ThreadControlMixin.__init__(self)

       def run(self):
          pass  # Put your code here



.. class:: ThreadControlMixin

   This class extends a thread of control by providing events to pause and stop a thread
   at runtime.

   .. py:attribute:: status

      A string used for internal status tracking only. Can be one of the following options
      ``initial``, ``running``, ``paused`` or ``stopped``. For more information please
      refer to the :ref:`Status Diagram <link-status-diagram>` section.

   .. method:: is_running()

      This method returns ``True`` if the object is in ``running`` state and ``False``
      otherwise.

   .. method:: is_stopped()

      This method returns ``True`` just after the :meth:`~ThreadControlMixin.stop` event
      is set for the first time.

   .. method:: pause()

      This method puts the object from ``running`` into ``paused`` state.

      :meth:`~ThreadControlMixin.pause` raises a :exc:`RuntimeError` if an attempt is
      made to pause the current object during ``initial`` or ``stopped`` state.

   .. method:: resume()

      This method puts the object from ``paused`` into ``running`` state.

      :meth:`~ThreadControlMixin.resume` raises a :exc:`RuntimeError` if an attempt is
      made to resume the current object during ``initial`` or ``stopped`` state.

   .. method:: stop()

      This method triggers the stop event and can only be called once.

      This method will raise a :exc:`RuntimeError` if called more than once on the same
      object. It is also an error to :meth:`~ThreadControlMixin.stop` the object during
      ``initial`` state and attempts to do so raise the same exception.

   .. method:: wait(timeout=None)

      This method waits until a state change from ``paused`` to ``running`` happens.

      When the *timeout* argument is present and not ``None``, it should be a
      floating point number specifying a timeout for the operation in seconds
      (or fractions thereof).

      :meth:`~ThreadControlMixin.wait` raises a :exc:`RuntimeError` if an attempt is
      made to wait the current object during ``initial`` or ``stopped`` state.

   .. method:: set_start_state()

      This method puts the object from ``initial`` into ``running`` state and
      can only be called once.

      This method will raise a :exc:`RuntimeError` if called more than once on
      the same object.

   .. method:: set_end_state()

      This method puts the object into ``stopped`` state.

