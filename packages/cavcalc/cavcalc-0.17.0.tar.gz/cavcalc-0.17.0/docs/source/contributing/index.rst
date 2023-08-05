.. _developing:

Contributing to cavcalc
=======================

.. note::
    Whilst `cavcalc` is still in the Alpha development stage, I will not be accepting any
    external contributions in order to keep the underlying framework consistent and stable.
    This will be changed when `cavcalc` enters into a Beta development status. Refer to the
    `PyPI page for cavcalc <https://pypi.org/project/cavcalc/>`_ to see the latest development
    status.


Submitting a bug report
-----------------------

If you encounter a bug in the code or documentation, especially in a release version, do
not hesitate to submit an issue to the `Issue Tracker <https://gitlab.com/sjrowlinson/cavcalc/-/issues>`_.

When reporting a bug, please include the following:

- A short, top-level summary of the bug. In most cases, this should be 1-2 sentences.
- A **minimal** but *complete and verifiable* example to reproduce the bug. If the bug
  was encountered from the command line interface (CLI) then just include the command
  used. Otherwise, if the bug was encountered via the Python API, then include the relevant
  parts of the script which resulted in the bug.
- (If applicable) The actual result(s) of the example provided versus the expected result(s).
- The `cavcalc` version, Python version and platform (i.e. OS version) you are using. You can find the
  first two from a Python interpreter with, e.g:

>>> import platform
>>> platform.python_version()
'3.7.3'
>>> import cavcalc
>>> cavcalc.__version__
'0.13.0'

If the bug is Physics-related (e.g. an unexpected discrepancy in results between `cavcalc` and
another method) then you should also provide details of the method(s) used to compute the
result - in particular the equations used.
