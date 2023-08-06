.. _xt_features:

=======================================
XT Features
=======================================

Experiment Tools Library

XTlib is an API and command line tool for managing and scaling your ML experiments.  

Features:
    - Experiment Store (Azure Storage, Azure Cosmos DB)
        - centralized cloud storage of experiment logs, source files, results, and models
        - scalable reporting from summary data in Cosmos DB

    - Experiment Compute (local machines, VM's, Philly, Azure Batch, Azure ML)
        - before run, upload data/models to storage
        - start new experiment on specified machine(s)
        - run native or in docker containers
        - hyperparameter tuning runs (Grid search, Random search, DGD search)
        - log events with xtlib, Tensorboard
        - check or monitor status of run (various options include Tensorboard)
        - during/after runs, generate reports (filter, sort, specify columns)

The goal of XTLib is to enable you to effortlessly organize and scale your ML experiments.
Our tools offer an incremental approach to adoption, so you can begin realizing benifits immediatly.

XTLib provides an experiment STORE that enables you to easily track, compare, rerun, and share your ML experiments.  
The STORE consists of user-defined workspaces, each of which can contain a set of user-run experiments.  

In addition, XTLib also provides simple access to scalable COMPUTE resources so you can 
run multiple experiments in parallel and on larger computers, as needed.  With this feature, 
you can run your experiments on your local machine, other local computers or provised VMs to which you 
have aceess, or on 1 or more cloud computers, allocated on demand (Azure Batch).

