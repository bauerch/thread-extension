:mod:`control` --- thread control mixin
=======================================

.. py:currentmodule:: src.control

The :class:`ThreadControlMixin` class extends typical `Threads objects
<https://docs.python.org/3/library/threading.html#thread-objects>`_ by
adding additional events to pause and stop threads at runtime.
This is especially useful in case of continuous running activities e.g.
monitoring tasks or batch jobs processed in the background.

