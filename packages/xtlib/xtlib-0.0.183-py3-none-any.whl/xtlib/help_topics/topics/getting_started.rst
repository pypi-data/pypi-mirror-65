.. _getting_started:

========================================
Getting Started with XT
========================================

XT is a command line tool to help you manage and scale your machine learning experiments, with a 
uniform model of workspaces and runs, across a variety of compute services.  It addition, it includes
additonal services like live and post Tensorboard viewing, hyperparameter searching, and ad-hoc plotting.

-----------------------
XT Requirements
-----------------------

The requirements for installing and running XT are:
    - Windows or Linux
    - Python 3.5 or later   (recommended: Python 3.6)
    - Anaconda or other virtual python environment (recommended: Anaconda)
    - User must have an Azure account (for authenticated access to Azure computing storage and resources)
    - For Linux users who will be using the Microsoft internal Philly services, the **curl** must be installed::

        https://www.cyberciti.biz/faq/how-to-install-curl-command-on-a-ubuntu-linux/


------------------------------------------
XT Install
------------------------------------------

Note: XT supports using any ML framework, but the below steps install PyTorch because it
is used by the XT demo.  Adjust as appropriate.

The suggested steps for installing:

    **1. PREPARE a conda virtual environment with PyTorch (only need to do this once):**
        
        .. code-block::

            > conda create -n MyEnvName python=3.6
            > conda activate MyEnvName
            > conda install pytorch torchvision cudatoolkit=10.1 -c pytorch

    **2. INSTALL XT:**

        .. code-block::

            > pip install -U xtlib

------------------------------------------------
Next Steps
------------------------------------------------

If you haven't tried out the **XT demo**, we recommend that you start with that.  It walks you thru
running a large set of XT commands that demonstate the power of XT.  

If you're ready to get started using XT with one of your projects, we recommend that you start with the 
**Preparing A New Project** For XT topic.

.. seealso:: 

    - :ref:`Run the XT Demo <xt_demo>`
    - :ref:`Preparing A New Project <prepare_new_project>`