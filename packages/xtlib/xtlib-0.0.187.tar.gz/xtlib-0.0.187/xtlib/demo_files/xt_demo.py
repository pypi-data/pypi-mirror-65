#
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.
#
# xt_demo.py: runs a set of titled xt commands, with navigations: run/skip/back/quite
import os
import sys
import logging
import argparse

from xtlib.helpers.feedbackParts import feedback as fb
from xtlib.helpers.key_press_checker import KeyPressChecker

from xtlib import utils
from xtlib import xt_cmds
from xtlib import pc_utils
from xtlib import file_utils
from xtlib import constants

logger = logging.getLogger(__name__)

cmds = []
cmd_count = 0

ARCHIVES_DIR = "..\\xt_demo_archives"

def build_cmds(auto_mode, quick_test):

    is_windows = (os.name == "nt")
    has_gui = pc_utils.has_gui()
    browse_flag = "--browse" if has_gui else ""

    # SET THESE before each demo (exper24 should be a multi-service set of simple runs)
    prev_exper = "exper18"
    curr_exper = "exper26"

    # OVERVIEW
    add_cmd("show the XT about page", "xt help --about")
    add_cmd("show the help topic on the miniMnist app", "xt help topic mini_mnist")

    # CONFIG FILES
    add_cmd("view the XT default config file", "xt config --default")
    add_cmd("view the local XT config file", "xt config")

    # HELP
    add_cmd("display XT commands", "xt help")
    add_cmd("display help for LIST JOBS command", "xt help list jobs")

    if has_gui:
        add_cmd("browse the XT HTML docs", "xt help --browse")

    # VERSION / RESTART
    add_cmd("display XT version", "xt help --version")

    # STATUS
    add_cmd("display STATUS of jobs on AZURE BATCH", "xt view status --target=batch")
    add_cmd("display all active jobs on any of my compute targets", "xt view status --target=all --active")

    # INITIAL SYNC LOCAL RUN (this will create MNIST data and model)
    add_cmd("run script without XT and generate data/model", "!python code\\miniMnist.py --data=data --save-model")

    # upload DATA/MODELS (depends on miniMnist generated data and model)
    add_cmd("upload MNIST dataset", "xt upload ./data/MNIST/processed/** MNIST/processed --share=data")
    add_cmd("upload previously trained MNIST model", "xt upload .\models\miniMnist\** miniMnist --share=models")

    # RUNS
    add_cmd("run script on LOCAL MACHINE", "xt  --target=local --exper={} run code\miniMnist.py".format(curr_exper))
    add_cmd("run script on PHILLY", "xt  --target=philly --exper={} run code\miniMnist.py".format(curr_exper))
    add_cmd("run script on AZURE BATCH", "xt  --target=batch --exper={} run code\miniMnist.py".format(curr_exper))
    add_cmd("run script on AZURE ML", "xt  --target=aml --exper={} run code\miniMnist.py".format(curr_exper))

    # REPORTS
    add_cmd("OVERVIEW: status of jobs", "xt list jobs --last=4")
    add_cmd("ZOOM in on CURRENT experiment", "xt list runs --exper={}".format(curr_exper))

    # TAGGING
    add_cmd("add tag 'good_run' to run1809, run1820", "xt set tags run1809, run1820 good_run")
    add_cmd("list runs with the 'good_run' tag", "xt list runs --workspace=ws1 --tags=good_run")

    # CMD LINE PIPING
    add_cmd("the 'list runs' and 'list jobs' have powerful filtering and sorting options", "xt list runs --exper=miniSearch --sort=metrics.test-acc --last=5")
    add_cmd("you can leverage the 'list runs' cmd to feed runs into another cmd, using XT command piping", \
        "!xt list runs --exper=miniSearch --sort=metrics.test-acc --last=5 | xt set tags $ top5")
    add_cmd("let's see which runs are now tagged with 'top5", 'xt list runs --tags=top5')

    # VIEW PORTAL
    add_cmd("Browse the portal for the 'philly' target", "xt view portal philly {}".format(browse_flag))
    add_cmd("Browse the portal for the 'aml' target", "xt view portal aml {}".format(browse_flag))

    if has_gui:
        # TENSORBOARD 
        templ = "{run}_{target}_lr={hparams.lr}_mo={hparams.momentum}_opt={hparams.optimizer}_tt={logdir}"
        cmd = 'xt view tensorboard --work=ws1 --exper={} {} --template="{}"'.format(prev_exper, browse_flag, templ)
        add_cmd("view LIVE tensorboard of cross-service experiments with custom path template", cmd)

    # LOG, CONSOLE, ARTIFACTS
    #add_cmd("view log for run1728", "xt view log ws1/run1728")
    add_cmd("view console output of run1728 (Azure ML run)", "xt view console ws1/run1728")

    browse_opt = "" if auto_mode or not has_gui else "--browse" 
    add_cmd("download all source code, output, and logs for run1728", "xt extract ws1/run1728 {}\\run1728 {}".format(ARCHIVES_DIR, browse_opt))

    # RERUN
    add_cmd("rerun run2362, with original source code and hyperparameter settings", "xt rerun ws1/run2362")

    # MOUNT data and DOWNLOAD model
    add_cmd("run script, mounting data and downloading model for eval", "xt --target=philly --data-action=mount --model-action=download run code\miniMnist.py --auto-download=0 --eval-model=1")

    # DOCKER RUNS
    # add_cmd("log in to azure docker registry", "xt docker login  --environment=pytorch-xtlib ")
    # add_cmd("log out from docker registry", "xt docker logout  --environment=pytorch-xtlib ")
    # add_cmd("run script in DOCKER container on LOCAL MACHINE", "xt --target=local --environment=pytorch-xtlib-local run code\miniMnist.py --no-cuda")
    # add_cmd("run script in DOCKER container on BATCH", "xt --target=batch --environment=pytorch-xtlib run code\miniMnist.py")

    # PARALLEL TRAINING
    add_cmd("run parallel training on Azure ML using 4 GPUs", 
        "xt --target=aml4x run code\miniMnist.py --train-percent=1 --test-percent=1  --epochs=100  --parallel=1")

    # DISTRIBUTED TRAINING
    add_cmd("run distributed training on Azure ML using 8 boxes", 
        "xt --target=aml --direct-run=true --nodes=8 --distributed run code\miniMnist.py --train-percent=1 --test-percent=1  --epochs=100  --distributed=1")

    timeout_opt = "--timeout=5" if auto_mode else ""

    # HPARAM SEARCH
    add_cmd("start a hyperparmeter search of 50 runs (5 boxes, 10 runs each) using Azure Batch", "xt --target=batch --runs=50 --nodes=5 --search-type=dgd --hp-config=code\miniSweeps.yaml run code\miniMnist.py")
    add_cmd("view a report of previously completed HP search, ordered by test accuracy", "xt list runs --job=job1100 --sort=metrics.test-acc --last=20")
    add_cmd("open Hyperparameter Explorer to compare the effect of hyperparameter settings on test accuracy, using a previously completed HP search", 
        "xt explore job2731 {}".format(timeout_opt))

    # AD-HOC PLOTTING (run as external cmd due to problem closing 2nd matplotlib window)
    if has_gui:

        # SINGLE PLOT of 10 RUNS
        cmd = '!xt plot run1467.391, run1467.392, run1467.393, run1467.394, run1467.395, run1467.396, run1467.397, run1467.398, run1467.399, run1467.400 ' + \
            "test-acc {}".format(timeout_opt)
        add_cmd("display a plot of 10 runs", cmd)

        # # APPLY SMOOTHING FACTOR
        # cmd = '!xt plot run1467.391, run1467.392, run1467.393, run1467.394, run1467.395, run1467.396, run1467.397, run1467.398, run1467.399, run1467.400 ' + \
        #     "test-acc --smooth=.85  {}".format(timeout_opt)
        # add_cmd("apply a smoothing factor", cmd)

        # # AGGREGATE over runs
        # cmd = '!xt plot run1467.391, run1467.392, run1467.393, run1467.394, run1467.395, run1467.396, run1467.397, run1467.398, run1467.399, run1467.400 ' + \
        #     "test-acc --smooth=.85 --aggregate=mean --range-type=std {}".format(timeout_opt)
        # add_cmd("plot the average the runs, using std as the range area", cmd)

        # 2 METRICS, 2x5 MATRIX (break on run)
        cmd = '!xt plot run1467.391, run1467.392, run1467.393, run1467.394, run1467.395, run1467.396, run1467.397, run1467.398, run1467.399, run1467.400 ' + \
            "train-acc, test-acc --break=run --layout=2x5 {}".format(timeout_opt)
        add_cmd("alternatively, let's add a 2nd metric, train-acc, and show each run in its own plot", cmd)

        # 2 METRICS, 2x1 MATRIX (break on col)
        cmd = '!xt plot run1467.391, run1467.392, run1467.393, run1467.394, run1467.395, run1467.396, run1467.397, run1467.398, run1467.399, run1467.400 ' + \
            "train-acc, test-acc --break=col --layout=2x1 {}".format(timeout_opt)
        add_cmd("finally, we can easily break on the col, instead of the run", cmd)

