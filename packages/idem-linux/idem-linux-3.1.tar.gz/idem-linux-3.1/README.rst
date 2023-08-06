**********
IDEM-LINUX
**********
**Grains, execution modules, and state modules common to all linux systems**

INSTALLATION
============

Install with pip::

    pip install idem-linux

DEVELOPMENT INSTALLATION
========================


Clone the `idem-linux` repo and install with pip::

    git clone https://gitlab.com/saltstack/pop/idem-linux.git idem_linux
    pip install -e idem_linux

EXECUTION
=========
After installation the `corn` command should now be available

TESTING
=======
install `requirements-test.txt` with pip and run pytest::

    pip install -r idem-linux/requirements-test.txt
    pytest idem-linux/tests

VERTICAL APP-MERGING
====================
Instructions for extending idem-linux into an OS or distro specific pop project

Install pop::

    pip install --upgrade pop

Create a new directory for the project::

    mkdir idem-{specific_linux_distro}
    cd idem-{specific_linux_distro}


Use `pop-seed` to generate the structure of a project that extends `corn` and `idem`::

    pop-seed -t v idem-{specific_linux_distro} -d corn exec states

* "-t v" specifies that this is a vertically app-merged project
*  "-d corn exec states" says that we want to implement the dynamic names of "corn", "exec", and "states"

Add "idem-linux" to the requirements.txt::

    echo "idem-linux @ git+https://gitlab.com/saltstack/pop/idem-linux.git" >> requirements.txt

And that's it!  Go to town making corn, execution modules, and state modules specific to your linux distro.
Follow the conventions you see in idem-linux.

For information about running idem states and execution modules check out
https://idem.readthedocs.io
