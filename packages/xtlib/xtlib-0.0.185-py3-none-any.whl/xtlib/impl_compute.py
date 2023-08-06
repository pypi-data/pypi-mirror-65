#
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.
#
# impl_compute.py: implementation of XT compute commands
import os
import sys
import time
import datetime
import numpy as np 

from .client import Client
from .runner import Runner
from .console import console
from xtlib.storage.store import Store
from .cmd_core import CmdCore
from .impl_base import ImplBase
from xtlib.attach import Attach
from .backends import backend_aml 
from xtlib.xt_client import XTClient
from .helpers.scanner import Scanner
from .qfe import inner_dispatch, get_dispatch_cmd, Dispatcher
from .qfe import command, argument, option, flag, root, clone
from .qfe import hidden, example, command_help, keyword_arg

from xtlib import utils
from xtlib import errors
from xtlib import capture
from xtlib import pc_utils
from xtlib import file_utils
from xtlib import job_helper
from xtlib import run_helper
from xtlib import box_information
'''
This module implements the following commands:

run creation:
     - xt <filename> <app args>                 # run file (.sh, .bat, .py) under control to xt on specified box/pool
     - xt python <filename> <app args>          # run python on file 
     - xt run app <app args>                    # run the app 
     - xt docker run <args>                     # run the specified docker image 

run control/information:
     * xt start tensorboard [ <name> ]          # start tensorboard process for specified box or run
     * xt stop tensorboard [ <name> ]           # stop tensorboard for specified box or run
     * xt collect logs <log path> <runs>        # copy log files from specified runs (on blob store) to grok server

     - xt monitor <name>                        # create a jupyter notebook to monitor an Azure ML run
     - xt attach <name>                         # attach output of run to console (use ESC to detach)
     - xt status                                # display the controller status on the specified box (flags: mirror, tensorboard, controller)
     - xt rerun <name> [ <app args> ]           # rerun the specified run with optional new cmd args
     - xt kill controller                       # terminates the controller on the specified box

     - xt kill runs [ <name list> ]             # terminates the specifed runs or (--boxes, --job, --workspace)

    (*) not yet completed
'''     
class ImplCompute(ImplBase):
    def __init__(self, config, store=None):
        super(ImplCompute, self).__init__()
        self.config = config
        self.store = store if store else Store(config=config)
        self.client = Client(config, store, None)
        self.core = CmdCore(self.config, self.store, self.client)
        self.client.core = self.core
        
        #self.azure_ml = backend_aml.AzureML(self.core)

    def is_aml_ws(self, ws_name):
        return False  # self.azure_ml.does_ws_exist(ws_name)

    def validate_and_add_defaults(self, cmd, args):
        dispatcher = Dispatcher({}, self.config)
        full_args = dispatcher.validate_and_add_defaults_for_cmd(cmd, args)

        return full_args

    #---- VIEW STATUS command ----
    @argument(name="run-name", required=False, help="return status only for the specified run")

    @option("cluster", help="the name of the cluster to be viewed")
    @option("vc", default="all", help="the name of the virtual cluster")
    @option("status", help="only show jobs with a matching status")
    @option("max-finished", default=100, type=int, help="the maximum number of finished jobs to show")
    @flag("tensorboard", help="shows the status of tensorboard processes on the box")
    @flag("mirror", help="shows the status of mirror processes on the box")
    @flag("monitor", help="continually monitor the status")
    @flag("auto-start", help="when specified, the controller on the specified boxes will be started when needed")
    @flag("queued", help="when specified, only queued runs are reported")
    @flag("active", help="when specified, only active runs are reported")
    @flag("completed", help="when specified, only completed runs are reported")
    @option("escape-secs", type=int, help="how many seconds to wait before terminating the monitor loop")
    @option("target", default="$xt-services.target", help="the name of the compute target to query for status")
    @option("username", default="$general.username", type=str, help="the username used to filter runs")
    @option("workspace", default="$general.workspace", type=str, help="the workspace used to filter runs")
    @option(name="job", help="query all boxes defined for the specified job")
    @example(task="show the status of runs on the local machine", text="xt view status")
    @example(task="show the status of run68", text="xt view status curious/run68")
    @command(kwgroup="view", help="displays the status of the specified compute target")
    def view_status(self, run_name, tensorboard, mirror, target, workspace, job, monitor, escape_secs, auto_start, 
            username, active, cluster, vc, status, max_finished, queued, completed):
        '''The view status command is used to display status information about the XT controller process
        running on a box (or pool of boxes).  
        
        The'tensorboard' flag is used to return information about the running tensorboard-related processes.
        The 'mirror' flag is used to return information about Grok server mirroring processes.
        '''

        if tensorboard:
            run_name = "tensorboard"
        elif mirror:
            run_name = "mirror"
        elif run_name:
            run_name, workspace = run_helper.parse_run_name(workspace, run_name)

        if not queued and not active and not completed:
            # if none of these are specified, it implies we want to see all info
            stage_flags = "queued, active, completed"
        else:
            # at least one flag was specified, so logically "or" them
            stage_flags = ""
            if queued:
                stage_flags += "queued, "
            if active:
                stage_flags += "active, "
            if completed:
                stage_flags += "completed, "

        # active = self.config.get("general", "active")
        # queued = self.config.get("general", "queued")

        if target == "all":
            # enumerate all registered targets and call their view_status method
            targets = self.config.get_targets()

            for target in targets:
                print("\nSTATUS for target '{}':".format(target))

                backend = self.core.create_backend(target, username=username)
                backend.view_status(run_name, workspace, job, monitor, escape_secs, auto_start, 
                    stage_flags, status, max_finished)
        else:
            # view status on a single target
            backend = self.core.create_backend(target, username=username)
            backend.view_status(run_name, workspace, job, monitor, escape_secs, auto_start, 
                stage_flags, status, max_finished)

    
    #---- ATTACH command ----
    @argument(name="run-name", help="The name of the run to attach")
    @option("workspace", default="$general.workspace", type=str, help="the workspace that the run resides within")
    @option("escape", type=int, help="the number of seconds to remain attached")
    @example(task="attach to run68 in the current workspace", text="xt attach run68")
    @command(help="attaches the streaming output of the specified run to the console")
    def attach(self, workspace, run_name, escape):
        run_name, actual_ws = run_helper.parse_run_name(workspace, run_name)
        is_aml = self.is_aml_ws(actual_ws)

        if is_aml:
            self.azure_ml.attach_to_run(actual_ws, run_name)
        else:
            #self.client.monitor_attach_run(actual_ws, run_name, escape=escape)
            cs, box_secret = run_helper.get_client_cs(self.core, actual_ws, run_name)
            if not cs:
                console.print("could not find info for run: {}/{}".format(actual_ws, run_name))
            else:
                with XTClient(self.config, cs, box_secret) as xtc:
                    attach = Attach(xtc)
                    attach.monitor_attach_run(actual_ws, run_name, escape=escape)

                    # xtc.connect()
                    # attach.simple_attach(actual_ws, run_name)

    #---- MONITOR command ----
    @argument(name="run-name", help="The name of the run to attach")
    @option("workspace", default="$general.workspace", type=str, help="the workspace that the run resides within")
    @example(task="monitor the AML run run544 from exper5", text="xt monitor exper5.run544")
    @command(help="creates a Python notebook to monitor the specified Azure ML run")
    def monitor(self, workspace, run_name):
        if not self.is_aml_ws(workspace):
            errors.combo_error("the monitor command is only supported for Azure ML runs")

        run_name, actual_ws = run_helper.parse_run_name(workspace, run_name)

        fn = self.azure_ml.make_monitor_notebook(actual_ws, run_name)
        dir = os.path.dirname(fn)
        #console.print("jupyter notebook written to: " + fn)
        monitor_cmd = "jupyter notebook --notebook-dir=" + dir
        console.print("monitoring notebook created; to run:")
        console.print("  " + monitor_cmd)

    #---- COLLECT LOGS command ----
    @argument(name="run-names", type="str_list", help="comma-separated list of run names")
    @argument(name="log_path", help="the wildcard path of the log files to collect")
    @option("workspace", default="$general.workspace", type=str, help="the workspace that the runs reside within")
    @example(task="collect the log files matching *tfevent* from run68", text="xt collect logs run68, run69 *tfevent* --work=curious")
    @command(help="copy log files from specified runs (on blob store) to grok server")
    def collect_logs(self, workspace, run_names, log_path):

        run_names, actual_ws = run_helper.parse_run_list(self.store, workspace, run_names)
        if len(run_names) == 0:
            self.store_error("No matching runs found")

        grok_server = None   # self.config.get("logging", "grok-server")

        count = 0
        for run_name in run_names:
            count += self.core.collect_logs_for_run(actual_ws, run_name, log_path, grok_server)

        console.print("{} log file collected to grok server: {}".format(count, grok_server))

    #---- START TENSORBOARD command ----
    @example(task="start tensorboard curious/run68", text="xt start tensorboard curious/run68")
    @command(help="start tensorboard for the specified run")
    def start_tensorboard(self):
        console.print("start_tensorboard cmd goes here...")

    #---- STOP TENSORBOARD command ----
    @example(task="stop tensorboard curious/run68", text="xt stop tensorboard curious/run68")
    @command(help="stop tensorboard for the specified run")
    def stop_tensorboard(self):
        console.print("stop_tensorboard cmd goes here...")

    def get_info_for_run(self, ws, run_name):
        cmdline = None
        box_name = None
        parent_name = None
        node_index = None

        records = self.store.get_run_log(ws, run_name)

        # get cmdline
        for record in records:
            if record["event"] == "cmd":
                dd = record["data"]
                cmdline = dd["cmd"]
                xt_cmdline = dd["xt_cmd"]
                break

        for record in records:
            if record["event"] == "created":
                dd = record["data"]
                box_name = dd["box_name"]
                node_index = dd["node_index"]
                # looks like we no longer log the parent name
                #parent_name = dd["parent_name"]
                parent_name = run_name.split(".")[0] if "." in run_name else None
                break

        return cmdline, xt_cmdline, box_name, parent_name, node_index

    #---- RERUN command ----
    @argument("run-name", help="the name of the original run")
    @option("workspace", default="$general.workspace", type=str, help="the workspace that the runs reside within")
    @option("response", default=None, help="the automatic response to be used to supplement the cmd line args for the run")
    @example(task="rerun run74", text="xt rerun curious/run74")
    @command(help="submits a run to be run again")
    def rerun(self, run_name, workspace, response):
        # NOTE: validate_run_name() call must be AFTER we call process_named_options()
        run_name, workspace = run_helper.parse_run_name(workspace, run_name)

        # extract "prompt" and "args" from cmdline
        cmdline, xt_cmdline, box_name, parent_name, node_index = self.get_info_for_run(workspace, run_name)

        #console.print("cmdline=", cmdline)
        prompt = ""

        if xt_cmdline:
            args = "  " + xt_cmdline
        else:
            # legacy run; just use subset of xt cmd
            args = "  xt " + cmdline

        console.print("edit/accept xt cmd for {}/{}".format(workspace, run_name))
        if response:
            # allow user to supplement the cmd with automation
            if "$cmd" in response:
                response = response.replace("$cmd", args)
            console.print(response)
        else:
            response = pc_utils.input_with_default(prompt, args)

        # keep RERUN cmd simple by reusing parse_python_or_run_cmd()
        full_cmd = response.strip()
        #console.print("  new_cmd=" + full_cmd)
        if not full_cmd.startswith("xt "):
            errors.syntax_error("command must start with 'xt ': {}".format(full_cmd))

        tmp_dir = file_utils.make_tmp_dir("rerun_cmd")
        job_id = self.store.get_job_id_of_run(workspace, run_name)
        capture.download_before_files(self.store, job_id, workspace, run_name, tmp_dir, silent=True)
         
        # move to tmp_dir so files get captured correctly
        prev_cwd = os.getcwd()
        os.chdir(tmp_dir)

        try:
            # recursive invoke of QFE parser to parse command (orginal + user additions)
            args = full_cmd.split(" ")
            args = args[1:]    # drop the "xt" at beginning
            inner_dispatch(args, is_rerun=True)
        finally:
            # change back to original dir
            os.chdir(prev_cwd)

    #---- STOP CONTROLLER command ----
    @option("box", default="local", type=str, help="the name of the box")
    @option("pool", type=str, help="the name of the pool of boxes")
    @example(task="stop the controller process on the local machine", text="xt stop controller")
    @example(task="terminate the controller process on box 'vm10'", text="xt stop controller --box=vm10")
    @command(help="stops the XT controller process on the specified box")
    def stop_controller(self, box, pool):

        boxes, pool_info, service_type = box_information.get_box_list(self.core, box=box, pool=pool)
        #console.print("boxes=", boxes, ", is_azure_pool=", is_azure_pool)

        self.client.cancel_controller_by_boxes(boxes)

    def print_cancel_results(self, cancel_results_by_boxes, run_summary=None, is_aml=False):
        #console.print("cancel_results_by_boxes=", cancel_results_by_boxes)

        if run_summary:
            console.print(run_summary)

        if not cancel_results_by_boxes:
            console.print("no matching runs found")
            return
            
        for box_name, results in cancel_results_by_boxes.items():

            # show box name as upper to emphasize where kill happened
            box_name = box_name.upper()

            if not run_summary:
                # if is_aml:
                #     console.print("Azure ML:")
                # else:
                #     console.print("box {}:".format(box_name))
                console.print(box_name + ":")

            if not results:
                console.print("  no matching active runs found")
            else:
                for result in results:
                    if not result:
                        continue

                    #console.print("result=", result)
                    ws_name = result["workspace"]
                    run_name = result["run_name"]
                    exper_name = result["exper_name"] if "exper_name" in result else None
                    killed = result["cancelled"]
                    status = result["status"]
                    before_status = result["before_status"]
                        
                    run_name = exper_name + "." + run_name if exper_name else run_name
                    full_name = ws_name + "/" + run_name

                    if killed:
                        console.print("  {} cancelled (status was '{}')".format(full_name, before_status))
                    else:
                        console.print("  {} has already exited, status={}".format(full_name, status))

    def get_runs_by_box(self, run_names, workspace=None):
        run_names, actual_ws = run_helper.parse_run_list(self.store, workspace, run_names)

        mongo = self.store.get_mongo()
        fields_dict = {"box_name": 1, "compute": 1, "ws": 1, "run_name": 1}

        filter_dict = {}
        filter_dict["run_name"] = {"$in": run_names}

        box_records = mongo.get_info_for_runs(actual_ws, filter_dict, fields_dict)

        # group by box_name
        runs_by_box = {}

        for br in box_records:
            if "box_name" in br:
                box_name = br["box_name"] 
                if not box_name in runs_by_box:
                    runs_by_box[box_name] = []
                runs_by_box[box_name].append(br)

        return runs_by_box

    #---- CANCEL RUN command ----
    @argument("run-names", type="str_list", help="the list of run names to cancel")
    @option("workspace", default="$general.workspace", type=str, help="the workspace that contains the runs")
    @example(task="cancel run103 in curious workspace", text="xt cancel runs run103 --work=curious")
    @command(kwgroup="cancel", help="cancels the specified run(s)")
    def cancel_run(self, run_names, workspace):

        runs_by_box = self.get_runs_by_box(run_names, workspace)

        cancel_results_by_box = {}

        for box_name, runs in runs_by_box.items():
            first_run = runs[0]

            ws_name = first_run["ws"]
            # = [ws_name + "/" + run["run_name"] for run in runs]
            run_names = [run["run_name"] for run in runs]
            compute = first_run["compute"] if "compute" in first_run else "pool"    # some legacy support

            backend = self.core.create_backend(compute)
            cancel_results = backend.cancel_runs_by_names(workspace, run_names, box_name)

            cancel_results_by_box[box_name] = cancel_results

        self.print_cancel_results(cancel_results_by_box)

    #---- CANCEL JOB command ----
    @argument("job", help="the name of the job to cancel")
    @example(task="cancel all runs in job3125", text="xt cancel job job3125")
    @command(kwgroup="cancel", kwhelp="cancels active runs, specified by name, job, or target", help="cancels the specified job and its active or queued runs")
    def cancel_job(self, job):

        mongo = self.store.get_mongo()

        filter_dict = {}
        filter_dict["job_id"] = {"$in": [job]}
        fields_dict = None    # get entire document  #{"compute": 1}

        cursor = mongo.get_info_for_jobs(filter_dict, fields_dict)
        records = list(cursor)
        if len(records) != 1:
            errors.store_error("unknown job_id={}".format(job))

        first = records[0]
        compute = first["compute"]
        runs_by_box = first["runs_by_box"]

        backend = self.core.create_backend(compute)
        compute_info = self.config.get_compute_def(compute)
        service_name = compute_info["service"]

        cancel_results_by_box = backend.cancel_runs_by_job(job, runs_by_box)

        # if service_name == "pool":
        #     # feed backend 1 box at a time
        #     for box_name in runs_by_box:
        #         cancel_results = backend.cancel_runs_by_job(job, box_name)
        #         cancel_results_by_group[box_name] = cancel_results
        # else:

        self.print_cancel_results(cancel_results_by_box)

    #---- CANCEL ALL command ----
    @argument("target", help="the name of the compute target whose runs will be cancelled")
    @hidden("username", default="$general.username", help="the username to log as the author of this run")
    @example(task="cancel all runs for current user on Philly", text="xt cancel all philly")
    @command(kwgroup="cancel", kwhelp="cancels active runs, specified by name, job, or target", help="cancels all queued/active runs on the specified compute target")
    def cancel_all(self, target, username):

        backend = self.core.create_backend(target, username)
        cancel_results_by_box = {}

        compute_info = self.config.get_compute_def(target)
        service_name = compute_info["service"]

        if service_name == "pool":
            boxes = compute_info["boxes"]
            for box_name in boxes:
                cancel_results = backend.cancel_runs_by_user(box_name)
            
                cancel_results_by_box[box_name] = cancel_results
        else:
            cancel_results = backend.cancel_runs_by_user(None)
            cancel_results_by_box[target] = cancel_results

        self.print_cancel_results(cancel_results_by_box)

    #---- RESTART CONTROLLER command ----
    @argument("job-id", help="the name of the job whose node will be restarted")
    @option("node-index", default=0, help="the 0-based node index to be restarted")
    @option("delay", type=float, default=15, help="the number of seconds to delay after cancelling runs and before restarting the controller")
    @example(task="simulate a service-level restart on job23, node 1", text="xt restart controller job23 --node=1")
    @command(help="uses the XT controller to simulate a service-level restart on the specified job/node")
    def restart_controller(self, job_id, node_index, delay):

        result = None

        # get the connection string for the job/node
        cs_plus = job_helper.get_client_cs(self.core, job_id, node_index)
        cs = cs_plus["cs"]
        box_secret = cs_plus["box_secret"]

        with XTClient(self.config, cs, box_secret) as xtc:
            if xtc.connect():
                result = xtc.restart_controller(delay)

        if result:
            console.print("controller restarted")
        else:
            console.print("could not connect to controller: ip={}, port={}".format(cs["ip"], cs["port"]))

    #---- VIEW CONTROLLER STATUS command ----
    @argument("job-id", help="the name of the job whose node will be restarted")
    @option("node-index", default=0, help="the 0-based node index to be restarted")
    @example(task="view the status of the 2nd node running job100", text="xt view controller status job100 --node=1")
    @command(kwgroup="view", help="uses the XT controller to view the status of the specified job/node")
    def view_controller_status(self, job_id, node_index):

        # get the connection string for the job/node
        cs_plus = job_helper.get_client_cs(self.core, job_id, node_index)
        cs = cs_plus["cs"]
        box_secret = cs_plus["box_secret"]
        
        job = cs_plus["job"]
        compute = job["compute"]

        if not cs:
            console.print("could not find controller for job={}".format(job_id))
        else:
            stage_flags="queued, active, completed"

            with XTClient(self.config, cs, box_secret) as xtc:
                if xtc.connect():
                    elapsed = xtc.get_controller_elapsed()
                    xt_version = xtc.get_controller_xt_version()
                    max_runs = xtc.get_controller_max_runs()
                    ip_addr = xtc.get_controller_ip_addr()
                    status_text = xtc.get_runs(stage_flags)

                    elapsed = str(datetime.timedelta(seconds=elapsed))
                    elapsed = elapsed.split(".")[0]   # get rid of decimal digits at end

                    box_name = cs["box_name"]
                    indent = "  "
                    cname = "localhost" if box_name=="local" else box_name

                    fmt_str = "XT controller:\n" + \
                        indent + "{}:{}, {}, SSL, xtlib: {}\n" + \
                        indent + "IP: {}:{}, running time: {}, max-runs: {}"
                        
                    text = fmt_str.format(job_id, cname, compute, xt_version, ip_addr, cs["port"], elapsed, max_runs)

                    text +=  "\n\n" + stage_flags + " runs on " + box_name.upper() + ":\n"
            
                    report = self.core.build_jobs_report(status_text)

                    console.print(text)
                    console.print(report)
                else:
                    console.print("could not connect to controller")

    #---- VIEW CONTROLLER LOG command ----
    @argument("job-id", help="the name of the job whose node will be restarted")
    @option("node-index", default=0, help="the 0-based node index to be restarted")
    @example(task="view the conntroller log for single node job100", text="xt view controller status job100")
    @command(kwgroup="view", kwhelp="view information about a node using the XT controller", help="uses the XT controller to view it's log on the specified job/node")
    def view_controller_log(self, job_id, node_index):

        result = None

        # get the connection string for the job/node
        cs_plus = job_helper.get_client_cs(self.core, job_id, node_index)
        cs = cs_plus["cs"]
        box_secret = cs_plus["box_secret"]
        stage_flags="queued, active, completed"

        with XTClient(self.config, cs, box_secret) as xtc:
            if xtc.connect():
                text = xtc.get_controller_log()

                box = cs["box_name"]
                console.print("box={}, controller log:".format(box.upper()))
                console.print(text)
            else:
                console.print("could not connect to controller")

    #---- RUN command ----
    @argument("script", required=True, type=str, help="the name of the script to run")
    @argument("script-args", required=False, type="text", help="the command line arguments for the script")

    # visible and hidden options (currently=71 total, 41 visible)
    @hidden("aggregate-dest", default="$hyperparameter-search.aggregate-dest", help="where hyperparameter searches should be aggregated for HX ('job' or 'experiment')")
    @hidden("after-dirs", default="$after-files.after-dirs", help="the files and directories to upload after the run completes")
    @hidden("after-omit", default="$after-files.after-omit", help="the files and directories to omit from after uploading")
    @flag("after-upload", default="$after-files.after-upload", help="when true, the after files are upload when the run completes")
    @hidden("option-prefix", default="$hyperparameter-search.option-prefix", help="the prefix to be used for specifying hyperparameter options to the script")
    @flag("attach", default="$general.attach", help="when True, the XT controller is also used on Azure ML runs")
    @option("cluster", type=str, help="the name of the Philly cluster to be used")
    @hidden("code-dirs", default="$code.code-dirs", help="paths to the main code directory and dependent directories")
    @hidden("code-omit", default="$code.code-omit", help="the list wildcard patterns to omit uploading from the code files")
    @flag("code-upload", default="$code.code-upload", help="when true, code is uploaded to job and download for each run of job")
    @hidden("code-zip", default="$code.code-zip", type=str, help="the type zip file to create for the CODE files: none/fast/compress")
    @option("concurrent", default="$hyperparameter-search.concurrent", type=int, help="the maximum concurrent runs to be allowed on each node")
    @option("data-action", default="$data.data-action", help="the data action to take on the target, before run is started")
    @hidden("data-local", default="$data.data-local", help="the path on the local machine specifying where the data for this job resides")
    @hidden("data-omit", default="$data.data-omit", help="the list wildcard patterns to omit uploading from the data files")
    @hidden("data-share-path", default="$data.data-share-path", help="the path on the data share where data for this run will be stored")
    @flag("data-upload", default="$data.data-upload", help="when true, the data for this job will be automatically upload when the job is submitted")
    @flag("data-writable", default="$data.data-writable", help="when true, a mounted data path can be written to")
    @hidden("delay-evaluation", default="$early-stopping.delay-evaluation", type=int, help="number of evals (metric loggings) to wait before applying early stopping policy")
    @option("description", help="your description of this run")
    @flag("direct-run", default="$general.direct-run", help="when True, the script is run without the controller (on Philly or AML)")
    @flag("distributed", default="$general.distributed", help="when True, the multiple nodes will be put into distributed training mode")
    @hidden("distributed-training", default="$aml-options.distributed-training", help="the name of the backend process to use for distributed training")
    @flag("dry-run", help="when True, the planned runs are displayed but not submitted")
    @hidden("early-policy", default="$early-stopping.early-policy", help="the name of the early-stopping policy to use (bandit, median, truncation, none)")
    @option("escape", type=int, default=0, help="breaks out of attach or --monitor loop after specified # of seconds")
    @hidden("env-vars", default="$general.env-vars", help="the environment variable to be passed to the run when it is launched")
    @option("docker", help="the docker entry to use with the target (from one of the entries in the config file [dockers] section")
    @hidden("evaluation-interval", default="$early-stopping.evaluation-interval", type=int, help="the frequencency (# of metric logs) for testing the policy")
    @option("experiment", default="$general.experiment", type=str, help="the name of the experiment to create this run under")
    @flag("fake-submit", help="when True, we skip creation of job and runs and the submit (used for internal testing)")
    @hidden("fn_generated_config", default="$hyperparameter-search.fn-generated-config", type=str, help="the name for the generated HP config file")
    @hidden("framework", default="$aml-options.framework", help="the name of the framework to be installed for the run (pytorch, tensorflow, chainer)")
    @hidden("fw-version", default="$aml-options.fw-version", help="the framework version number")
    #@hidden("grok-server", default="$logging.grok-server", help="the ip address of the grok-server to be used for mirroring")
    @flag("hold", help="when True, the Azure Pool (VM's) are held open for debugging)")
    @option("hp-config", default="$hyperparameter-search.hp-config", type=str, help="the path of the hyperparameter config file")
    @hidden("log", default="$logging.log", help="specifes if run-related events should be logged")
    @option("low-pri", type=bool, help="when true, use low-priority (preemptable) nodes for this job")
    @option("max-minutes", default="$hyperparameter-search.max-minutes", type=int, help="the maximum number of minutes the run can execute before being terminated")
    @hidden("max-seconds", type=int, default="$aml-options.max-seconds", help="the maximum number of seconds this run will execute before being terminated")
    @option("max-runs", default="$hyperparameter-search.max-runs", type=int, help="the total number of runs across all nodes (for hyperparameter searches)")
    @hidden("maximize-metric", default="$general.maximize-metric", help="whether to minimize or maximize value of primary metric")
    @hidden("mirror-dest", default="$logging.mirror-dest", help="the location where mirrored information is store (none, storage, grok)")
    @hidden("mirror-files", default="$logging.mirror-files", help="the wildcard path that specifies files to be mirrored")
    @option("model-action", default="$model.model-action", help="the model action to take on the target, before run is started")
    @hidden("model-share-path", default="$model.model-share-path", help="the model share name for the model")
    @flag("model-writable", default="$model.model-writable", help="when true, a mounted model path can be written to")
    @flag("monitor", help="when True, a Jupyter notebook is created to monitor the run")
    @flag("multi-commands"   , help="the script file contains multiple run commands (one per line)")
    @option("nodes", type=int, help="the number of normal (non-preemptable) nodes to allocte for this run")
    @option("parent-script", type=str, help="path of script used to initialize the target for repeated runs of primary script")
    @hidden("pip-freeze", default="$internal.pip-freeze", help="when true, installed pip packges are included in the setup log")
    @hidden("primary-metric", default="$general.primary-metric", help="the name of the metric to use for hyperparameter searching")
    @option("queue", type=str, help="the name of the Philly queue to use when submitting this job")
    #@option("repeat", type=int, help="the number of times to repeat the run, on each node")
    @hidden("remote-control", default="$general.remote-control", help="specifies if XT controller will listen for XT client commands")
    @hidden("report-rollup", default="$run-reports.report-rollup", help="whether to rollup metrics by primary metric or just use last reported metric set")
    @option("resume-name", help="when resuming a run, this names the previous run")
    @option("runs", default=None, type=int, help="the total number of runs across all nodes (for hyperparameter searches)")
    @option("schedule", default="static", values=["static", "dynamic"], help="specifies if runs are pre-assigned to each node or allocate on demand")
    @option("search-type", values=["random", "grid", "bayesian", "dgd"], default="$hyperparameter-search.search-type", help="the type of hyperparameter search to perform")
    @option("seed", default=None, help="the random number seed that can be used for reproducible HP searches")
    @flag("show-controller", default="$internal.show-controller", help="displays output of local or pool boxes in an locla command window")
    @option("sku", help="the name of the Philly SKU to be used (e.g, 'G1')")
    @hidden("slack-factor", default="$early-stopping.slack-factor", type=float, help="(bandit only) specified as a ratio, the delta between this eval and the best performing eval")
    @hidden("slack-amount", default="$early-stopping.slack-amount", type=float, help="(bandit only) specified as an amount, the delta between this eval and the best performing eval")
    @hidden("storage", default="$xt-services.storage", help="name of storage service to be used for this run")
    @option("submit-logs", default=None, help="specifies a directory to which log files for the submit are saved")
    @option("target", default="$xt-services.target", help="one of the user-defined compute targets on which to run")
    @hidden("truncation-percentage", default="$early-stopping.truncation-percentage", type=float, help="truncation only) percent of runs to cancel at each eval interval")
    @option("use-gpu", type=bool, default="$aml-options.use-gpu", help="when True, the gpu(s) on the nodes will be used by the run")
    @hidden("username", default="$general.username", help="the username to log as the author of this run")
    @hidden("user-managed", type=bool, default="$aml-options.user-managed", help="if true, it implies that the local machine or VM will be managed by the user")
    @option("vc", help="the name of the Philly virtual cluster to be used")
    @option("vm-size", help="the type of Azure VM computer to run on")
    @hidden("working-dir", default="$code.working-dir", type=str, help="the run's working directory, relative to the code directory")
    @option("workspace", default="$general.workspace", type=str, help="the workspace to create and manage the run")
    @flag("xtlib-upload", default="$code.xtlib-upload", help="when True, local source code for xtlib is included in the source code snapshot ")
    
    @example(task="run the script miniMnist.py", text="xt run miniMnist.py")
    @example(task="run the linux command 'sleep3d' on philly", text="xt --target=philly --code-upload=0 run sleep 3d")
    @command(options_before_cmd=True, keyword_optional=False, pass_by_args=True, help="submits a script or executable file for running on the specified compute target")
    def run(self, args):
        '''
        The run command is used to run a program, python script, batch file, or shell script on 
        one of following compute services:

        - local (the local machine)
        - pool (a specified set of computers managed by the user)
        - Azure Batch
        - Azure ML
        - Philly
        '''
        #console.diag("run_cmd")

        # add xt cmd to args
        cmd = get_dispatch_cmd()
        args["xt_cmd"] = "xt " + cmd if cmd else ""

        runner = Runner(self.config, self.core)
        runner.process_run_command(args)

    # TEMP (dup of runner.py function)
    def get_script_dir(self, cmd_parts):
        script_dir = None

        parts = cmd_parts
        for i, part in enumerate(parts):
            path = os.path.realpath(part)
            if os.path.isfile(path):
                script_dir = os.path.dirname(path)
                parts[i] = os.path.basename(path)
                break

        return script_dir
    


