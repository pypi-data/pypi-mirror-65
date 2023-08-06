.. _login:

========================================
XT Login
========================================

XT needs to retreive service keys so that it can access the various services defined in the XT config file
on behalf of the user.  These keys are stored in an Azure Key Vault (also defined in the XT config file).

The first time a user runs XT in a new OS session, they will be redirected to the browser for Azure authentication
of their selected identify.  

Once the authentication has suceessfully completed, the keys are cached in memory
for the duration of the OS session.  This caching can be cleared at any time using the **xt clear credentials** command.

.. seealso:: 

    - :ref:`clear credentials command<clear_credentials>`
    - :ref:`XT config file<xt_config_file>`







