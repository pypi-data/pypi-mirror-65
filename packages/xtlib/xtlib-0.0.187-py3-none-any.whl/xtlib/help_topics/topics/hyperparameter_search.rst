.. _hyperparameter_search:

========================================
Hyperparameter Searching 
========================================

This page describes how to do Hyperparameter searching with XT.

The general steps involved in a hyperparameter search:
    - decide which hyperparameters you want to include in the search
    - decide the values you want to search to draw form (the value distribution)
    - specify the hyperparameters and their associated distributions
    - run your job using the `--repeat` and/or `--nodes` options to specify how many runs the search will use
    - analyze the results of your search

----------------------------------------------------------
Value distributions:
----------------------------------------------------------

When providing values to be searched over for a hyperparameter, you can specify them in 
these forms:

    - a comma-separated list of numbers
    - a comma-separated list of strings
    - the special symbol `RANDINT`
    - @disttype(value, value, ...)

The **@disttype** form of the above specifies a value distribution from the **hyperopt** library.  The following 
distribution types are supported::

    - choice(value, value, ...)
    - randint(upper)                      
    - uniform(low, high)
    - normal(mu, sigma)
    - loguniform(low, high)
    - lognormal(mu, sigma)
    - quniform(low, high, q)
    - qnormal(mu, sigma, q)
    - qloguniform(low, high, q)
    - qlognormal(mu, sigma, q)

------------------------------------------------
How to specify the hyperparams to search
------------------------------------------------

There are 2 ways to specify the hyperparameters and their associated values:
    - as special command line arguments to your ML script
    - using the `--hp-search` run option to specify a .yaml file 

-------------------------------------------------------------
Specifying hyperparameters in ML app's command line options
-------------------------------------------------------------

XT supports two basic forms of specifying hparam spaces to search as command line opions to your ML script:

    - name=[value list]
    - name=[$func(values)]

The "func" here must be one of the hyperopt search functions.

Here is an example of specifying a hyperparameter search in the ML script options::

    xt --target=philly --nodes=5 --repeat=10 run code\miniMnist.py --lr=[.01, .03, .05] --optimizer=[adam, sgd] --seed=[$randint()]

------------------------------------------------
Format of hp-search config file (.yaml)
------------------------------------------------

When specifying hyperparameters and their values distributions in a .yaml file, it should follow this form::

    hparams:
        name: value
        ...

Here is an example of a .yaml hp-config file::

        seed: $randint()
        lr: [.001, .003, .007]
        optimizer: ["adam", "sgd", "radam"]
        beta1: $uniform(.91, .99)

---------------------------------------------
Enabling a hyperparameter search
---------------------------------------------

A hyperparameter search is enabled when --search-type is set to a supported seach algorithm and 
a source of hyperparameter search spaces is found in one of the following:

    - the ML app's command line options
    - a hyperparameter search file is specifed with the --hp-config option

---------------------------------------------
Static searches
---------------------------------------------

Static searches are when the total list of search runs is generated before the job 
is submitted to the compute target.  Static searches are used under any of the following conditions:

    - search-type is **grid** or **random**  (and hyperparameter search is enabled)
    - the `--multi-commands` option has been specified

The `--multi-commands` option essentially allows users to generate and run a set of commands (distributed across the specified set of nodes) that comprise their own explict hyperparameter search.

Here are some examples of XT commands that result in static searches::

    - > xt --search-type=grid --hp-config=my_search_spaces.yaml run code\miniMnist.py
    - > xt --multi run code\multi_commands.txt

Static search run names are of the form "run" and a sequential number, assigned when the job is submitted.

---------------------------------------------
Dynamic searches
---------------------------------------------

Dynamic searches are when child runs are created dynamically on each compute node, when the XT controller is ready to run the next search.  Dynamic searches are used under any of the following conditions:

    - search-type is a value other than **grid** or **random** (and hyperparameter search is enabled)
    - the user has specified `--runs` or `--max-runs` with a number that indicates the ML app should be run multiple times on each node

When the `--runs` or `--max-runs` is specified and is greater then the number of specified nodes in the computer target, the user ML app command is repeated on each node, as needed, to 
meet the specified number of runs.

Here are some examples of XT commands that result in dynamic searches and child runs::

    - > xt --search-type=dgd --hp-config=my_search_spaces.yaml run code\miniMnist.py
    - > xt --runs=8 --nodes=2 --target=batch run code\miniMnist.py

Child run names are of the form:: 

    <parent run name>.<child number>   
    
The parent run name is the run name assigned for the command/node combination when the job is submitted.  The child 
number is the next sequential number for child runs assoiciated with the parent run, when the child run is created.

---------------------------------------------
Scaling the search runs
---------------------------------------------

There are several XT properties that work together to control the scaling of the search runs:

    - nodes  (compute target property)
        - the number of compute nodes to allocate for the search
        - defaults to 1 if not set

    - runs   (command line option only)
        - the total number of runs to be performed
        - defaults to 1*nodes if not set

    - concurrent    (hyperparameter-search property)
        - maximum number of concurrent runs per node 
        - defaults to 1

    - max-runs    (hyperparameter-search property)
        - limits the number of runs in search (e.g. grid search, where size of the search may be unknown to user)
        - defaults to -1 (not set) 

---------------------------------------------
How dynamic hyperparameter searching works
---------------------------------------------

On each node, the associated XT controller controls the scheduling of runs.  When a new run slot is available and an HP search run is at the top of the queue:
    - XT uses the HP search run as a template from which it creates a new **child run**
    - the HP search algorithm is given a history of past runs and the hyperparameter distributions to draw a sample from
    - the HP search algorithms returns a dictionary of hyperparameter name/value pairs
    - XT then applies the HP name/value pairs to the command line for the run and/or a config file for the run 
    - the child run is then launched
    - the HP search run (parent) is requeued if its `--repeat` count has not been exhausted

.. note:: 

    names for child runs are formed by taking the parent run name and appending a "." followed a sequential child number.  so, the first
    child of **run235** would be named **run235.1**.

An exception to the above is for the **grid search** algorithms.  For grid searches, all of the runs are pre-generated according the number of 
runs and then each node is given a static set of runs, each with an associated set of hyperparameter values.

---------------------------------------------
how to analyze results of a HP search
---------------------------------------------

There are many ways to analyze the results of a HP search, but XT provides 3 recommended tools:

    - the hyperparameter explorer (GUI tool)
    - the XT 'list runs' command
    - the XT 'plot' command

For example, to find the best performing runs in a hyperparamete search whose job id is **job2338** and whose 
primary metric is **test-acc**, you can use the command::

    xt list runs --job=job2338 --sort=metrics.test-acc

To compare the training curve for some runs of interest (say, run23.1 thru run 23.10), we can use the command::

    xt plot run23.1-run23.10 train-acc, test-acc --x=epoch --break=run --layout=2x5
    

.. seealso:: 

    - `the hyperopt library <http://hyperopt.github.io/hyperopt/>`_
    - :ref:`XT controller<xt_controller>`
    - :ref:`explore command <explore>`
    - :ref:`list runs command <list_runs>`
    - :ref:`plot command <plot>`
    - :ref:`XT config file <xt_config_file>`

