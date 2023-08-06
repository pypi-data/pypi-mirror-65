#
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.
#
# hyperex.py: multi-pane matplotlib-based GUI for exploring runs thru their hyperparameter settings

import os
import json
import copy
import time
import numpy as np

# on-demand import of matplotlib
plt = None
patches = None
Rectangle = None
Button = None
RadioButtons = None

from xtlib.helpers.xt_config import get_merged_config
from xtlib.storage.store import Store
from xtlib import utils
from xtlib.console import console
from xtlib import errors

#LOCAL_CACHE_DIR = "e:/rdlexperiments"  # Local dir structure must match azure storage.

# GLOBALS (TODO: remove these)
USE_OLD_RUNS_DOWNLOAD = False
XTLIB_WORKSPACE = None
XTLIB_AGGNAME = None
XTLIB_AGGTYPE = None
SCORE_NAME = None

USE_SUCCESS_RATE = False  # May be overridden by config.txt.
HELDOUT_TESTING = False  # May be overridden by config.txt.
SUCCESS_RATE_THRESHOLD = 0.99  # May be overridden by config.txt.
MIN_SUCCESS_RATE_TO_PLOT = 0.5

RUN_COUNT_THRESHOLD = 0.

STD_DEV = 0
STD_ERR = 1
SEPARATE = 2
PLOT_STYLE_LABELS = ['Standard deviation', 'Standard error', 'Separate runs']

LEGEND_SIZE = 16
LEGEND_POSITION = 'lower left'

NUM_HIST_BINS = 64
PRUNE_SETTINGS = True

MAX_NUM_RUNS = 0  # For throttling.

fig = None

class PerformanceChart(object):
    def __init__(self, explorer, num_reports_per_run):
        self.explorer = explorer
        self.num_reports_per_run = num_reports_per_run
        self.perf_axes = fig.add_axes([0.54, 0.05, 0.44, 0.92])
        self.prev_curve = None
        # For the x axis, copy the steps from the first run. (All other runs are assumed to use the same set of steps.)
        self.steps = np.zeros((self.num_reports_per_run))
        for i in range(self.num_reports_per_run):
            self.steps[i] = self.explorer.runs[0].metric_reports[i].steps
        self.plot_from_runs()

    def plot_from_runs(self):
        self.perf_axes.clear()
        self.perf_axes.set_title("Workspace={}  {}={}".format(XTLIB_WORKSPACE, XTLIB_AGGTYPE.capitalize(), XTLIB_AGGNAME), fontsize=16)
        self.perf_axes.set_xlabel("Time steps", fontsize=16)
        if USE_SUCCESS_RATE:
            self.perf_axes.set_ylabel("Episode success rate", fontsize=16)
        else:
            self.perf_axes.set_ylabel("Mean {} over recent steps".format(SCORE_NAME), fontsize=16)
        self.perf_axes.set_xlim(self.explorer.plot_min_x, self.explorer.plot_max_x)
        self.perf_axes.set_ylim(self.explorer.plot_min_score, self.explorer.plot_max_score)
        # Count how many runs to include after filtering.
        runs = self.explorer.runs
        num_runs = 0
        for run in runs:
            if run.include:
                num_runs += 1
        # Gather the data into a numpy array.
        d = np.zeros((self.num_reports_per_run, num_runs))
        i_run = 0
        for run in runs:
            if run.include:
                for i_report in range(self.num_reports_per_run):
                    d[i_report, i_run] = run.metric_reports[i_report].score
                i_run += 1

        if (self.explorer.plot_style == STD_DEV) or (self.explorer.plot_style == STD_ERR):
            # Display means with error bars.
            means = np.zeros((self.num_reports_per_run))
            error_bars = np.zeros((self.num_reports_per_run))
            for i in range(self.num_reports_per_run):
                scores = d[i,:]
                means[i] = np.mean(scores)
                if self.explorer.plot_style == STD_DEV:
                    normalizer = 1.
                elif self.explorer.plot_style == STD_ERR:
                    normalizer = num_runs
                error_bars[i] = np.sqrt(np.var(scores, ddof=1) / normalizer)
            ymin = means - error_bars
            ymax = means + error_bars
            curve = PerfCurve(self.steps, means, ymin, ymax, num_runs)
            # Plot the curves.
            self.plot_error(curve, 'blue')
            self.plot_curve(curve, 'blue', label='Current set', alpha=1.)
            if self.prev_curve:
                self.plot_error(self.prev_curve, 'red')
                self.plot_curve(self.prev_curve, 'red', alpha=1., label='Previous set')
            self.perf_axes.legend(loc=LEGEND_POSITION, prop={'size': LEGEND_SIZE})
            self.prev_curve = curve
            # Dump.
            # for i in range(self.num_reports_per_run):
            #     console.print(means[i])
        else:
            # Display the runs separately.
            i_run = 0
            for run in runs:
                if run.include:
                    scores = d[:,i_run]
                    curve = PerfCurve(self.steps, scores, 0, 0, 1)
                    self.plot_curve(curve, 'blue', alpha=0.1, label='')
                    i_run += 1

        if USE_SUCCESS_RATE:
            threshold_line = HorizontalBar(SUCCESS_RATE_THRESHOLD, "Sample efficiency threshold", 'green',
                                           self.explorer.plot_min_x, self.explorer.plot_max_x)
            threshold_line.plot(self)

    def plot_error(self, curve, color):
        self.perf_axes.fill_between(curve.steps, curve.ymax, curve.ymin, color=color, alpha=0.2)

    def plot_curve(self, curve, color, alpha, label, include_runs=True):
        if include_runs:
            label += "  ({} runs)"
        self.perf_axes.plot(curve.steps, curve.means, label=(label.format(curve.num_runs)), color=color, alpha=alpha, linewidth=3)


