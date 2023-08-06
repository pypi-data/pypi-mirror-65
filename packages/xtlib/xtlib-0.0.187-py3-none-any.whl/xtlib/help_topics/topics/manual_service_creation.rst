.. _manual_service_creation:

========================================
Manually Creating XT Services
========================================

XT needs a set of cloud services to run jobs on cloud computers, log stats, and store experiment artifacts. 

Normally, the **xt create team** command can be used to create an template for the services. This page documents
how to manually create the services without using the template.  It was written before the template option was 
created and may be removed in the future.

In the following steps, you will manually create a set of 6 Azure services, which should take about 30 minutes
to complete.

--------------------------
The Azure Services for XT
--------------------------

There are 6 services associated with an XT team:

    - Storage               (provides cloud storage for your experiments)
    - Mongo DB              (provides fast Database access to the stats and metrics of your experiments)
    - Key Vault             (provides secure storage of the credentials for your services)
    - Azure Batch           (a general compute service that offers on-demand Virtual Machines)
    - Azure ML              (a compute services designed for Machine Learning on VMs)
    - Container Registry    (provides storage for docker images)

The below steps show you how to create these services from the Azure Portal.  Mostly, we will
be relying on the default settings when creating these services, except as noted below. 


--------------------------------------------
Creating the Storage Service
--------------------------------------------

1. Select a simple, short team name for your XT team, without any special punctuation.  For example, "phoenix".

2. In the Azure Portal::

    - select the "+ Create a Resource" button
    - search for "Storage Account"
    - select the Microsoft "Storage account - blob, file, table, queue" item
    - click on "Create"

3. For the Create dialog::

    - for "Subscription", select the Azure Subscription ID that you want the service billed to
    - for "Resource group", we suggest you create a NEW group named the same as your XT team
    - for "Storage account name", we recommend your team name, followed by "storage" (e.g., phoenixstorage)
    - for "Location", choose a location that is close to your team's primary location.  you will use this same location for all of your XT services.
    - for "Account kind", choose "Storage (general purpose v1)" 
    - the defaults for the remaining options all work fine, so click on "Review + create"
    - click on "create"

The Portal should respond with "Deployment under way...".  While the service is being deployed (takes about 5 minutes), you can continue with the below steps.

--------------------------------------------
Creating the Mongo DB Service
--------------------------------------------

1. In the Azure Portal::

    - select the "+ Create a Resource" button
    - search for "Cosmos"
    - select the Microsoft "Azure Cosmos DB" item
    - click on "Create"

2. For the Create dialog::

    - for "Subscription", select the Azure Subscription ID that you want the service billed to
    - for "Resource group", we suggest you use your team group
    - for "Account name", we recommend your team name, followed by "mongodb" (e.g., phoenixmongodb)
    - for "API", choose "Azure Cosmos DB for MongoDB API"
    - for "Location", choose the same location used for your Storage service
    - for "Version", select "3.2"
    - the defaults for the remaining options all work fine, so click on "Review + create"
    - click on "create"

The Portal should respond with "Deployment under way...".  While the service is being deployed (takes about 5 minutes), you can continue with the below steps.


--------------------------------------------
Creating the Key Vault Service
--------------------------------------------

1. In the Azure Portal::

    - select the "+ Create a Resource" button
    - search for "key vault"
    - select the Microsoft "Key Vault" item
    - click on "Create"

2. For the Create dialog::

    - for "Subscription", select the Azure Subscription ID that you want the service billed to
    - for "Resource group", we suggest you use your team group
    - for "Key vault name", we recommend your team name, followed by "keyvault" (e.g., phoenixkeyvault)
    - for "Region", choose the same location used for your Storage service
    - the defaults for the remaining options all work fine, so click on "Review + create"
    - click on "create"

The Portal should respond with "Deployment under way...".  While the service is being deployed (takes about 5 minutes), you can continue with the below steps.


--------------------------------------------
Creating the Azure Batch Service
--------------------------------------------

1. In the Azure Portal::

    - select the "+ Create a Resource" button
    - search for "batch service"
    - select the Microsoft "Batch Service" item
    - click on "Create"

2. For the Create dialog::

    - for "Subscription", select the Azure Subscription ID that you want the service billed to
    - for "Resource group", we suggest you use your team group
    - for "Account name", we recommend your team name, followed by "batch" (e.g., phoenixbatch)
    - for "Location", choose the same location used for your Storage service
    - the defaults for the remaining options all work fine, so click on "Review + create"
    - click on "create"

The Portal should respond with "Deployment under way...".  While the service is being deployed (takes about 5 minutes), you can continue with the below steps.

--------------------------------------------
Creating the Azure ML Service
--------------------------------------------

1. In the Azure Portal::

    - select the "+ Create a Resource" button
    - search for "machine learning"
    - select the Microsoft "Machine Learning" item
    - click on "Create"

2. For the Create dialog::

    - for "Workspace name", we recommend your team name, followed by "aml" (e.g., phoenixaml)
    - for "Subscription", select the Azure Subscription ID that you want the service billed to
    - for "Resource group", we suggest you use your team group
    - for "Location", choose the same location used for your Storage service
    - for "Workspace edition", choose "Enterprise"
    - the defaults for the remaining options all work fine, so click on "Review + create"
    - click on "create"

The Portal should respond with "Deployment under way...".  While the service is being deployed (takes about 5 minutes), you can continue with the below steps.

--------------------------------------------
Creating the Container Registry Service
--------------------------------------------

1. In the Azure Portal::

    - select the "+ Create a Resource" button
    - search for "registry"
    - select the Microsoft "Container Registry" item
    - click on "Create"

2. For the Create dialog::

    - for "Registry name", we recommend your team name, followed by "registry" (e.g., phoenixregistry)
    - for "Subscription", select the Azure Subscription ID that you want the service billed to
    - for "Resource group", we suggest you use your team group
    - for "Location", choose the same location used for your Storage service
    - the defaults for the remaining options all work fine, so click on "Review + create"
    - click on "create"

The Container Registry is normally created instantly and the Portal navigates to the newly created service.

.. seealso:: 

    - :ref:`Creating XT Services  <creating_xt_services>`
    - :ref:`create team cmd <create_team>`
    - :ref:`Preparing A New Project <prepare_new_project>`
