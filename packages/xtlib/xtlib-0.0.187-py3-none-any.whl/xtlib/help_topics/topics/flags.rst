.. _flags:

=======================================
XT Root Flags and Options
=======================================

XT root flags are flags that are global (not associated with a particular command).  The must appear before any commands.

The current XT flags are:

    --console=value   (option)  Sets the level of console output (none, normal, diagnostics, detail)
    --help            (flag)    Shows an overview of XT command syntax
    --stack-trace     (flag)    Show the stack trace when an exception is raised
    --quick-start     (flag)    XT startup time is reduced (experimental)

Example::

    xt --console=diagnostics list runs

The above execute the XT 'list runs' command, with timing and diagnostic messages enabled.