class PerfCurve(object):
    def __init__(self, steps, means, ymin, ymax, num_runs):
        self.steps = steps
        self.means = means
        self.ymin = ymin
        self.ymax = ymax
        self.num_runs = num_runs


class HorizontalBar(object):
    def __init__(self, score, label, color, min_x, max_x):
        self.score = score
        self.label = label
        self.color = color
        self.plot_min_x = min_x
        self.plot_max_x = max_x
        self.plot_min_score = score
        self.plot_max_score = score

    def plot(self, perf_chart):
        d = np.zeros((2))
        d[0] = self.score
        d[1] = self.score

        steps = np.zeros((2))
        steps[0] = self.plot_min_x
        steps[1] = self.plot_max_x

        curve = PerfCurve(steps, d, d, d, 1)
        perf_chart.plot_curve(curve, self.color, alpha=1., label=self.label, include_runs=False)
        if (perf_chart.explorer.plot_style == STD_DEV) or (perf_chart.explorer.plot_style == STD_ERR):
            perf_chart.perf_axes.legend(loc=LEGEND_POSITION, prop={'size': LEGEND_SIZE})


class Histogram(object):
    def __init__(self, explorer, id, num_ids):
        self.explorer = explorer
        self.id = id
        self.num_ids = num_ids
        self.axes = None
        self.values = []
        self.y_button_height = 0.018
        self.setting = None  # Always None for global hist. Changes for setting hists.
        self.visible = False
        self.num_reports_per_run = self.explorer.num_reports_per_run

    def add_axes(self, axes_to_share):
        bottom_client_margin = 0.02  # So there's room at the bottom for a histogram title.
        top_hist_margin = 0.04  # To separate the histograms a bit.
        self.width = 0.25
        self.height = 1. / self.num_ids
        self.left_bound = 0.25
        self.bottom = bottom_client_margin + (self.num_ids - self.id - 1) * self.height
        self.height -= top_hist_margin
        if axes_to_share:
            self.axes = fig.add_axes([self.left_bound, self.bottom, self.width, self.height], sharex=axes_to_share)
        else:
            self.axes = fig.add_axes([self.left_bound, self.bottom, self.width, self.height])
        if self.id > 0:
            self.axes.get_xaxis().set_visible(False)
            self.axes.spines["right"].set_visible(False)
            self.axes.spines["top"].set_visible(False)
            self.init_button()
            self.set_visible(False)
        return self.axes

    def init_button(self):
        x_left_bound = self.left_bound
        x_width = self.width
        y_top = self.bottom
        self.button_axes = plt.axes([x_left_bound, y_top - self.y_button_height, x_width, self.y_button_height])
        self.button = Button(self.button_axes, "some text")
        self.button.label.set_fontsize(12)
        self.button.on_clicked(self.on_click)

    def set_visible(self, visible):
        self.axes.get_yaxis().set_visible(visible)
        self.axes.spines["left"].set_visible(visible)
        self.axes.spines["bottom"].set_visible(visible)
        self.button_axes.set_visible(visible)
        self.visible = visible

    def update(self):
        self.axes.clear()
        self.values = []
        if USE_SUCCESS_RATE:
            se_runs = []

        if self.id == 0:
            # The global histogram.
            for run in self.explorer.runs:
                if run.include:
                    self.values.append(run.overall_score)
        else:
            # A per-setting histogram.
            hparam = self.explorer.current_hparam
            if hparam != None:
                num_settings = len(hparam.settings)
                if self.id <= num_settings:
                    self.setting = hparam.settings[self.id - 1]
                    self.set_visible(True)
                    if self.setting.include:
                        for run in self.explorer.runs:
                            if run.include:
                                if run.hparam_name_value_pairs[self.setting.hparam.name] == self.setting.value:
                                    self.values.append(run.overall_score)
                                    if USE_SUCCESS_RATE:
                                        se_runs.append(run)
                        self.button.label.set_text("{}  ({} runs)".format(self.setting.value, len(self.values)))
                        self.axes.set_facecolor('1.0')  # White
                        self.axes.get_yaxis().set_visible(True)
                    else:
                        # This setting is excluded. Show any runs that would be included if this setting were toggled.
                        for run in self.explorer.runs:
                            if run.num_settings_that_exclude_this == 1:
                                if run.hparam_name_value_pairs[self.setting.hparam.name] == self.setting.value:
                                    self.values.append(run.overall_score)
                                    if USE_SUCCESS_RATE:
                                        se_runs.append(run)
                        self.button.label.set_text("{}  ({} runs, excluded)".format(self.setting.value, len(self.values)))
                        self.axes.set_facecolor('0.9')  # Gray
                        self.axes.get_yaxis().set_visible(False)
                else:
                    # This histogram is not currently mapped to a setting.
                    self.axes.set_facecolor('1.0')
                    self.set_visible(False)
        if self.id == 0:
            color = 'b'
            if USE_SUCCESS_RATE:
                self.axes.set_xlabel("(<--better)   Sample efficiency, in training steps", fontsize=14)
            else:
                self.axes.set_xlabel("Mean {} over all steps   (better-->)".format(SCORE_NAME), fontsize=14)
            self.axes.set_ylabel("Runs in set", fontsize=14)
        else:
            color = (0., 0.7, 0.)
        edgecolor = 'white' if self.values else None

        # Plot the histogram bins.
        self.axes.hist(self.values, bins=NUM_HIST_BINS, range=(self.explorer.hist_min_x, self.explorer.hist_max_x),
                       facecolor=color, edgecolor=edgecolor, zorder=2)

        if self.visible and (self.id > 0):
            if len(self.values) > 0:
                y = 0
                h = self.axes.viewLim.y1
                x = self.explorer.hist_min_x

                if USE_SUCCESS_RATE:
                    w = self.explorer.compute_sample_efficiency(se_runs)
                else:
                    # Average the run scores (like reward).
                    tot = 0.
                    for v in self.values:
                        tot += v
                    w = tot / len(self.values)

                # Plot the aggregate per-setting metric.
                if self.setting.include:
                    color = 'orange'
                else:
                    color = (0.9, 0.8, 0.6)
                rect = Rectangle((x,y), w, h,linewidth=1,edgecolor=color,facecolor=color, zorder=1)
                self.axes.add_patch(rect)

            # Plot the best runsets as small square marks.
            self.plot_best_runsets()

    def plot_best_runsets(self):
        canvas_x0 = self.axes._position.x0
        canvas_x1 = self.axes._position.x1
        canvas_y0 = self.axes._position.y0
        canvas_y1 = self.axes._position.y1

        x0_units = self.axes.viewLim.x0
        x1_units = self.axes.viewLim.x1
        y0_units = self.axes.viewLim.y0
        y1_units = self.axes.viewLim.y1

        x_units_per_pixel = (x1_units - x0_units) / (fig.bbox.bounds[2] * (canvas_x1 - canvas_x0))
        y_units_per_pixel = (y1_units - y0_units) / (fig.bbox.bounds[3] * (canvas_y1 - canvas_y0))

        count_y1 = self.explorer.max_runs_per_runset + 1
        count_y0 = RUN_COUNT_THRESHOLD
        count_scale = (y1_units - y0_units) / (count_y1 - count_y0)

        mark_size = 5.  # pixels
        mark_dx = mark_size * x_units_per_pixel
        mark_dy = mark_size * y_units_per_pixel
        metric_offset = mark_size * x_units_per_pixel / 2.
        count_offset = mark_size * y_units_per_pixel / 2.

        hparam = self.explorer.current_hparam
        if hparam != None:
            num_settings = len(hparam.settings)
            if self.id <= num_settings:
                self.setting = hparam.settings[self.id - 1]
                for runset in self.explorer.configstring_runset_dict.values():
                    if runset.runs[0].hparam_name_value_pairs[self.setting.hparam.name] == self.setting.value:
                        if runset.count > count_y0:
                            # if runset.count > y1_units:
                            #     assert runset.count <= y1_units
                            if runset.metric > x1_units:
                                assert runset.metric <= x1_units
                            count_norm = (runset.count - count_y0) * count_scale - y0_units
                            rect = Rectangle((runset.metric - metric_offset, count_norm - count_offset), mark_dx, mark_dy,
                                              linewidth=1, edgecolor='black', facecolor='black', zorder=3)
                            self.axes.add_patch(rect)

    def on_click(self, event):
        self.setting.include = not self.setting.include
        self.explorer.update_runs()


