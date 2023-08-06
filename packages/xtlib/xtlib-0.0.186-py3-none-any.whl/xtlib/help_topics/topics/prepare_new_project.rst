.. _prepare_new_project:

========================================
Preparing a new project for XT 
========================================

This describes how to prepare a new project to be used with XT.  This consists of correcting defining a 
local xt_config.yaml file that will be used to submit your runs to the associated backend service, as 
well for other XT commands associated with your project.

Basic steps::

    - define or select a target environment to run the project on (Philly, Azure Batch, etc.)

    - decide if the project will be run in a predefined docker container, a custom docker container, 
      or in native mode

    - determine the additional environment dependencies you will have, above:
        - the docker container 
        - the conda environment
        - python packages
        - the native OS image

    - if your target is Philly, Batch, or Azure ML, you should declare you additional dependencies, or write
      a shell script to install the depencies and run your ML app

    - if your target is LOCAL or a POOL of vm's (which are considered by XT to be user-managed), you should manually prepare the machine(s) by installing
      the additional environment dependencies 


Creating a Local Config File
-----------------------------

Selecting a pre-build docker container 
--------------------------------------

Creating a custom docker container
-----------------------------------

Specifying your docker requirements
------------------------------------

Specifying additonal requirements in the config File
----------------------------------------------------

Creating a Run Script for installing additonal requirements
-----------------------------------------------------------

Uploading Data to a Cloud Data Folder
-------------------------------------

Accepting a Data Path in your app
---------------------------------

Adding XT logging code to your app
----------------------------------

.. seealso:: 

    - :ref:`xt config command <config>` 
    - :ref:`XT config file<xt_config_file>` 
