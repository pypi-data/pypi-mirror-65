.. _how_xt_works:

=======================================
How XT Works
=======================================

This page gives an overview of XT operates.

Services:
    1. XT needs a set of cloud services to run jobs on cloud computers, log stats, and store experiment artifacts
    2. After XT is installed, the **xt create team** command can be used to create a template for the services
    3. The user then runs the template in the Azure Portal to create the services
    4. Once created, the services can be used by a single user or shared among a team of users

Authentication:
    1. The user is initially authenticated by the Azure Active Directory service
    2. The user's service credentials are stored in Azure Key Vault
    3. The service credentials are cached and remain available for the current OS session
    4. When XT is run in a new OS session, the user will be authenticated again

Configuration Settings:
    1. XT maintains a set of default settings for all commands and services 
    2. Any subset of these settings can be overridden by a local XT config file (a file in the working directory)
    3. In addition, XT's command line options can override/supplement the config file settings relevant to the associated command

Basic XT configuration:
    1. Enter your Azure service information in the **external-services** section of your config file
    2. Create entries in the **compute-targets** section for 1 or more COMPUTE targets to use for running experiments
    3. Add the storage, compute, and vault services to be used by XT in the **xt-services** section
    4. For each compute target, specify the **setup** property with the name of an entry in the **setup** section
    5. **setups** entries allow you to specify:
        - an environment activation command (conda, venv, etc.)
        - a list of conda packages your app needs installed on the associated compute target
        - a list of pip packages your app needs installed on the associated compute target
    6. [optional] Enter the computers that you have available to run with in the **boxes** section 

----------------------------------
Core Services
----------------------------------

XT has a number of features and commands, but they revolve around 3 fundamental core services:
    - job submission
    - experiment storage
    - experiment stats

-----------------------------
Experiment Storage
-----------------------------

The artifacts of each job you run under XT are store in your specified XT Storage service.  These artifacts include:

    - job files:
        - your code files (as a .zip file)
        - job log files

    - run files (a set for each run of your job)
        - your live output files (files written to your mounted run storage)
        - your final output files (captured at the end of your run)
        - run log files

-----------------------------
Experiment Stats
-----------------------------

The experiment stats include:

    - job properties
    - run properties (for each run in your job)
    - hyperparameter settings that you have logged to XT
    - metrics that you have logged to XT

All of this information is stored in your XT Storage service as well as in your MongoDB database service for fast access.

.. seealso:: 

    - :ref:`Creating XT Services <creating_xt_services>`
    - :ref:`XT Login <login>`
    - :ref:`Prepare a new Project <prepare_new_project>`
    - :ref:`Job Submission <job_submission>`
