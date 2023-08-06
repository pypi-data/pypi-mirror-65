.. _cmd_options:

======================================
XT command options
======================================

You can use two methods to customize behavior of XT commands:
    - Edit your local XT config file to change default XT config file properties
    - Use command line options to override default and local config file properties 
    
------------------------------------------
Types of XT command line options
------------------------------------------

There are 3 types of XT command line options, along with rules for their placement within the XT command:
    - root options (these apply to any command and must appear before the command)
    - run options (these option apply to the **run** command and must appear before the **run** keyword)
    - normal command options (these are command-specific options for command other than the **run** command, and must appear after the command keyword(s))

The syntax for the XT **run** command is:

   - **xt** [ <root options> ] [ <run options> ] **run** <script file> [ <script arguments> ]

The syntax for all other XT commands is:

   - **xt** [ <root options> ] <command keywords> <command arguments> <command options>

-------------------------------------
Specifying options
-------------------------------------

For specifying options, the general syntax is:

    - `<name>=<value>`

**Note:** all option names begin with two dashes (`\-\-`)

A subset of the options are  **flags**, which are options that don't require an `=<value>` part.  When flags are specified by their name only, they are set to the value **true**.  Flags can also be set explictly to an *on* value (**on**, **true**, **1**) or an off value (**off**, **false**, **0**).

Option values types:
    - flag            (as described above)
    - string          (quoted string; can be unquoted if value is a simple token)
    - int             (integer value)
    - float           (floating point number)
    - bool            (**true** or **false** value)
    - string list     (a comma separated list of unquoted strings)
    - number list     (a comma separated list of numbers - can be mixture of ints and floats)
    - prop_op_value   (a triple of a property name, a relational operator, and a string or number value, with no spaces between the parts)

------------------------------
Specify string values 
------------------------------

XT is a command line program and gets the majority of its input from the OS command line shell. This means that the command input XT receives is restricted: 
    - on Linux, single and double quotes are removed 
    - on Windows, double quotes are removed 

For these reasons, we recommend the following when specifying string values to XT::

    - for strings that consist of a single token, no quotes are needed::

        - title=Accuracy

    - on Windows, you can use {} or single quotes::
        
        --title={this is my title}
        --title='this is my title'

    - on Linux, you can use {}, nested quotes, or escaped quotes::

        --title={this is my title}
        --title="'this is my title'"
        --title=\'this is my title\'

-----------------------------
Root options
-----------------------------

The root options (**console**, **stack-trace**, etc.) must appear immediately after the **xt** name.  These options apply to all XT commands and control things like how much output is displayed during command execution.

-----------------------------
Run options
-----------------------------

These options for the run command are just like any XT option, except for their required position in the command.


.. seealso:: 

    - :ref:`XT Config file <xt_config_file>`
    - :ref:`XT Root Flags and Options <flags>`
    - :ref:`XT run command <run>`
    - :ref:`XT Filters <filters>`
