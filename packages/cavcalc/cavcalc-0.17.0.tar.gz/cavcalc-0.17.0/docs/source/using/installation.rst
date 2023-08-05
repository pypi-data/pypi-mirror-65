Installation
============

Release version
---------------

Installation is simple, just run::

    pip install --upgrade cavcalc

to install the latest release version of cavcalc.

Development version
-------------------

Follow the steps below to install the latest state of cavcalc. Make sure to follow the guide
corresponding to the system you are installing to.

.. rubric:: Linux / MacOS (Unix)

1. Clone the repository `<https://gitlab.com/sjrowlinson/cavcalc>`_ via::

    git clone https://gitlab.com/sjrowlinson/cavcalc

2. Change directory to your local copy of the cavcalc repository::

    cd cavcalc

3. Installation of cavcalc in development mode is now simple, just run::

    pip install -e .

   in the root directory of your local copy of the cavcalc repository.

.. rubric:: Windows

1. If you have not already done so, install the `Conda package manager <https://docs.conda.io/en/latest/miniconda.html>`_.

2. Again, if you have not already done so, install `Git for Windows <https://gitforwindows.org/>`_. You can either
   use the tools this provides directly to clone the cavcalc repository (see step 5 below) or add the path
   to your git executable to the Windows environment variables - details on how to do this are shown in the next step,
   but you can skip this if you intend to use the *git bash/gui here* feature(s) of Git for Windows.

3. (Optional) To be able to use git from the command line, and via an Anaconda Prompt, you need to add the path to your
   git executable (installed in the step above) to the Windows environment variables.

   Type "environment variables" into the Windows search bar and open the first result. Click the "Environment Variables..."
   button.

   In the new window that pops up, navigate to the lower panel (System Variables) and find the field named "Path". Click the
   "Edit" button with this field highlighted. You will now be presented with a window showing all the currently stored paths.
   Click the "New" button in this Window and add the following two paths separately::

    C:\Program Files\Git\bin\git.exe
    C:\Program Files\Git\cmd

   Note that these paths above are assuming that you did not change the default install location of Git for Windows in step 2.

4. Open an Anaconda Prompt using the Windows search bar.

5. Clone the repository `<https://gitlab.com/sjrowlinson/cavcalc>`_ via::

    git clone https://gitlab.com/sjrowlinson/cavcalc

   Note that if you skipped step 3 then you will need to use *git bash here* or *git gui here* by right clicking
   in the File Explorer. If you select *git bash here* then you will be presented with a bash-like terminal
   in which you can run the git clone command above. Close this terminal after cloning the repository and return
   to your Anaconda Prompt.

6. Change directory to your local copy of the cavcalc repository::

    cd cavcalc

7. Installation of cavcalc in development mode is now simple, just run::

    pip install -e .

   in the root directory of your local copy of the cavcalc repository.


Note that in the final step of both guides above we use the ``-e`` option with pip
install. This options means that the install is performed in "editable" mode such
that any changes to Python source code files in cavcalc (i.e. after pulling the
latest changes on master from the repository) will be reflected in a version installed
in this way.

.. rubric:: Keeping your development version up to date

If you want to use all the new features of cavcalc as they are developed then you will
need to pull changes from the repository as and when you need them. To do this, simply run::

    git pull

when in any directory of your local copy of the cavcalc repository.