def add_cmd(title, xt_cmd, silent=False):

    title = file_utils.fix_slashes(title)
    xt_cmd = file_utils.fix_slashes(xt_cmd)

    cmd = {"title": title, "xt_cmd": xt_cmd, "silent": silent}
    cmds.append(cmd)

def wait_for_nav_key(auto_mode):
    if auto_mode:
        response = b"\r"
    else:
        # get KEYPRESS from user
        while True:
            with KeyPressChecker() as kpc:
                response = kpc.getch_wait()
                #xtprint("got reponse=", response)

            # treat control-c as "q"
            if response == b'\x03':
                response = b"q"

            if response in [b"\r", b"\n", b"s", b"b", b"q"]:
                break

            print("? ", end="", flush=True)

    print()
    return response

def wait_for_any_key(auto_mode):
    if auto_mode:
        response = b"\r"
    else:
        # get KEYPRESS from user
        while True:
            with KeyPressChecker() as kpc:
                response = kpc.getch_wait()
                break
    print()
    return response

def navigate(cmds, auto_mode, steps):
    pc_utils.enable_ansi_escape_chars_on_windows_10()
    
    index = 0
    while True:

        if index < 0:
            # keep in range (in response to user 'back')
            index = 0

        if not (1+index) in steps:
            index += 1
            if index >= len(cmds):
                break
            continue

        # show title, cmd
        cmd = cmds[index]
        cmd_text = cmd["xt_cmd"]
        silent = cmd["silent"]

        if silent:
            # don't show cmd; just execute it
            os.system(cmd_text)
            index += 1
            continue

        is_windows = (os.name == "nt")

        # clear screen
        if auto_mode:
            print("======================================")
        elif is_windows:
            # windows
            os.system("cls")
        else:
            # linux - screen is inconsistent (SSH screen drawing?)
            os.system('clear')
            
        if auto_mode:
            # adjust some commands for auto mode
            if cmd_text.startswith("xt rerun"):
                cmd_text += " --response=$cmd"
            elif cmd_text.startswith("xt extract"):
                cmd_text += " --response=y"
            elif cmd_text.startswith("xt explore"):
                cmd_text += " --timeout=5"
            # elif "--open" in cmd_text:
            #     cmd_text = cmd_text.replace("--open", "")

        print("xt demo {}/{}: {}".format(index+1, len(cmds), cmd["title"]))
        print(" > " + cmd_text + " ", end="", flush=True)

        response = wait_for_nav_key(auto_mode)
        #print("response=", response, 'b"q"=', b"q", response == b"q")

        if response in [b"\r", b"\n"]:
            # ---- RUN COMMAND ---- 
            if cmd_text.startswith("xt "):
                # run XT cmd internally
                fb.reset_feedback()
                xt_cmds.main(cmd_text)
            elif cmd_text.startswith("!"):
                os_cmd = cmd_text[1:]
                # treat as OS cmd
                os.system(os_cmd)
            else:
                raise Exception("internal error: unexpected cmd=", cmd_text)
            
            global cmd_count
            cmd_count += 1
            index += 1
        elif response == b"s":
            print("[skip]")
            index += 1
            continue
        elif response == b"b":
            print("[back]")
            index -= 1
            continue
        elif response == b"q":
            print("[quit]")
            break
        else:
            print("unrecognized choice: press ENTER to run, 'q' to quit, 's' for skip, or 'b' for back")

        if index >= len(cmds):
            break

        print()
        print("hit any key to continue: ", end="", flush=True)
        response = wait_for_any_key(auto_mode)
        if response == b"q":
            break

