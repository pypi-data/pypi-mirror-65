********
IDEM-BSD
********
**Grains, execution modules, and state modules common to all bsd systems**

INSTALLATION
============

Install with pip::

    pip install idem-bsd

DEVELOPMENT INSTALLATION
========================


Clone the `idem-bsd` repo and install with pip::

    git clone https://gitlab.com/saltstack/pop/idem-bsd.git idem_bsd
    pip install -e idem_bsd

EXECUTION
=========
After installation the `corn` command should now be available

TESTING
=======
install `requirements-test.txt` with pip and run pytest::

    pip install -r idem-bsd/requirements-test.txt
    pytest idem-bsd/tests

VERTICAL APP-MERGING
====================
Instructions for extending idem-bsd into an OS specific pop project

Install pop::

    pip install --upgrade pop

Create a new directory for the project::

    mkdir idem-{specific_bsd_os}
    cd idem-{specific_bsd_os}


Use `pop-seed` to generate the structure of a project that extends `corn` and `idem`::

    pop-seed -t v idem-{specific_bsd_os} -d corn exec states

* "-t v" specifies that this is a vertically app-merged project
*  "-d corn exec states" says that we want to implement the dynamic names of "corn", "exec", and "states"

Add "idem-bsd" to the requirements.txt::

    echo "idem-bsd @ git+https://gitlab.com/saltstack/pop/idem-bsd.git" >> requirements.txt

And that's it!  Go to town making corn, execution modules, and state modules specific to your bsd os.
Follow the conventions you see in idem-bsd.

For information about running idem states and execution modules check out
https://idem.readthedocs.io
