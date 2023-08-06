#
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.
#
# mongo_run_index.py: mongo functions that specialize in run_index management
import os
import sys
import time
import json
import copy
import uuid
import arrow
import shutil
import numpy as np
import logging

from xtlib import utils
from xtlib import errors
from xtlib import constants
from xtlib import file_utils

from xtlib.console import console

logger = logging.getLogger(__name__)

# status values
WAITING = "waiting_for_restart"
STARTED = "started"
RESTARTED = "restarted"
UNSTARTED = "unstarted"
COMPLETED = "completed"

class MongoRunIndex():
    '''
    Goal: a simple, reliable, atomic operation-based way to allocate the next child run 
    index for a node, with restart support.  Support both static and dynamic scheduling.

    Originally tried to use Mongo array and positional $ element support but:
        - $ projection for find_and_update() didn't work
        - using more than 1 array property to filter in find_and_update didn't work

    So, switched to current implementation, where each active run is its own document.
    '''
    def __init__(self, mongo, job_id, parent_run_name, node_id, new_session=True):
        self.mongo = mongo
        self.job_id = job_id
        self.parent_run_name = parent_run_name
        self.node_id = node_id
        self.schedule = self.get_job_property("schedule")

        if new_session:
            self.restart_runs_for_node()

    def restart_runs_for_node(self):
        '''
        non-atomic update of all active runs for this node: set to WAITING
        '''
        fd = {"_id": self.job_id, "active_runs.node_id": self.node_id, "$in": {"active_runs.status": [STARTED, RESTARTED]}}

        while True:
            # this will only update a single array entry at a time (using mongo 3.2)
            dd = self.mongo.mongo_db["__jobs__"].find_and_modify(fd , update={"$set": {"active_runs.$.status": WAITING}}, new=True)
            if not dd:
                break

    def get_next_child_run(self):
        if self.schedule == "static":
            entry = self.get_next_child_static()
        else:
            entry = self.get_next_child_dynamic()

        return entry
    
    def get_next_child_name(self):
         child_number = self.mongo.get_next_run_id(self.parent_run_name)
         run_name = self.parent_run_name + "." + str(child_number)
         return run_name

    def get_next_child_static(self):
        # look for a WAITING entry to restart
        entry = self.get_first_entry( filter={"node_id": self.node_id, "status": WAITING}, update={"status": RESTARTED})
        if not entry:

            # look for an UNSTARTED entry to start
            run_name = self.get_next_child_name()
            entry = self.get_first_entry( filter={"node_id": self.node_id, "status": UNSTARTED}, update={"status": STARTED, "run_name": run_name})

        return entry

    def get_next_child_dynamic(self):
        # look for a WAITING entry to restart
        entry = self.get_first_entry( filter={"status": WAITING}, update={"node_id": self.node_id, "status": RESTARTED})
        if not entry:

            # look for an UNSTARTED entry to start
            run_name = self.get_next_child_name()
            entry = self.get_first_entry( filter={"status": UNSTARTED}, update={"node_id": self.node_id, "status": STARTED, "run_name": run_name})

        return entry

    def get_job_property(self, prop_name):
        cursor = self.mongo.mongo_db["__jobs__"].find( {"_id": self.job_id}, {prop_name: 1})
        job_dd = list(cursor)[0] if cursor else None
        value = utils.safe_value(job_dd, prop_name)
        return value

    def get_first_entry(self, filter, update):
        # build filter dictionary for caller's nested properties
        fd = {"_id": self.job_id}

        for name, value in filter.items():
            key = "active_runs.{}".format(name)
            fd[key] = value

        # mongodb workaround: since $ projection operator not working with find_and_modify(),
        # we add a unique id (guid) so we know which element we have updated
        # guid = str(uuid.uuid4())
        # update["guid"] = guid

        # build update dictionary for caller's nested properties
        ud = {}
        for name, value in update.items():
            key = "active_runs.$.{}".format(name)
            ud[key] = value

        ar = self.get_job_property("active_runs")
        print("----------------------")
        # print("ar=", ar)
        print("filter:", fd)
        print("update:", ud)
        
        result = self.mongo.mongo_db["__jobs__"].find_and_modify(fd, update={"$set": ud}, fields={"active_runs": 1}, new=True)
        if result:
            active_runs = result["active_runs"]
            #result = next((ar for ar in active_runs if "guid" in ar and ar["guid"] == guid), None) 
            result = next((ar for ar in active_runs), None) 
        return result

        [   {'node_id': 'node0', 'run_index': 0, 'run_name': 'run9999.43', 'status': 'started'}, 
            {'node_id': 'node1', 'run_index': 1, 'run_name': 'run9999.44', 'status': 'started'}, 
            {'node_id': 'node2', 'run_index': 2, 'run_name': None, 'status': 'unstarted'}, 
            ...]


  