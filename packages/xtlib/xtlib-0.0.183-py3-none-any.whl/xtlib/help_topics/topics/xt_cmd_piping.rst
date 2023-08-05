.. _xt_cmd_piping:

========================================
XT Command Piping
========================================

Currently, 2 XT commands have powerful query options: *xt list runs* and *xt_list_jobs*.  There 
are several other XT commands that accept a list of runs or jobs, but don't have the same query options.

To help bridge this gap, you can use command line piping (in Windows or Linux command lines) to pipe runs or jobs
matched by a query command to another XT command.  

For example, supposed you wanted to take the top 15 highest scoring runs and tag them with the tag "top15".  One 
way to do this is do issue a "list runs" command with the needed filters and sorting, and then copy/pase (or read and type) the 
run names into the "set tags" command.

With XT command piping you can do this is one step:

        .. code-block::

            > xt list runs --sort=metrics.test-acc --last=15 | xt set tags $ top15

In the above *xt set tags* command, note that we have specified a '$' in the location where we want the run names 
from the first command to be inserted.  This is required; without the '$', names from the incoming command will be ignored.

For a second example, suppose you wanted to include the most recently completed 10 runs in a set of plots.  This can be done with:

        .. code-block::

            > xt list runs --status=completed --last=10 | xt plot $ train-acc, test-acc --layout=2x5

            

