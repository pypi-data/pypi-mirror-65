.. _xt_config_file:

====================
XT Config File
====================

This page explains the sections and properties of the XT config file.  

------------------------
Overview
------------------------

The behavior of XT is controlled by an extensive set of properties, organized into sections.

These properties are all listed in the default XT config file (which is a readonly file, installed as part of the XTLib package).  Users
can override or supplement these properties using a local XT config file, residing in the command line current directory.  This file only has to 
contain the properties that are being changed, and are typically much smaller then the default config file.

In addition, some of the properties can be overridden by XT command options.  Refer to the help for each command to view the available options.

------------------------
Sections
------------------------


***************************
1. External Services
***************************

The **external-services** section defines the service names and credentials for services defined in subsequent sections.
These services are mostly Azure-based services, but also include services like Philly.

There are currently 4 general types of services defined as external services:
    - compute services              (services that can run ML jobs)
    - storage services              (services where files (blobs) can be read and written)
    - mongo db services             (database services that expose the MongoDB interface)
    - docker registry services      (services that can store (register and retreive) docker containers)

The general entry for an exernal service in the XT config file looks like:

    name: {type: "servicetype", prop: "value" }

Where:
    - **name** is the actual serivce name recognized by the service
    - **servicetype** is one of: **philly**, **batch**, **aml**, **storage**, **mongo**, **registry**
    - **prop** and **value** represent other credentials appropriate to the associated service

Service properties by service type:

    - philly      - no additional properties
    - batch       - **key**, **url**
    - aml         - **subscription-id**, **resource-group**
    - storage     - **key**
    - mongo       - **mongo-connection-string**
    - registry    - **login-server**, **username**, **password**, **login**

Example: suppose you have created a new Azure ML service called **myaml** using the Azure Portal.  To register this for use in XT,
you would find the **subscription-id** and **resource-group** for your new service in the Azure Portal (see they **Settings | Properties** section) and then 
define the following property under the **external-services** property of your local XT config file, filling in your values for **subscription-id** and
**resource-group**::

    external-services:
        myaml: {type: "aml", subscription-id: "", resource-group: ""}


***************************
2. XT Services
***************************

The **xt-services** section identifies the specific external service to use for each of the following XT services:: 
    - storage
    - mongo
    - target

The **storage** service is the service used to for storage of all workspace, experiment, and run related files, include source code,
log files, and output files.

The **mongo** service is the database service (with a MongoDB interface) that is used by XT for fast access to run and job stats and metrics.

The **target** service is the default compute target used by XT for running jobs. Target services are defined in the **Compute Targets** section 
of the XT config file.

Example: here is an example of the **xt-services** section::

    xt-services:
        storage: "xtsandboxstorage"        # storage for all services 
        mongo: "xt-sandbox-cosmos"         # database used for all runs across services
        target: "local"                    # our default compute target 


***************************
3. Compute Targets
***************************

The **compute-targets** section defines the available configured services that can be used for running your ML apps from XT.  

There are currently 4 types of targets that can be defined:
    - philly     (this represents a configuration of a Philly service that was defined in the external-services section)
    - batch      (this represents a configuration of an Azure Batch service that was defined in the external-services section)
    - aml        (this represents a configuration of an Azure ML service that was defined in the external-services section)
    - pool       (this represents a configuration for a set of named VMs)

The general entry for compute target looks like:

    name: {service: "servicename", prop: "value" }

Where:: 
    - **servicename** is the name of a service defined in the **external-services** section
    - **prop** and **value** represent configuration properties specific to each service type