class MetricReport(object):
    def __init__(self, run_record, time_name, step_name, success_rate_name, sample_efficiency_name, primary_metric):
        metric_dict = run_record["data"]

        self.time = float(metric_dict[time_name]) if time_name in metric_dict else 0
        if not step_name in metric_dict:
            errors.combo_error("step name hyperparameter '{}' (named in XT config file) not found in hp search file".format(step_name))
        self.steps = int(metric_dict[step_name])

        if USE_SUCCESS_RATE:
            self.score = float(metric_dict[success_rate_name])
            self.sample_efficiency = float(metric_dict[sample_efficiency_name])
        else:
            self.score = float(metric_dict[primary_metric])


class RunSet(object):
    def __init__(self, configuration_string):
        self.configuration_string = configuration_string
        self.runs = []
        self.count = None
        self.metric = None


class Run(object):
    def __init__(self, run_record, time_name, step_name, success_rate_name, sample_efficiency_name, primary_metric):
        
        self.hparam_name_value_pairs = {}
        self.settings = []
        self.configuration_string = ''
        self.include = True
        self.num_settings_that_exclude_this = 0
        self.reset_metrics()

        if USE_OLD_RUNS_DOWNLOAD:
            json_line = json.loads(run_record)
            log_records = json_line['log']
        else:
            log_records = run_record['log_records']

        for log_record in log_records:
            event = log_record["event"]

            if event == "hparams":
                hparam_dict = log_record["data"]
                for key in hparam_dict:
                    self.hparam_name_value_pairs[key] = hparam_dict[key]
            elif event == "metrics":
                self.add_metric_report(log_record, time_name, step_name, success_rate_name, sample_efficiency_name, primary_metric)

        self.normalize_overall_score()

    def reset_metrics(self):
        self.metric_reports = []
        self.overall_score = 0.

    def add_metric_report(self, run_record, time_name, step_name, success_rate_name, sample_efficiency_name, primary_metric):
        metric_report = MetricReport(run_record, time_name, step_name, success_rate_name, sample_efficiency_name, primary_metric)
        self.metric_reports.append(metric_report)
        if USE_SUCCESS_RATE:
            self.overall_score = metric_report.sample_efficiency
        else:
            self.overall_score += metric_report.score

    def extend_metric_reports(self, target_num_metric_reports, reporting_interval):
        current_num = len(self.metric_reports)
        if current_num < target_num_metric_reports:
            final_metric_report = self.metric_reports[-1]
            for i in range(target_num_metric_reports - current_num):
                new_metric_report = copy.copy(final_metric_report)
                new_metric_report.steps += (i + 1) * reporting_interval
                self.metric_reports.append(new_metric_report)

    def normalize_overall_score(self):
        num_reports = len(self.metric_reports)
        if not USE_SUCCESS_RATE:
            if num_reports > 0:
                self.overall_score /= num_reports

    def update_inclusion(self):
        self.include = True
        self.num_settings_that_exclude_this = 0
        for setting in self.settings:
            if not setting.include:
                self.include = False
                self.num_settings_that_exclude_this += 1


