.. _columns:

========================================
Columns in XT 
========================================

 The columns shown in the *list runs* and *list jobs* commands can be customized using the *columns* property
 of the *run-reports*" and *job-reports* properties specified in the user's local XT config file.

The columns available for use in the *list runs* command come from 4 sources:

    - standard run columns (e.g., run, status, target, etc.)
    - hyperparameter name/value pairs logged by the ML app to XT (e.g. lr, optimizer, epochs, or hidden_dim)
    - metric name/value pairs logged by the ML app to XT (e.g. step, reward, epoch, train-loss, train-acc, test-loss, test-acc)
    - tag name/value pairs added to the run by the user 

The columns available for use in the *list jobs* command come from 2 sources:

    - standard job columns (e.g., job, status, target, etc.)
    - tag name/value pairs added to the job by the user 

.. note::
    A list of all available columns within the set of records returned by a reporting command can be seen by specifying the ``--available`` option on the command.

The *columns* property used to specify the columns shown by the associated command is a list of column spec strings.  A column
spec string consists of 3 parts:

    column-name     (required: name of the column to include)
    =header-name    (optional: the name shown in the Column Header, defaults to the column name) 
    :format-code    (optional: the python or XT formatting code to use in formatting values for the column)

Let's look at each of these in more detail:

    column-name: if the column in not a standard column, in needs to be prefixed by one of:
        *hparams.*, *metrics.*, *tags.* (e.g., hparams.lr, metrics.train_loss, tags.important)

    header-name: this is the text that will be shown as the header column in the reports

    format-code: this can be any of the following:
        - python formatting string (e.g., *.2f*, or ",")
        - $bz     (if value is zero, display as blanks)
        - $do     (display only the date portion of a datetime value)
        - $to     (display only the date portion of a datetime value)

  Examples:

    - To display the hyperparameter "discount_factor" as "discount", specify the column as  "discount_factor=factor".
    - To display the value for the "steps" metric with the thousands comma format, specify the column as "steps:,".  
    - To specify the column "train-acc" as "accuracy" with 5 decimal places, specify it as "train-acc=accuracy:.5f".  


.. seealso:: 

    - :ref:`list runs <list_runs>`
    - :ref:`list jobs <list_jobs>`