Configuration properties by service type:
    philly:
        - **cluster**: the name of the Philly cluster to run on
        - **vc**: the name of the Philly virtual cluster to run on
        - **sku**: the type of machine to run on (G1=single GPU, G4=4 GPUs, G8=8 GPUs, G16=16 GPUs)
        - **nodes**: the number of machines to run on 
        - **low-pri**: if True. job should be run on a preemptible set of machines 
        - **docker**: the name of a docker environment (defined in the **dockers** section) that will be used to run the job
    batch:
        - **vm-size**: the Azure name that defines the machine hardware to be used (e.g., Standard_NC6)
        - **azure-image**: the name of an image defined in the **azure-images** section (defines the OS to run on)
        - **nodes**: the number of machines to run on 
        - **low-pri**: if True. job should be run on a preemptible set of machines 
        - **box-class**: the name of an entry in the **script-launch-prefix** section, used to run scripts on the batch VMs
        - **docker**: the name of a docker environment (defined in the **dockers** section) that will be used to run the job
    aml:       
        - **compute**: the name of a predefined Azure Compute object that should be used for running jobs (defines a configuration of VMs)
        - **vm-size**: the Azure name that defines the machine hardware to be used (e.g., Standard_NC6)
        - **nodes**: the number of machines to run on 
        - **low-pri**: if True. job should be run on a preemptible set of machines 
        - **docker**: the name of a docker environment (defined in the **dockers** section) that will be used to run the job
    pool:
        - **boxes** (a list of box names (defined in the **boxes** section) that will be used to run the job
        - **docker**: the name of a docker environment (defined in the **dockers** section) that will be used to run the job

Example: here is an example of how to specify an Azure Batch compute target::

    compute-targets:
        batch: {service: "xtsandboxbatch", vm-size: "Standard_NC6", azure-image: "dsvm", nodes: 1, low-pri: true,  box-class: "dsvm", environment: "none"}


***************************
4. Environments
***************************
The **environment** section lets users define named environments (docker images) that can be used in compute target definitions.

An environment should be defined as follows:

    name: {registry: "registryservice", image: "imagename" }

Where:
    - **name** is the user-defined friendly name for the environment
    - **registryservice** is the name of a registry service defined in the **external-services** section
    - **imagename** is the name of a docker image defined in the registry service.

Example: here is an example of how to specify a docker image that is registered in the **philly-registry** service::

    environments:
        philly-pytorch: {registry: "philly-registry", image: "microsoft_pytorch:v1.2.0_gpu_cuda9.0_py36_release_gpuenv_hvd0.16.2"}

***************************
5. General
***************************

The **general** section defines the set of general XT properties and their values. 

Here are the **general** properties:

    **username**:
        - this should be set to "$username", which will default to the corporate login name of the user.  this value is used for logging for new runs/jobs, as well as when submitting Philly commands from linux.

    **workspace**:
        - this specifies the name of the default XT workspace to use for various XT commands

    **experiment**:
        - this specifies the name of the default XT experiment to use for various XT commands

    **attach**:
        - when True, the user's console will be automatically attached to the first run output when a job is submitted
          using the "run" or "rerun" command

    **feedback**:
        - when true, user will receive percentage feedback for upload and download commands

    **run-cache-dir**:
        - this specifies the local directory that XT will use to cache run information for certain commands

    **distributed**   
        - when True, XT will run the submitted job as a distributed training run on multiple nodes (boxes).

    **direct-run**
        - normally, runs under XT are launched and controlled by the XT controller app, running on the same compute node (box) as the 
          run.  when **direct-run** is specified, the XT controller is not used, and the runs are launched and controller directly by
          the underlying service controller.  The setting of this property is ignored by the **pool** service, which always uses the XT controller.

    **quick-start**
        - when True, the XT start-up time for each command is reduced.  This is an experimental property that is expected to eventuall be removed.

    **primary-metric**
        - this property should be set to the name of the primary metric reported by your ML app.  this metric will be used to guide
          hyperparameter searches and early stopping algorithms.

    **maximize-metric**
        - when set to True, the **primary-metric** is treated as a metric that the hyperparmeter search should maximize (e.g., accuracy).  
          when set to False, it is treated as a metric that should be minimized (like loss).

    **conda-packages**
        - this is a list of packages that should be installed by **conda** on the target nodes (boxes).  some services, like Azure ML, will
          use this information to automatically build (or select a previously built) docker image on behalf of the user.

    **pip-packages**
        - this is a list of packages that should be installed by **pip** on the target nodes (boxes).  some services, like Azure ML, will
          use this information to automatically build (or select a previously built) docker image on behalf of the user.

    **env-vars**
        - these are environment variable name/value pairs, in the form of a dictionary, that should be set on the target node/box before the user's runs 
          begin executing.

Example of a general section definition::

    general:
        username: "$username"                  # use our Microsoft login
        workspace: "ws1"                       # create new runs in this workspace
        experiment: "exper1"                   # associate new runs with this experiment
        attach: false                          # do not auto-attach to runs
        feedback: true                         # show detailed feedback for upload/download
        run-cache-dir: "~/.xt/runs-cache"      # where we cache run information (SUMMARY and ALLRUNS)
        distributed: false                     # normal run
        direct-run: false                      # use the XT controller
        quick-start: false                     # don't use this feature
        primary-metric: "test-acc"             # the accuracy of our validation data
        maximize-metric: true                  # we want to maximize the test-acc
        conda-packages: []                     # no packages for conda to install

        # getting torchvision + pillow to run on correctly batch, philly, and aml is tricky 
        pip-packages: ["torch==1.2.0", "torchvision==0.4.1", "Pillow==6.2.0", "watchdog==0.9.0", "xtlib==*"]   

        env-vars: {"is_test_run": False}       # set the environment variable "is_test_run" to False before starting the run


***************************
6. Code
***************************

The **code** section defines the set of XT properties that control the creation of code snapshots (collecting and copying the code from the local 
machine to the storage service as part of the run submission process).  

Here are the **code** properties:

    **code-dirs**
        - this is a list of directories that define the source code used by the ML app.  The first directory specified is considered the root of the code directory,
          and any other specified directories are copied to storage as children of the root directory.  There is a special symbol that can be used (usually for the 
          first directory), **$scriptdir**.  If found, it is replaced by the directory that contains the run script or app specifed by the **run** command.  Also, for
          any specified directory, a wildcard name can be used as the last node of the directory.  In addition, the special wildcard **\*\*** can be used to 
          specify that the directory should be captured recursively (processing all subdirectories of all subdirectories).

    **code-upload**
        - this is normally set to True, meaning that the contents of the **code-dirs** should be captured and uploaded to the XT storage associated
          with the submitted job.  If set to False, no code files will be captured/copied.  

    **code-zip**
        - this specifies if the code files should be zipped before uploading, and if so, what type of compression should be used.  Depending on your local 
          machine computing speed, the number and size of your code files, and your upload speed, you can increase the speed of your code capture/upload
          process by trying different values for this property.  The supported values are **none** (meaning do not 
          create a .zip file), **fast** (meaning create a .zip file, but don't compress the files), and **compress** (meaning create a .zip file
          and compress the files added to it).

    **code-omit**
        - this is a list of directory or file names, optionally containing wildcard characters.  When capturing the code files, files or directories matching
          any names in **code-omit** will not be included.

    **xtlib-upload**
        - when set to True, the source code files from XTLib (the XT package) will be included as a child directory of the root code directory.  this allows
        the XT controller and your ML app to run against the same version of XTLib that you are using on your desktop.  it was primarily designed as an 
        internal feature for use by XT developers.

Example: here is an example of the **code** section::

    code:
        xtlib-upload: true                 # upload XTLIB sources files for each run for use by controller and ML app
        code-zip: "compress"               # none/fast/compress ("fast" means zip w/o compression)
        code-omit: [".git", "__pycache__", "logs", "data"]      # directories and files to omit when capturing before/after files

***************************
7. After Files
***************************

The **after-files** section defines the set of XT properties that control the uploading of run-related files after the run has completed.

Here are the **after-files** properties:

    **after-dirs**
        - this is a list of directories that define the files that should be captured and uploader after a run has completed.  the directories
          are specified relative to the working directory of the run (which is set by the XT controller).  Any directory can optionally include
          a wildcard name as its last node, to match files in the specified directory.  In addition, the special wildcard **\*\*** can be used to 
          specify that the directory should be captured recursively (processing all subdirectories of all subdirectories).

    **after-upload**
        - this is normally set to True, meaning that the contents of the **after-files** should be captured and uploaded to the XT storage associated
          with the asociated run.  If set to False, no files will be captured/copied.

Example: here is an example of the **after-files** section::

    after-files:
        after-dirs: ["*", "output/*"]         # specifies output files (for capture from compute node to STORE)
        after-upload: true                    # should after files be uploaded at end of run?

***************************
8. Data
***************************

The **data** section defines the set of XT properties that control the actions taken by XT on run-related data files.  These actions are:
    - uploading of data files to XT storage when a run is submitted
    - downloading data files to the compute node when a run is about to be started
    - mounting of a local drive to the data files in XT storage

Here are the **data** properties:

    **data-local**
        - this is the directory on the local machine where the data can be found.  used when **data-upload** property is set to True.

    **data-upload**
        - normally set to False.  When set to True, the data file specified by the **data-local** directory will be uploaded to XT storage
          each time a job is submitted.

    **data-share-path**
        - this is path on the XT data share where the data files should reside.

    **data-action**
        - this is the action that XT should take on the compute node before beginning the run.  the value must be one of:
        **none** (do nothing related to data files), **download** (download the files from the **data-share-path**), 
        or **mount** (mount the **data-share-path** to a local folder name).  if **download** or **mount** is specified, the 
        ML app can retreive the associated local folder by querying the value of the environment variable **XT_DATA_DIR**.

    **data-omit**
        - this is a list of directory or file names, optionally containing wildcard characters.  When capturing and uploading data files,
        files or directories matching any names in **data-omit** will not be included.

    **data-writable**
        - when set to True and when **data-action** is set to **mount**, the mounted directory will be writable (files can be added or updated).

Example: here is an example of the **data** section::

    data:
        data-local: ""                         # local directory of data for app
        data-upload: false                     # should data automatically be uploaded
        data-share-path: ""                    # path in data share for current app's data
        data-action: "none"                    # data action at start of run: none, download, mount
        data-omit: []                          # directories and files to omit when capturing before/after files
        data-writable: false                   # when true, mounted data is writable
        
***************************
9. Model
***************************

The **model** section defines the set of XT properties that control the actions taken by XT related to the run-related model files. 

These actions are:
    - downloading model files to the compute node when a run is about to be started
    - mounting of a local drive to the model files in XT storage

Here are the **model** properties:

    **model-share-path**
        - this is path on the XT model share where the model files should reside.

    **model-action**
        - this is the action that XT should take on the compute node before beginning the run.  the value must be one of:
        **none** (do nothing related to model files), **download** (download the files from the **model-share-path**), 
        or **mount** (mount the **model-share-path** to a local folder name).  if **download** or **mount** is specified, the 
        ML app can retreive the associated local folder by querying the value of the environment variable **XT_MODEL_DIR**.

    **model-writable**
        - when set to True and when **model-action** is set to **mount**, the mounted directory will be writable (files can be added or updated).

Example: here is an example of the **model** section::

    model:
        model-share-path: ""                   # path in model share for current app's model
        model-action: "none"                   # model action at start of run: none, download, mount
        model-writable: false                  # when true, mounted model is writable

***************************
10. Logging
***************************

The **logging** section controls the logging of run-related events and the mirroring of run-related files to XT storage.  Note that the
implementation of the XT **view tensorboard** command  depends on mirroring of the Tensorboard log files.

Here are the **logging** properties:

    **log**
        - the normal value is True, which means experiment run events are logged to XT storage.  when set to False, these events are not logged.

    **notes**
        - controls if and when a user is prompted for a description of the job being submitted.  the value must be one of: **none** (no prompting 
        is done), **before** (user is prompted at the beginning of the submission), or **after** (user is prompted at the end of the submission).

    **mirror-files**
        - this is a list of directories that define the files that should be watch and uploaded to XT storage associated with the run.   the directories
          are specified relative to the working directory of the run (which is set by the XT controller).  Any directory can optionally include
          a wildcard name as its last node, to match files in the specified directory.  In addition, the special wildcard **\*\*** can be used to 
          specify that the directory should be captured recursively (processing all subdirectories of all subdirectories).  One of the uses for mirroring 
          run files is the support of XT **view tensorboard** command.

    **mirror-dest**
        - this controls if files are mirrored and if so, where they are copied to.  the value must currently be one of: **none** (no file watching or 
          mirroring is done), or **storage** (files specified by **mirror-files** are watched and copied to the XT storage associated with
          the run).

Example: here is an example of the **logging** section::

    logging:
        log: true                              # specifies if experiments are logged to STORE
        notes: "none"                          # control when user is prompted for notes (none, before, after, all)
        mirror-files: "logs/**"                # default wildcard path for log files to mirror
        mirror-dest: "storage"                 # one of: none, storage

***************************
11. Internal
***************************

The **internal** section is for controlling operations in XT designed to be used by internal XT developers, but may also be of value to XT users.

Here are the **internal** properties:

    **console**
        - the controls the XT console output.  values must be one of: **none** (all XT output is supressed), **normal** (high level command progress and results
          are sent to the console), **diagnostics** (command timing and high level trace information is also sent to the console), or **detail** (command timing
          and detailed trace information is also sent to the console).
          
    **stack-trace**
        - when set to True and execeptions are raised, the associated stack traces are sent to the console.  when set to False, the stack traces are 
        omitted.

    **auto-start**
        - when set to True, the XT controller is automatically started for "view status" commands (mainly for use when running on the local machine 
        or a specified pool of boxes).  The current design is that the XT controller continues to run after the submitted job as completed, but 
        this may change in the future.

Example: here is an example of the **internal** section::

    internal:
        console: "normal"                      # controls the level of console output (none, normal, diagnostics, detail)
        stack-trace: false                     # show stack trace for errors  
        auto-start: false                      # when true, the controller is automatically started on 'status' cmd

***************************
12. AML Options
***************************

The **aml-options** section contains the properties that are currently specific to the Azure ML service.  These properties are:

    **use-gpu**
        - if True and a GPU exists, it will be made available to your app.  If False, no GPU will be made available.  

    **use-docker**
        - if True, a docker image will be defined based on the specified **framework**, **conda-packages**, 
           and **pip-packages**.  if an matching image already exists, that will be used for the run.  Otherwise, 
           a custom docker image will be built and used.  the image will then be saved by Azure ML for subsequent runs.

    **framework**
        - this is the base framework that will be used for the run.  supported values are: **pytorch**, **tensorflow**, 
            **chainer**, and **estimator**.

    **fw-version**
        - this specifies the version string of the **framework** to be used.

    **user-managed**
        - when True, Azure ML assumes the environment has already been correctly configured by the user.  This property
        should be set to False for normal runs.

    **distributed-training**
        - this specifies the name of the distributed backend to use for distributed training.  the value should be one of:
          **mpi**, **gloo**, or **nccl**.

    **max-seconds**
        - this specified the time limit for the ML run.  if the running time exceeds this limit, a timeout error will occur.
          this property can be set to -1 to specify that maximize run time.

Example: here is an example of the **aml-options** section::

    aml-options:
        use-gpu: true                          # use GPU(s) 
        use-docker: true                       # by default, build a docker image for pip/conda dependencies (faster startup, once built)
        framework: "pytorch"                   # currently, we support pytorch, tensorflow, or chainer
        fw-version: "1.2"                      # version of framework (string)
        user-managed: false                    # when true, AML assumes we have correct prepared environment (for local runs)
        distributed-training: "mpi"            # one of: mpi, gloo, or nccl
        max-seconds: -1                        # max secs for run before timeout (-1 for none)

***************************
13. Early Stopping
***************************

The **early-stopping** section specifies properties that are used by the Azure ML early stopping algorithms (currently only available when
running on an AML service).  Early stopping algorithms looks at the training progress and status of an ML app and decide if the trining should 
be stopped before the specified number of steps or epochs are reached.

The properties in the **early-stopping** section are:

    **early-policy**
        - specifies the early stopping algorithm to be used.  value must be one of: **none** (no early stopping is done by AML), 
        **bandit** (the AML Bandit ES algorithm is used), **median** (the AML Median ES algorithm is used), or **truncation** 
        (the AML Truncation ES algorithm is used)

    **delay-evaluation**
        - the # of metric reportings to wait before the first application of the early stopping policy

    **evaluation-interval**
        - the frequency (# of metric reportings) to wait before reapplying the early stopping policy.

    **slack-factor**
        - for the Bandit ES only: specified as a ratio, the delta between the current evaluation and the best performing
          evaluation
          
    **stack-amount**
        - for the Bandit ES only: specified as an amount, the delta between the current evaluation and the best performing
          evaluation

    **truncation-percentage**
        - for the Truncation ES only: percentage of runs to cancel after each early stopping evaluation

Example: here is an example of the **early-stopping** section::

    early-stopping:
        early-policy: "none"           # bandit, median, truncation, none
        delay-evaluation: 10           # number of evals (metric loggings) to delay before the first policy application
        evaluation-interval: 1         # the frequencency (# of metric logs) for testing the policy
        slack-factor: 0                # (bandit only) specified as a ratio, the delta between this eval and the best performing eval
        slack-amount: 0                # (bandit only) specified as an amount, the delta between this eval and the best performing eval
        truncation-percentage: 5       # (truncation only) percent of runs to cancel at each eval interval

***************************
14. Hyperparameter Search
***************************

The **hyperparameter-search** section controls how hyperparameter searching is done in XT.  

In XT, hyperparameter searching starts from a set of named hyperparameter and their associated value distributions.  
These are normally specified in a hyperparameter config file (.txt), or they can be specified in the run command, 
as special arguments to your ML app.  Before each search run is started, the values for each hyperparameter
are sampled from their distributes, according to the hyperparameter search algorithm being used.  Once a
set of values for the hyperparameters has been determined, the values can then be passed to the ML
app thru an app config file (.txt), or by passing command line arguments to the ML app.

The **hyperparameter-search** section properties are:

    **option-prefix**
        - if this value is an empty string or the value "none", command line arguments are not generated for
        each search run.  otherwise, the value of **option-prefix** is used in front of each hyperparameter name to 
        form command line arguments to the ML app.  for example, if **option-prefix** is set to "--", and the
        hyperparameter **lr** is being set to .05 by the hyperparameter search algorithm, then the 
        command argument "--lr=.05" would be passed to your ML app on its command line when it is run.

    **aggregate-dest**
        - this is where results for the hyperparameter search are aggregated.  This aggregation enabled faster access
        to the log files for the runs in the search.  The value of this property should be one of these: 
        **none** (no aggregation is done), **job** (results are aggregated to the storage area associated with
        the job), or **experiment** (results are aggregated to the storage area associated with the 
        experiment).

    **search-type**
        - this is the type of search algorithm to use.  the values currently support are: **none** (for no searching), 
        **grid** (for a exhaustive rollout of all combinations of discrete hyperparameter values), **random** (for
        random sampling of the hyperparameter values), **bayesian** (for a search guided by bayesian learning), and
        **dgd** (the distributed grid descent algorithm, a search guided by nearest neighbors of best searches).

    **max-minutes**
        - specifies the maximum time in minutes for a hyperparameter search run.  if set the -1, no maximum time
        is enforced.  currently only supported for Azure ML service.

    **max-concurrent-runs**
        - this is the maximum concurrent runs over all nodes.  currently only supported for Azure ML service.

    **hp-config**
        - this is the name of the file containing the hyperparameters and their associated values or value distributions.

    **fn-generated-config**
        - the is the name of the app config file to be generated in the run directory before each run.  this file 
        should be used by the ML app to load the its hyperparameter values for the current run.  if set to an empty string, 
        no file will be generated.

Here is an example of a **hyperparameter-search** section::

    hyperparameter-search:
        option-prefix: "--"               # prefix for hp search generated cmdline args (set to None to disable cmd args from HP's)
        aggregate-dest: "job"          # set to "job", "experiment", or "none"
        search-type: "random"          # random, grid, bayesian, or dgd
        max-minutes: -1                # -1=no maximum
        max-concurrent-runs: 100       # max concurrent runs over all nodes
        hp-config: ""                  # the name of the text file containing the hyperparameter ranges to be searched
        fn-generated-config: "config.txt"  # name of HP search generated config file

***************************
15. Hyperparameter Explorer
***************************

The **hyperparameter-explorer** section specifies hyperparameter and metric names and other properties used by the Hyperparameter 
Explorer (HX).  HX is a GUI interface for exploring the effect of different hyperparameter settings on the performance of 
your ML trained model.

The properties for the **hyperparameter-explorer** section are:

    **hx-cache-dir**
        - this is the name of a directory that HX will use to download all of the run logs for an experiment or job.

    **steps-name**
        - this is the name of the hyperparameter that your ML app uses for specifying the total number of training steps.

    **log-interval-name**
        - this is the name of the hyperparameter that your ML app uses for specifying the number of steps between logging metrics.

    **step-name**
        - this is the name of the metric your ML app uses to represent the number of training steps processed to-date.

    **time-name**
        - this is the name of the metric your ML app uses to represent the elapsed time of your training.

    **sample-efficiency-name**
        - this is the name of the metric your ML app uses to represent the sample efficiency of your training to-date.

    **success-rate-name:**
        - this is the name of the metric your ML app uses to represent the success rate of your training to-date.

Here is an example of a **hyperparameter-explorer** section::

    hyperparameter-explorer:
        hx-cache-dir: "c:/hx_cache"        # directory hx uses for caching experiment runs 
        steps-name: "steps"                # usually "epochs" or "steps" (hyperparameter - total # of steps to be run)
        log-interval-name: "LOG_INTERVAL"  # name of hyperparameter that specifies how often to log metrics
        step-name: "step"                  # usually "epoch" or "step" (metrics - current step of training/testing)
        time-name: "sec"                   # usually "epoch" or "sec
        sample-efficiency-name: "SE"       # sample efficiency name 
        success-rate-name: "RSR"           # success rate name 

***************************
16. Run Reports
***************************

The **run-reports** section controls how the **list runs** command formats its reports.  The primary control
revolves around the run columns, drawn from:

    - standard run properties (like **target** or **status**)
    - ML app logged hyperparameters (name must be prefixed by "hparams.")
    - ML app logged metrics (name must be prefixed by "metrics.")
    - user assigned run tags (name must be prefixed by "tags.")

The properties of the **run-reports** section are:

    **sort**
        - specifies the run column used for sorting the runs.  if not specified, this property default to "run".

    **reverse**
        - if set to True, a reverse sort is preformed (runs are arranged in descending order of their sort column)

    **max-width**
        - the maximum width of a column in the report (in text characters)

    **precison** 
        - the default precision (number of decimal places) to use for formatting float values 

    **uppercase-hdr**
        - if True, the header names on the top and bottom of the report are uppercased.

    **right-align-numeric**
        - if True, number values are right-aligned in their columns
    
    **truncate-with-ellipses**
        - if True, column values that exceed the maximum width for the column are truncated with ellipses.

    **status**
        - if specified, this value is used to match records by their status value (filters out non-matching records)

    **record-rollup**
        - if true, the reporting record with the best primary metric will select the metrics to display.  if False, the
          last reported set of metric will be displayed.

    **columns**
        - this is a list of column specifications to define the colums and their formatting for the report.  A column 
          specification can be as simple as the name of a column, but it can also include some customization.  Refer 
          to the `Columns in XT <columns>` topic for more information.

An example of the **run-reports** section::

    run-reports:
        sort: "name"                   # default column sort for experiment list (name, value, status, duration)
        reverse: false                 # if experiment sort should be reversed in order    
        max-width: 30                  # max width of any column
        precision: 3                   # number of fractional digits to display for float values
        uppercase-hdr: true            # show column names in uppercase letters
        right-align-numeric: true      # right align columns that contain int/float values
        truncate-with-ellipses: true   # if true, "..." added at end of truncated column headers/values
        status: ""                     # the status values to match for 'list runs' cmd
        report-rollup: false           # if primary metric is used to select run metrics to report (vs. last set of metrics)

        columns: ["run", "created:$do", "experiment", "queued", "job", "target", "repeat", "search", "status", 
            "tags.priority", "tags.description",
            "hparams.lr", "hparams.momentum", "hparams.optimizer", "hparams.steps", "hparams.epochs",
            "metrics.step", "metrics.epoch", "metrics.train-loss", "metrics.train-acc", 
            "metrics.dev-loss", "metrics.dev-acc", "metrics.dev-em", "metrics.dev-f1", "metrics.test-loss", "metrics.test-acc", 
            "duration", 
            ]

***************************
17. Job Reports
***************************

The **job-reports** section controls how the **list jobs** command formats its reports.  The primary control
revolves around the job columns, drawn from:

    - standard job properties (like **target** or **created**)
    - user assigned job tags (name must be prefixed by "tags.")

The properties of the **job-reports** section are:

    **sort**
        - specifies the job column used for sorting the jobs.  if not specified, this property default to "job".

    **reverse**
        - if set to True, a reverse sort is preformed (jobs are arranged in descending order of their sort column)

    **max-width**
        - the maximum width of a column in the report (in text characters)

    **precison** 
        - the default precision (number of decimal places) to use for formatting float values 

    **uppercase-hdr**
        - if True, the header names on the top and bottom of the report are uppercased.

    **right-align-numeric**
        - if True, number values are right-aligned in their columns
    
    **truncate-with-ellipses**
        - if True, column values that exceed the maximum width for the column are truncated with ellipses.

    **columns**
        - this is a list of column specifications to define the colums and their formatting for the report.  A column 
          specification can be as simple as the name of a column, but it can also include some customization.  Refer 
          to the `Columns in XT <columns>` topic for more information.

An example of the **job-reports** section::

    job-reports:
        sort: "name"                   # default column sort for experiment list (name, value, status, duration)
        reverse: false                 # if experiment sort should be reversed in order    
        max-width: 30                  # max width of any column
        precision: 3                   # number of fractional digits to display for float values
        uppercase-hdr  : true          # show column names in uppercase letters
        right-align-numeric: true      # right align columns that contain int/float values
        truncate-with-ellipses: true   # if true, "..." added at end of truncated column headers/values

        columns: ["job", "created", "started", "workspace", "experiment", "target", "nodes", "repeat", "tags.description", "tags.urgent", "tags.sad=SADD", "tags.funny", "low_pri", 
            "vm_size", "azure_image", "service", "vc", "cluster", "queue", "service_type", "search", 
            "job_status:$bz", "running_nodes:$bz", "running_runs:$bz", "error_runs:$bz", "completed_runs:$bz"]


***************************
18. Tensorboard
***************************

The **tensorboard** section controls how the **view tensorboard** command operates in XT.  The properties
for the **tensorboard** section are:

    **template**
        - the **template** property is a string that specifies how to name the Tensorboard log files from multiple runs.  It can include
        run column names (standard, hparams.*, metrics.*, tags.*) in curly braces along with normal characters outside thoses braces, 
        to build up log file names that enable easier filtering of runs within Tensorboard.

Here is an example **tensorboard** section::

    tensorboard::
        template: "{workspace}_{run_name}_{logdir}"

***************************
19. Script Launch Prefix
***************************

The **script-launch-prefix** section specify the shell command and arguments that should be used to run XT generated scripts on compute nodes, 
specified by the **box-class** property associated with the compute node.

The general format for a property of the **script-launch-prefix** section is:
    boxclass: commandstring

where:
    - **boxclass** is the class of the box (specified as a compute target property, or a box property, or hardcoded for to **linux** for 
    **aml** and **philly** services)

    - **commandstring** is a shell command and optional arguments used to run the scripts.  An example of a **commandstring** would be
        "bash --login" for linux systems.

Here is an example of a **script-launch-prefix** section::

    script-launch-prefix:
        # list cmds used to launch scripts (controller, run, parent), by box-class
        windows: ""
        linux: "bash --login"
        dsvm: "bash --login"
        azureml: "bash"
        philly: "bash --login"  

***************************
20. Azure Batch Images
***************************

The **azure-batch-images** section defines OS images for use in defining **batch** type compute targets.  The general 
format for an entry in this section is:

    imagename: {offer: "offername", publisher: "publishername", sku: "skuname", node-agent-sku-id: "skuid", version: "versionname"}

Where:
    - **imagename** is a user-defined name for the image being defined.
    - **offername** is the offer type of the Azure Virtual Machines Marketplace Image. For example, UbuntuServer or WindowsServer.
    - **publishername** is the publisher of the Azure Virtual Machines Marketplace Image. For example, Canonical or MicrosoftWindowsServer.
    - **skuname** is the SKU of the Azure Virtual Machines Marketplace Image. For example, 18.04-LTS or 2019-Datacenter.
    - **skuid** is the SKU of the Batch Compute Node agent to be provisioned on Compute Nodes in the Pool. 
    - **versionname** is the version of the Azure Virtual Machines Marketplace Image. A value of 'latest' can be specified to select the latest version of an Image.
    
More info about these properties is available in the Azure Batch 
docs `here <https://docs.microsoft.com/en-us/python/api/azure-batch/azure.batch.models.imagereference?view=azure-python>` and 
`here <https://docs.microsoft.com/en-us/python/api/azure-batch/azure.batch.models.virtualmachineconfiguration?view=azure-python>`.

Here is an example of a **azure-batch-images** section::

    azure-batch-images:
        # these are OS images that you can use with your azure batch compute targets (see [compute-targets] section above)
        dsvm: {offer: "linux-data-science-vm-ubuntu", publisher: "microsoft-dsvm", sku: "linuxdsvmubuntu", node-agent-sku-id: "batch.node.ubuntu 16.04", version: "latest"}
        ubuntu18: {publisher: "Canonical", offer: "UbuntuServer", sku: "18.04-LTS", node-agent-sku-id: "batch.node.ubuntu 18.04", version: "latest"}

***************************
21. Boxes
***************************

The **boxes** section defines a list of remote computers or Azure VMs that can be used as compute targets with XT.  The named boxes can also
be used directly by name in various XT utility commands.  

Requirements: each defined box needs to have ports 22 and port 18861 open for incoming messages, for configuration the box, and for communicating 
with the XT controller.


The general format for a box is:

    **boxname**: {address: **boxaddress**, os: **osname**, box-class: **boxclassname**, max-runs: **maxrunsvalue**, actions: **actionlist**}
    
Where:
    **boxname**
        - is the user-defined name for the box.

    **boxaddress** 
        - is an IP address (such as "52.224.239.149") or a username followed by "@" followed by an IP address, such as "jsmith@52.224.239.149". The 
        special $username can be used in this address (it will be replaced by the OS login of the user).

    **osname** 
        - is one of: **linux** or **windows**, representing the OS the box is running on.

    **boxclassname** 
        - is the user-defined name of a box-class, used in the **script-launch-prefixes** section.  This name is used to establish the script prefix
        to use when running scripts on the box.

    **maxrunsvalue** 
        - is maximum number of simultaneous XT runs allowed on the box.  this value is used by the XT controller to schedule runs on the box.

    **actionlist** 
        - is a list of actions (one of: **data**,  **model**) that XT will perform on the box, according to the properties of the **data** and **model** 
        sections defined in the config file.


Here is an example of a **boxes** section::

    boxes:
        local: {address: "localhost", os: "windows", box-class: "windows", max-runs: 1, actions: []}
        vm1: {address: "$username@52.170.38.14", os: "linux", box-class: "linux", max-runs: 1, actions: []}
        vm10: {address: "$username@52.224.239.149", os: "linux", box-class: "linux", max-runs: 1, actions: []}

***************************
22. Providers
***************************

The **providers** section defines the set of code providers active in XT, listed by their provider type.  

The current provider types in XT are:
    - command       (defines the set of commands available in XT)
    - compute       (defines the set of backend compute services available in XT)
    - hp-search     (defines the set of hyperparameter search algorithms available in XT)
    - storage       (defines the set of storage providers available in XT)

For each provider type, a dictionary of name/value pairs is specified.  The name is a user-defined name that may appear
elsewhere in the XT config file or command line options.  The value is a provider **code path**.

Here is an example of a **providers** section::

    providers:
        command: {
            "compute": "xtlib.impl_compute.ImplCompute", 
            "storage": "xtlib.impl_storage.ImplStorage", 
            "help": "xtlib.impl_help.ImplHelp", 
            "utility": "xtlib.impl_utilities.ImplUtilities"
        }

        compute: {
            "pool": "xtlib.backend_pool.PoolBackend", 
            "philly": "xtlib.backend_philly.Philly",
            "batch": "xtlib.backend_batch.AzureBatch",
            "aml": "xtlib.backend_aml.AzureML"
        }

        hp-search: {
            "dgd": "xtlib.search_dgd.DGDSearch",
            "bayesian": "xtlib.search_bayesian.BayesianSearch",
            "random": "xtlib.search_random.RandomSearch"
        }

        storage: {
            "azure-blob-21": "xtlib.store_azure_blob21.AzureBlobStore21",
            "azure-blob-210": "xtlib.store_azure_blob210.AzureBlobStore210",
            "store-file": "xtlib.store_file.FileStore",
        }

.. seealso:: 

    - :ref:`xt config command <config>` 
    - :ref:`Preparing a new project for XT <prepare_new_project>` 
    - :ref:`Hyperparameter Searching in XT <hyperparameter_search>` 
    - :ref:`Extensibility in XT <extensibility>` 