class HyperparameterSetting(object):
    def __init__(self, explorer, hparam, id, value, include):
        self.explorer = explorer
        self.hparam = hparam
        self.id = id
        self.value = value
        self.include = include


class Hyperparameter(object):
    def __init__(self, explorer, group, name):
        self.explorer = explorer
        self.group = group
        self.name = name
        self.id = -1
        self.value_setting_dict = {}
        self.settings = []
        self.single_value = None
        self.display = False

    def add_setting(self, setting_value, include):
        if setting_value not in self.value_setting_dict.keys():
            setting = HyperparameterSetting(self.explorer, self, 0, setting_value, include)
            self.value_setting_dict[setting_value] = setting
        setting = self.value_setting_dict[setting_value]
        self.single_value = setting_value
        return setting

    def init_button(self):
        x_left_bound = 0.015
        x_width = 0.2
        y_top_bound = 0.08
        y_spacing = 0.06
        y_button_height = 0.04
        self.button_axes = plt.axes([x_left_bound, 1.0 - y_top_bound - self.id * y_spacing, x_width, y_button_height])
        self.button = Button(self.button_axes, self.name)
        self.button.label.set_fontsize(18)
        self.button.on_clicked(self.on_click)

    def on_click(self, event):
        if self.explorer.current_hparam != self:
            self.explorer.set_current_hparam(self)
            self.explorer.update_histograms()
            fig.canvas.draw()


class HyperparameterGroup(object):
    def __init__(self, explorer, title):
        self.explorer = explorer
        self.title = title
        self.hparams = []
        self.display = False

    def add_hparam(self, hparam):
        self.hparams.append(hparam)


