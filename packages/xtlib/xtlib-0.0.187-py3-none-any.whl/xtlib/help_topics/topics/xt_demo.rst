.. _xt_demo:

========================================
Run the XT Demo
========================================

XT now offers a self-contained demo that walks the user thru several common usage scenarios, using multiple ML backends.

The suggested steps for installing and running the demo are as follows:

    **1. PREPARE a conda virtual environment with PyTorch (only need to do this once):**
        
        .. code-block::

            > conda create -n MyEnvName python=3.6
            > conda activate MyEnvName
            > conda install pytorch torchvision cudatoolkit=10.1 -c pytorch

    **2. INSTALL CURL if you are running on Linux and will be using the Philly compute service:**

            https://www.cyberciti.biz/faq/how-to-install-curl-command-on-a-ubuntu-linux/

    **3. INSTALL XT:**

        .. code-block::

            > pip install -U xtlib

    **4. CREATE a set of demo files:**

        .. code-block::

            > xt create demo xt_demo

            This will create 2 files and 1 subdirectories in the *xt_demo* directory:
                - xt_config_overrides.yaml     (xt config settings, active when xt is run from this directory)
                - xt_demo.py - the python file that drives the demo
                - code  (a subdirectory containing some files used by the demo app)

    **5. Start the demo:**

        .. code-block::

            > cd xt_demo
            > python xt_demo.py

        Once started, you can navigate thru the demo with the following keys:
            - ENTER (to execute the current command)
            - 's'   (to skip to the next command)
            - 'b'   (to move to the previous command)
            - 'q'   (to quit the demo)