def parse_args(arg_list=None):
    # Training settings
    parser = argparse.ArgumentParser(description='XT Demo')

    parser.add_argument('--auto', action='store_true', default=False, help='runs the demo unattended')
    parser.add_argument('--quick-test', action='store_true', default=False, help='specifies we are running as part of the quick-test')
    parser.add_argument("steps", nargs="*", help="the steps to be run")

    if not arg_list:
        arg_list = sys.argv[1:]
    args = parser.parse_args(arg_list)

    print("parsed xt_demo args:", args)
    return args

def parse_steps(step_list):
    count = len(cmds)
    #print("step_list=", step_list)

    if step_list:
        steps = []
        for step in step_list:
            if "-" in step:
                low, high = step.split("-")
                low = int(low) if low else 1
                high = int(high) if high else count

                low = max(1, low)
                high = min(count, high)

                for s in range(low, high+1):
                    steps.append(s)
            else:
                step = int(step)
                step = max(1, min(count, step))
                steps.append(step)
    else:
        steps = range(1, 1+count)

    steps = list(steps)
    return steps

def main(arg_list=None):
    utils.init_logging(constants.FN_XT_EVENTS, logger, "XT Demo")

    args = parse_args(arg_list)
    auto_mode = args.auto
    quick_test = args.quick_test

    build_cmds(auto_mode, quick_test)

    steps = parse_steps(args.steps)
    response = ""

    if not auto_mode:
        print()
        print("This demonstrates how to run common XT commands")
        print("Press ENTER to execute each command (or s=SKIP, b=BACK, q=QUIT)")
        print()

        print("hit any key to continue: ", end="", flush=True)
        response = wait_for_any_key(auto_mode)

    if response != b"q":
        navigate(cmds, auto_mode, steps)

    # clean-up
    file_utils.ensure_dir_deleted(ARCHIVES_DIR)

    print("end of xt_demo")

    return cmd_count

if __name__ == "__main__":
    main()