class HyperparameterExplorer(object):
    def __init__(self, store, ws_name, primary_metric, cache_dir, aggregate_dest, dest_name, fn_hp_config,
        steps_name, log_interval_name, time_name, step_name, success_rate_name, sample_efficiency_name):

        # on-demand import (since reference causes fonts to rebuild cache...)
        global plt, patches, Rectangle, Button, RadioButtons

        import matplotlib.pyplot as plt
        import matplotlib.patches as patches
        from matplotlib.patches import Rectangle
        from matplotlib.widgets import Button
        from matplotlib.widgets import RadioButtons

        # TODO: remove these globals
        global XTLIB_WORKSPACE, XTLIB_AGGNAME, XTLIB_AGGTYPE, SCORE_NAME, fig
        XTLIB_WORKSPACE = ws_name
        XTLIB_AGGNAME = dest_name
        XTLIB_AGGTYPE = aggregate_dest
        SCORE_NAME = primary_metric

        global fig

        fig = plt.figure(figsize=(20,12))
        fig.canvas.set_window_title('Hyperparameter Explorer')

        self.left_pane_axes = fig.add_axes([0.0, 0.0, 1.0, 1.0])
        self.left_pane_axes.get_xaxis().set_visible(False)
        self.left_pane_axes.get_yaxis().set_visible(False)
        self.left_pane_axes.spines["left"].set_visible(False)
        self.left_pane_axes.spines["right"].set_visible(False)
        self.left_pane_axes.spines["top"].set_visible(False)
        self.left_pane_axes.spines["bottom"].set_visible(False)

        self.plot_style = STD_DEV
        self.radio_buttons_axes = fig.add_axes([0.83, 0.07, 0.14, 0.1])
        self.radio_buttons = RadioButtons(self.radio_buttons_axes, (PLOT_STYLE_LABELS[0], PLOT_STYLE_LABELS[1], PLOT_STYLE_LABELS[2]))
        self.radio_buttons_axes.set_zorder(20)
        self.radio_buttons.on_clicked(self.radio_buttons_on_clicked)

        self.set_current_hparam(None)

        self.xtstore = store   # Store(config=xt_config)
        self.ws_name = XTLIB_WORKSPACE
        self.fn_hp_config = fn_hp_config
        #self.exper_name = XTLIB_AGGNAME

        config_file_path, all_run_records = self.download_runs(aggregate_dest, dest_name, cache_dir)

        self.build_all(all_run_records, config_file_path, fn_hp_config, steps_name, log_interval_name, 
            time_name, step_name, success_rate_name, sample_efficiency_name, primary_metric)

    def build_all(self, all_run_records, config_file_path, fn_hp_config, steps_name, log_interval_name, 
            time_name, step_name, success_rate_name, sample_efficiency_name, primary_metric):

        self.define_hyperparameters(config_file_path)  # Get the superset of hparam definitions.

        # if USE_OLD_RUNS_DOWNLOAD:
        #     all_runs_file_path = "{}{}".format(local_cache_path, "all_runs.jsonl")
        #     self.load_runs_from_file(all_runs_file_path)
        # else:
        #     self.all_runs = self.xtstore.get_all_runs('experiment', self.ws_name, self.exper_name)
        #     self.load_runs()  # Populate the run objects with some data.

        self.load_runs(all_run_records, time_name, step_name, success_rate_name, sample_efficiency_name, primary_metric)  # Populate the run objects with some data.

        # set TOTAL_STEPS, REPORTING_INTERVAL
        if not steps_name in self.name_hparam_dict:
            errors.combo_error("steps hyperparameter '{}', which was specified in the XT config file, was not found in hyperparameters file: {}"  \
                    .format(steps_name, fn_hp_config))
        self.TOTAL_STEPS = self.name_hparam_dict[steps_name].single_value

        # TODO: remove this dependency on REPORTING_INTERVAL
        if log_interval_name in self.name_hparam_dict:
            REPORTING_INTERVAL = self.name_hparam_dict[log_interval_name].single_value
        else:
            #REPORTING_INTERVAL = 20
            errors.combo_error("Missing required LOG_INTERVAL hyperparameter")

        self.num_reports_per_run = self.TOTAL_STEPS // REPORTING_INTERVAL

        # Copy each run's final metric report as necessary.
        for run in self.runs:
            run.extend_metric_reports(self.num_reports_per_run, REPORTING_INTERVAL)

        self.get_plot_bounds_from_runs()
        self.populate_hparams()

        # Assemble runsets.
        self.configstring_runset_dict = {}
        self.group_runs_into_runsets()

        for run in self.runs:
            run.update_inclusion()  # This takes into consideration any non-included settings.
        self.assemble_left_pane()
        self.create_hparam_border()

        # Create a fixed set of histogram objects to be reused for all settings.
        # The first (top) histogram is the aggregate for all settings (in the focus).
        self.hists = []
        for i in range(self.max_settings_per_hparam + 1):
            self.hists.append(Histogram(self, i, self.max_settings_per_hparam + 1))

        # Add the histogram axes in reverse order, to get the right z-order.
        axes_to_share = self.hists[self.max_settings_per_hparam].add_axes(None)
        for i in range(self.max_settings_per_hparam):
            self.hists[self.max_settings_per_hparam - i - 1].add_axes(axes_to_share)

        # Populate histograms.
        self.update_histograms()

        # Create the perf chart.
        self.perf = PerformanceChart(self, self.num_reports_per_run)

    def download_runs(self, aggregate_dest, dest_name, cache_dir):

        # Download the all_runs file
        local_cache_path = "{}/{}/{}/".format(cache_dir, self.ws_name, dest_name)
        config_file_path = "{}{}".format(local_cache_path, "config.txt")
        all_runs_file_path = "{}{}".format(local_cache_path, "all_runs.txt")

        if aggregate_dest == "experiment":
            console.print("downloading runs for EXPERIMENT={}...".format(dest_name))
            # files are at EXPERIMENT LEVEL
            # read SWEEPS file
            if not self.xtstore.does_experiment_file_exist(self.ws_name, dest_name, self.fn_hp_config):
                errors.store_error("missing experiment hp_config file (ws={}, exper={}, fn={})".format(self.ws_name, 
                    dest_name, self.fn_hp_config))
            self.xtstore.download_file_from_experiment(self.ws_name, dest_name, self.fn_hp_config, config_file_path)

            # read ALLRUNS info aggregated in EXPERIMENT
            # if not self.xtstore.does_experiment_file_exist(self.ws_name, dest_name, constants.ALL_RUNS_FN):
            #     errors.user_error("missing experiment SUMMARY file (ws={}, exper={}, fn={})".format(
            #         self.ws_name, dest_name, constants.ALL_RUNS_FN))
            # self.xtstore.download_file_from_experiment(self.ws_name, dest_name, constants.ALL_RUNS_FN, all_runs_file_path)
            allrun_records = self.xtstore.get_all_runs(aggregate_dest, self.ws_name, dest_name)
        else:  
            console.print("downloading runs for JOB={}...".format(dest_name))
            # files are at JOB LEVEL
            # read SWEEPS file
            if not self.xtstore.does_job_file_exist(dest_name, self.fn_hp_config):
                errors.store_error("missing job hp_config file (job={}, fn={})".format(dest_name, self.fn_hp_config))
            self.xtstore.download_file_from_job(dest_name, self.fn_hp_config, config_file_path)

            # read ALLRUNS info aggregated in JOB
            # if not self.xtstore.does_job_file_exist(dest_name, constants.ALL_RUNS_FN):
            #     errors.user_error("missing job SUMMARY file (job={}, fn={})".format(dest_name, constants.ALL_RUNS_FN))
            # self.xtstore.download_file_from_job(dest_name, constants.ALL_RUNS_FN, all_runs_file_path)
            allrun_records = self.xtstore.get_all_runs(aggregate_dest, self.ws_name, dest_name)

        console.diag("after downloading all runs")

        # # Get the runs.
        # local_cache_path = "{}/{}/{}/".format(LOCAL_CACHE_DIR, self.ws_name, self.exper_name)
        # hp_config_file_path = "{}{}".format(local_cache_path, "config.txt")
        # self.xtstore.download_file_from_experiment(self.ws_name, self.exper_name, "config.txt", hp_config_file_path)
        return config_file_path, allrun_records

    def load_runs_from_file(self, all_runs_path):
        self.runs = []
        for line in open(all_runs_path, 'r'):
            # Process one run.log
            run = Run(line)
            if len(run.metric_reports) == 0:  # Parent runs can create lines without metric reports.
                continue
            self.runs.append(run)
            if MAX_NUM_RUNS > 0:
                if len(self.runs) == MAX_NUM_RUNS:
                    break
        # console.print("num runs processed = {}".format(len(self.runs)))

    def radio_buttons_on_clicked(self, label):
        if label == PLOT_STYLE_LABELS[self.plot_style]:
            return
        if label == PLOT_STYLE_LABELS[0]:
            self.plot_style = 0
        elif label == PLOT_STYLE_LABELS[1]:
            self.plot_style = 1
        elif label == PLOT_STYLE_LABELS[2]:
            self.plot_style = 2
        self.perf.prev_curve = None
        self.perf.plot_from_runs()
        fig.canvas.draw()

    def draw(self):
        self.hist.draw()

    def create_hparam_border(self):
        if len(self.name_hparam_dict) > 0:
            if len(self.displayed_hparams) > 0:
                rect = self.displayed_hparams[0].button_axes.get_position()
                xm = 0.004
                ym = 0.006
                x = rect.x0 - xm
                y = 2.0
                w = (rect.x1 - rect.x0) + 2*xm
                h = (rect.y1 - rect.y0) + 2*ym
                rectangle = Rectangle((x, y), w, h, linewidth=4, edgecolor='g', facecolor='none')
                self.hparam_border = self.left_pane_axes.add_patch(rectangle)

    def set_current_hparam(self, hparam):
        self.current_hparam = hparam
        if hparam != None:
            rect = hparam.button_axes.get_position()
            xm = 0.004
            ym = 0.006
            x = rect.x0 - xm
            y = rect.y0 - ym
            self.hparam_border.set_xy([x, y])

    def run(self, timeout=None):
        if len(self.runs) == 0:
            console.print("error - no valid runs found")
            return

        if timeout:
            # build a thread to close our plot window after specified time
            from threading import Thread

            def set_timer(timeout):
                console.print("set_timer called: timeout=", timeout)
                time.sleep(timeout)
                console.diag("timer triggered!")
                plt.close("all")

            thread = Thread(target=set_timer, args=[timeout])
            thread.daemon = True    # mark as background thread
            thread.start()

        mng = plt.get_current_fig_manager()
        #mng.window.showMaximized()

        plt.show()

    def define_hyperparameters(self, hp_config_file_path):
        self.name_hparam_dict = {}
        self.hparam_groups = []
        with open(hp_config_file_path, 'r') as file:
            hp_config_file_text = file.read()
        line_num = 0
        group = None
        lines = hp_config_file_text.split('\n')
        for line in lines:
            line_num += 1
            if (len(line) == 0) or (line[0] == '#'):
                if (len(line) > 0):
                    group = HyperparameterGroup(self, line[2:])
                    self.hparam_groups.append(group)
                continue
            halves = line.split('=')
            name_string, value_string = halves[0].strip(), halves[1].strip()
            if value_string == 'randint':
                continue  # Ignore the seed parameters.
            hparam = Hyperparameter(self, group, name_string)
            if '#' in value_string:
                value_string = value_string[:value_string.index('#')].strip()
            values = value_string.split(',')
            for value in values:
                hparam.add_setting(self.cast_value(value.strip()), True)
            self.name_hparam_dict[name_string] = hparam
            group.add_hparam(hparam)
        if "USE_SUCCESS_RATE" in self.name_hparam_dict.keys():
            global USE_SUCCESS_RATE
            USE_SUCCESS_RATE = self.name_hparam_dict["USE_SUCCESS_RATE"].single_value
        if "HELDOUT_TESTING" in self.name_hparam_dict.keys():
            global HELDOUT_TESTING
            HELDOUT_TESTING = self.name_hparam_dict["HELDOUT_TESTING"].single_value
        if "SUCCESS_RATE_THRESHOLD" in self.name_hparam_dict.keys():
            global SUCCESS_RATE_THRESHOLD
            SUCCESS_RATE_THRESHOLD = self.name_hparam_dict["SUCCESS_RATE_THRESHOLD"].single_value

    def cast_value(self, value_str):
        if value_str == 'None':
            new_value = None
        elif value_str == 'True':
            new_value = True
        elif value_str == 'False':
            new_value = False
        else:
            try:
                new_value = int(value_str)
            except ValueError:
                try:
                    new_value = float(value_str)
                except ValueError:
                    new_value = value_str
        return new_value

    def load_runs(self, all_run_records, time_name, step_name, success_rate_name, sample_efficiency_name, primary_metric):
        self.runs = []
        for record in all_run_records:
            run = Run(record, time_name, step_name, success_rate_name, sample_efficiency_name, primary_metric)
            if len(run.metric_reports) == 0:  # Parent runs can create lines without metric reports.
                continue
            self.runs.append(run)
            if MAX_NUM_RUNS > 0:
                if len(self.runs) == MAX_NUM_RUNS:
                    break

    def get_plot_bounds_from_runs(self):
        self.plot_min_x = 1000000000
        self.plot_max_x = -1000000000
        self.plot_min_score = 1000000000
        self.plot_max_score = -1000000000
        if USE_SUCCESS_RATE:
            self.plot_min_x = 0.
            self.plot_min_score = 0.
            self.plot_max_score = 1.0
        for run in self.runs:
            for report in run.metric_reports:
                x = report.steps
                if x > self.plot_max_x:
                    self.plot_max_x = x
                if x < self.plot_min_x:
                    self.plot_min_x = x
                y = report.score
                if y > self.plot_max_score:
                    self.plot_max_score = y
                if y < self.plot_min_score:
                    self.plot_min_score = y
        if USE_SUCCESS_RATE:
            self.hist_min_x = self.plot_min_x
            self.hist_max_x = self.plot_max_x
            if MIN_SUCCESS_RATE_TO_PLOT is not None:
                self.plot_min_score = MIN_SUCCESS_RATE_TO_PLOT
        else:
            self.hist_min_x = self.plot_min_score
            self.hist_max_x = self.plot_max_score

    def populate_hparams(self):
        # Connect up the runs and hparams.
        for run in self.runs:
            for hparam_name in run.hparam_name_value_pairs.keys():  # Only hparams that were read by the code,
                if hparam_name in self.name_hparam_dict.keys():  # and were listed in config_overrides.txt.
                    hparam = self.name_hparam_dict[hparam_name]
                    setting_value = run.hparam_name_value_pairs[hparam_name]
                    setting = hparam.add_setting(setting_value, not PRUNE_SETTINGS)
                    run.settings.append(setting)
        # Decide which hparams to display in the left pane.
        for hparam_name, hparam in self.name_hparam_dict.items():
            if len(hparam.value_setting_dict) > 1:
                hparam.display = True
                hparam.group.display = True
                setting_values = []
                for setting in hparam.value_setting_dict.values():
                    setting_values.append(setting.value)
                # Sort the settings, to determine their display order in the middle pane.
                setting_values.sort()
                for val in setting_values:
                    hparam.settings.append(hparam.value_setting_dict[val])

    def group_runs_into_runsets(self):
        # Create the runsets.
        for run in self.runs:
            for hparam_name in run.hparam_name_value_pairs.keys():  # Only hparams that were read by the code,
                if hparam_name in self.name_hparam_dict.keys():              # and were listed in config_overrides.txt,
                    hparam = self.name_hparam_dict[hparam_name]
                    if hparam.display:                              # and were chosen for display.
                        run.configuration_string += '{}, '.format(run.hparam_name_value_pairs[hparam_name])
            if run.configuration_string not in self.configstring_runset_dict.keys():
                self.configstring_runset_dict[run.configuration_string] = RunSet(run.configuration_string)
            runset = self.configstring_runset_dict[run.configuration_string]
            runset.runs.append(run)
        # Print a report.
        self.max_runs_per_runset = 0
        n1 = 0
        np = 0
        for runset in self.configstring_runset_dict.values():
            num_runs = len(runset.runs)
            if num_runs > self.max_runs_per_runset:
                self.max_runs_per_runset = num_runs
            if num_runs == 1:
                n1 += 1
            else:
                np += 1
        console.print("{} runs".format(len(self.runs)))
        console.print("{} runsets".format(len(self.configstring_runset_dict)))
        console.print("{} have 1 run".format(n1))
        console.print("{} max runs per runset".format(self.max_runs_per_runset))
        # Finalize each runset.
        for runset in self.configstring_runset_dict.values():
            runset.count = len(runset.runs)
            if USE_SUCCESS_RATE:
                # Calculate sample efficiency from the success rates of the runs.
                runset.metric = self.compute_sample_efficiency(runset.runs)
            else:
                # Average the run scores (like reward).
                sum = 0.
                for run in runset.runs:
                    sum += run.overall_score
                    runset.metric = sum / runset.count

    def assemble_left_pane(self):
        self.max_settings_per_hparam = 0
        id = 0
        self.displayed_hparams = []
        for group in self.hparam_groups:
            if group.display:
                # console.print("\n# {}".format(group.title))
                for hparam in group.hparams:
                    if hparam.display:
                        self.displayed_hparams.append(hparam)
                        num_settings = len(hparam.settings)
                        if num_settings > self.max_settings_per_hparam:
                            self.max_settings_per_hparam = num_settings
                        hparam.id = id
                        id += 1
                        hparam.init_button()
                        # console.print("  {}".format(hparam.name))
                        # for setting in hparam.settings:
                        #     console.print("    {}".format(setting.value))
        self.num_settings_to_display = self.max_settings_per_hparam

    def update_histograms(self):
        for hist in self.hists:
            hist.update()
        self.hists[0].axes.set_xlim(self.hist_min_x, self.hist_max_x)

    def update_runs(self):
        for run in self.runs:
            run.update_inclusion()
        self.update_histograms()
        self.perf.plot_from_runs()
        fig.canvas.draw()

    def compute_sample_efficiency(self, runs):
        if HELDOUT_TESTING:
            return min(self.TOTAL_STEPS, self.compute_sample_efficiency_by_median(runs))
        else:
            return self.compute_sample_efficiency_by_mean_success_rate(runs)

    def compute_sample_efficiency_by_median(self, runs):
        return np.median([run.overall_score for run in runs])

    def compute_sample_efficiency_by_mean_success_rate(self, runs):
        # First aggregate the success rates of the runs.
        num_runs = len(runs)
        num_reports = self.num_reports_per_run
        xs = np.zeros((num_reports))
        ys = np.zeros((num_reports))
        for run in runs:
            for i in range(num_reports):
                ys[i] += run.metric_reports[i].score
        for i in range(num_reports):
            ys[i] /= num_runs
            xs[i] = self.runs[0].metric_reports[i].steps
        return self.x_at_y(SUCCESS_RATE_THRESHOLD, xs, ys)

    def x_at_y(self, y, xs, ys):
        x1 = 0.
        y1 = 0.
        for i in range(len(xs)):
            x2 = xs[i]
            y2 = ys[i]
            if y2 >= y:
                return x1 + (x2 - x1) * (y - y1) / (y2 - y1)
            else:
                x1 = x2
                y1 = y2
        return x1


if __name__ == "__main__":
    hx = HyperparameterExplorer()
    hx.run()
