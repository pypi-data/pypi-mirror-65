.. _filters:

======================================
Filters in XT 
======================================

Filters are used for showing only records of interest in the *list runs* and *list jobs* commands.

The ``--filter`` option can be used to show a subset of all runs in the workspace.  It can be specified 
multiple times, effectively combining the expressions with an implicit *and* operator.

The general form of the filter is:

    <column> <relational operator> <value>

The *column* of a filter can be a standard run or job column name, or a custom property name prefixed by one of:

    - hparams.      (e.g., *hparams.lr* refers to the learning rate hyperparameter logged by the user ML app to XT)
    - metrics.      (e.g., *metrics.train-loss* refers to the training loss metric logged by the user ML app to XT)
    - tags.         (e.g., *tags.category* refers to the tag "category" added to runs or jobs by the user)

.. note::
    A list of all available columns within the set of records returned by a reporting command can be seen by specifying the ``--available`` option on the command.

The *operator* of a filter can be one of following:

        - one of the python relational operators: <, <=, >, >=, ==, !=
        - =           (an alternate way to specify the == operator)
        - <>          (an alternate way to specify the != operator)
        - \:regex\:     (treats the value as a regular expression in matching the specified column on each record)
        - \:exists\:    (the existance of the column will be matched to each record according to the specified true/false value)
        - \:mongo\:     (the value of this filter will be interpreted as a mongo-db filter expression)

The *value* of a filter can take the form of:

    - integers
    - floats
    - strings
    - $true    (replaced with a python True value)
    - $false   (replaced with a python False value)
    - $none    (replaced with a python None value)
    - $empty   (replaced with a python empty string value)

Filter Examples:
        
    - To show runs where the train-acc metric is > .75, you can specify: ``--filter="train-acc>.75"``
    - To show runs where the hyperparameter lr was == .03 and the test-f1 was >= .95, you can specify the filter option twice: ``--filter="lr=.03"  --filter="test-f1>=.95"``
    - To show runs where the repeat is set to something other than None, ``--filter="repeat!=$none"``
   
.. seealso:: 

    - :ref:`list runs <list_runs>`
    - :ref:`list jobs <list_jobs>`
