#
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.
#
# self.py: functions to help produce plots of metrics from runs
import math
import time
import numpy as np
import pandas as pd

from xtlib import utils
from xtlib import errors
from xtlib import console
from xtlib import run_helper

class PlotBuilder():
    def __init__(self, run_names, col_names, x_col, layout, break_on, title, colors, show_legend, plot_titles,
            legend_titles, smoothing_factor, plot_type, marker_size, marker_shape, alpha, edge_color, timeout,
            aggregate, range_type, range_alpha, run_log_records, style, show_toolbar, max_runs, max_traces,
            group_by, error_bars, cap_size, show_plot, save_to, x_label):
        
        self.run_names = run_names
        self.col_names = col_names
        self.x_col = x_col
        self.layout = layout
        self.break_on = break_on
        self.title = title
        self.colors = colors
        self.show_legend = show_legend
        self.plot_titles = plot_titles
        self.legend_titles = legend_titles
        self.smoothing_factor = smoothing_factor
        self.plot_type = plot_type
        self.marker_size = marker_size
        self.marker_shape = marker_shape
        self.alpha = alpha
        self.edge_color = edge_color
        self.timeout = timeout
        self.aggregate = utils.zap_none(aggregate)
        self.range_type = utils.zap_none(range_type)
        self.range_alpha = range_alpha
        self.run_log_records = run_log_records
        self.style = utils.zap_none(style)
        self.show_toolbar = show_toolbar
        self.max_runs = max_runs
        self.max_traces = max_traces
        self.group_by = group_by if group_by else "run"
        self.error_bars = utils.zap_none(error_bars)
        self.cap_size = cap_size
        self.show_plot = show_plot
        self.save_to = save_to
        self.x_label = x_label

    def build(self):

        data_frames_by_cols = self.build_data_frames()
        if data_frames_by_cols:

            for cols, dfx in data_frames_by_cols.items():
                dfx = self.pre_preprocess_data_frame(dfx)
                data_frames_by_cols[cols] = dfx

            # this check is to enable faster testing
            if self.show_plot or self.save_to:
                self.plot_data(data_frames_by_cols)

    def build_data_frames(self):
        '''
        1. for each run, collect the reported metrics as metric sets (by reported col list)

        2. append to the dataframe for that col list
        '''
        # build "data_frames"
        no_metrics = []
        pp_run_names = []
        used_max = False
        data_frames_by_cols = {}

        for record in self.run_log_records:
            # extract metrics for this run
            run = record["_id"]
            node = utils.node_id(record["node_index"])
            job = record["job_id"]
            experiment = record["exper_name"]
            workspace = record["ws"]

            log_records = record["log_records"]

            metric_sets = run_helper.build_metrics_sets(log_records)
            if not metric_sets:
                no_metrics.append(run)
                continue

            if self.max_runs and len(pp_run_names) >= self.max_runs:
                used_max = True
                break

            if not self.col_names:
                # not specified by user, so build defaults
                self.col_names, x_col = self.get_default_metric_column(metric_sets)

            if not self.x_col:
                self.x_col = x_col

            # merge metric sets into dfx
            for metric_set in metric_sets:

                # create a pandas DataFrame
                df = pd.DataFrame(metric_set["records"])
                cols = str(list(df.columns))
                
                # add run_name column
                df["run"] = [run] * df.shape[0]
                df["node"] = [node] * df.shape[0]
                df["job"] = [job] * df.shape[0]
                df["experiment"] = [experiment] * df.shape[0]
                df["workspace"] = [workspace] * df.shape[0]

                if not cols in data_frames_by_cols:
                    data_frames_by_cols[cols] = df
                else:
                    dfx = data_frames_by_cols[cols]
                    dfx = dfx.append(df)
                    data_frames_by_cols[cols] = dfx

            pp_run_names.append(run)

        if no_metrics:
            console.print("\nnote: following runs were skipped (currently have no logged metrics): \n    {}\n".format(", ".join(no_metrics)))

        if used_max:
            console.print("plotting first {} runs (use --max-runs to override)".format(self.max_runs))
        else:
            console.print("plotting {} runs...".format(len(pp_run_names)))

        # update our list of run_names to proces
        self.run_names = pp_run_names

        return data_frames_by_cols

    def get_agg_df(self, df, agg_op, df_cols):
        agg_dict = {}

        for col in self.col_names:
            if col in df_cols:
                agg_dict[col] = agg_op

        df_out = df.agg(agg_dict)  
        #df3 = df2.fillna(method='ffill')
        df_out = df_out.reset_index()

        return df_out

    def pre_preprocess_data_frame(self, dfx):
        '''
        apply pre-processing operations to specified data frame:
            - data frame most likely will NOT contain all y cols
            - optionally smooth the Y-axis cols
            - optionally create aggregate VALUE Y-axis cols
            - optionally create aggregate SHADOW Y-axi cols
        '''
        if self.smoothing_factor:
            # SMOOTH each column of values

            for col in self.col_names:
                if col in dfx.columns:
                    self.apply_smooth_factor(dfx, col, self.smoothing_factor)

        # get a copy of columns before group-by
        dfx_pre = dfx
        df_cols = list(dfx.columns)

        if self.aggregate:
            # specifying an aggregate hides the the other runs' values (for now)

            if self.group_by:
                # GROUP data 
                group_col = self.group_by
                group_prefix = "node" if self.group_by == "node_index" else ""
                x_col = self.x_col

                dfx = dfx.groupby([group_col, x_col])
            
            # AGGREGATE data
            df_agg_from = dfx
            dfx = self.get_agg_df(df_agg_from, self.aggregate, df_cols)

            # ERROR BARS data
            if self.error_bars:
                df_err = self.get_agg_df(df_agg_from, self.error_bars, df_cols)

                for col in self.col_names:
                    if col in df_err.columns:
                        # extract err data for col
                        err_data = df_err[col]

                        # add col data as new name to dfx
                        dfx[col + "_err_"] = err_data

            if self.range_type:
                self.run_names.append(self.range_type)

                min_values, max_values = self.range_runs(runs_dict, self.range_type)
                runs_dict[self.range_type] = (min_values, max_values)

        return dfx

    def apply_smooth_factor(self, data_frame, col, weight):

        presmooth_values = list(data_frame[col])
        smooth_values = self.apply_smooth_factor_core(presmooth_values, weight)

        data_frame[col] = smooth_values
        data_frame[col + "_presmooth_"] = presmooth_values

    def apply_smooth_factor_core(self, values, weight):
        smooth_values = []

        if values:
            prev = values[0] 
            for value in values:
                smooth = weight*prev + (1-weight)*value
                smooth_values.append(smooth)                       
                prev = smooth                                 

        return smooth_values

    def calc_actual_layout(self, count, layout):
        if not "x" in layout:
            errors.syntax_error("layout string must be of form RxC (R=# rows, C=# cols)")

        r,c = layout.split("x", 1)

        if r:
            r = int(r)
            c = int(c) if c else math.ceil(count / r)
        elif c:
            c = int(c)
            r = int(r) if r else math.ceil(count / c)

        full_count = r*c
        if full_count < count:
            errors.combo_error("too many plots ({}) for layout cells ({})".format(count, full_count))

        return r, c

    def get_xy_values(self, data_frames_by_cols, group_name, y_col, x_col):

        for cols, df in data_frames_by_cols.items():
            if y_col in df.columns:
                # get values for specified run name
                df = df[ df[self.group_by]==group_name ]

                col_list = [y_col]

                if x_col:
                    col_list.insert(0, x_col)

                err_col = y_col + "_err_"
                if err_col in df.columns:
                    col_list.append(err_col)

                dfc = df[ col_list ]
                dfc = dfc.dropna() 

                break

        return dfc

    def plot_data(self, data_frames_by_cols):
        console.diag("starting to plot data")

        # on-demand import for faster XT loading
        import seaborn as sns
        import matplotlib.pyplot as plt
        import matplotlib as mpl
        import pylab

        if not self.show_toolbar:
            # hide the ugly toolbar at bottom left of plot window
            mpl.rcParams['toolbar'] = 'None' 

        # apply seaborn styling
        if self.style:
            sns.set_style(self.style)

        # decide how layout, titles, etc. will be set
        for dfx in data_frames_by_cols.values():
            group_names = dfx[self.group_by].unique() 

            # first dataframe is sufficient
            break
        
        group_count = len(group_names)
        col_count = len(self.col_names)

        break_on_groups = self.break_on and ("run" in self.break_on or "group" in self.break_on)
        break_on_cols = self.break_on and "col" in self.break_on

        if break_on_groups and break_on_cols:
            plot_count = group_count*col_count
        elif break_on_groups:
            plot_count = group_count
        elif break_on_cols:
            plot_count = col_count
        else:
            plot_count = 1

        # calc true layout 
        if self.layout:
            plot_rows, plot_cols = self.calc_actual_layout(plot_count, self.layout) 
        else:
            plot_cols = plot_count
            plot_rows = 1

        runs_per_plot = 1 if break_on_groups else group_count
        cols_per_plot = 1 if break_on_cols else col_count
        
        if runs_per_plot == 1:
            plot_title = "$run"
            legend_text = "$col"
        elif cols_per_plot == 1:
            plot_title = "$col"
            legend_text = "$run"
        else:
            plot_title = None
            legend_text = "$col ($run)"

        if not self.plot_titles and plot_title:
            self.plot_titles = [plot_title]

        if not self.legend_titles:
            self.legend_titles = [legend_text]

        if not self.colors:
            self.colors = ["blue", "red", "green", "orange"]

        # configure matplotlib for our subplots
        sharex = True
        sharey = True

        #plt.close()
        window_size = (14, 6)

        fig, plots = plt.subplots(plot_rows, plot_cols, figsize=window_size, sharex=sharex, sharey=sharey, constrained_layout=True)
        if not isinstance(plots, np.ndarray):
            # make it consistent with plot_count > 1 plots
            plots = [plots]
        elif plot_rows > 1:
            plots = plots.flatten()

        fig.suptitle(self.title, fontsize=16)

        if self.timeout:
            # build a thread to close our plot window after specified time
            from threading import Thread

            def set_timer(timeout):
                console.print("set_timer called: timeout=", self.timeout)
                time.sleep(self.timeout)
                console.diag("timer triggered!")

                plt.close("all")
                print("closed all plots and the fig")

            thread = Thread(target=set_timer, args=[self.timeout])
            thread.daemon = True    # mark as background thread
            thread.start()

        line_index = 0
        plot_index = 0
        trace_count = 0
        x_label = self.x_label if self.x_label else self.x_col
            
        if self.aggregate == "none":
            self.aggregate = None

        if (self.aggregate and (break_on_cols and not break_on_groups)) \
            or ((not self.aggregate) and break_on_cols):
            # columns needs to be the outer loop
            for c, col in enumerate(self.col_names):

                if trace_count >= self.max_traces:
                    break

                if c and break_on_cols:
                    plot_index += 1
                    line_index = 0

                for r, group_name in enumerate(group_names):

                    if trace_count >= self.max_traces:
                        break

                    if r and break_on_groups:
                        plot_index += 1
                        line_index = 0

                    # PLOT_INNER
                    ax = plots[plot_index] # .gca()
                    dfc = self.get_xy_values(data_frames_by_cols, group_name, col, self.x_col)

                    self.plot_inner(ax, group_name, col, self.x_col, x_label, line_index, data_frame=dfc)
                    line_index += 1
                    trace_count += 1
        else:
            # run will work as the outer loop
            for r, group_name in enumerate(group_names):

                if trace_count >= self.max_traces:
                    break

                if r and break_on_groups:
                    plot_index += 1
                    line_index = 0

                for c, col in enumerate(self.col_names):

                    if trace_count >= self.max_traces:
                        break

                    if c and break_on_cols:
                        plot_index += 1
                        line_index = 0

                    # PLOT_INNER
                    ax = plots[plot_index] #.gca()
                    dfc = self.get_xy_values(data_frames_by_cols, group_name, col, self.x_col)

                    self.plot_inner(ax, group_name, col, self.x_col, x_label, line_index, data_frame=dfc)
                    line_index += 1
                    trace_count += 1

        if self.save_to:
            plt.savefig(self.save_to)

        if self.show_plot:
            pylab.show()

    def get_seaborn_color_map(self, name, n_colors=5):
        '''
        name: muted, xxx
        '''
        import seaborn as sns
        from matplotlib.colors import ListedColormap

        # Construct the colormap
        current_palette = sns.color_palette(name, n_colors=n_colors)
        cmap = ListedColormap(sns.color_palette(current_palette).as_hex())
        return cmap

    def plot_inner(self, ax, run_name, col, x_col, x_label, line_index, data_frame):

        import seaborn as sns
        from matplotlib.ticker import MaxNLocator

        col_count = len(data_frame.columns)

        x_values = data_frame.iloc[:, 0].values
        y_values = data_frame.iloc[:, 1].values
        err_values = data_frame.iloc[:, 2].values if col_count > 2 else None
        
        if x_values is not None:
            x_values = [float(x) for x in x_values]
            ax.set_xlabel(x_label)

        if isinstance(y_values, tuple):
            # its the 2-tuple of (low, high) values
            y_low, y_high = y_values

            y_low = [float(y) for y in y_low]
            y_high = [float(y) for y in y_high]

            if not x_values:
                x_values = range(len(y_low))
        else:
            # normal list of values
            y_low, y_high = None, None
            y_values = [float(y) for y in y_values]
            if not x_values:
                x_values = range(len(y_values))
        
        console.detail("x_values=", x_values)
        console.detail("y_values=", y_values)

        num_y_ticks = 10
        ax.get_yaxis().set_major_locator(MaxNLocator(num_y_ticks))
        color = self.colors[line_index % len(self.colors)]

        line_title = self.legend_titles[line_index % len(self.legend_titles)]
        line_title = self.fixup_text(line_title, run_name, col)

        cmap = self.get_seaborn_color_map("muted")
        if self.plot_type == "line":

            # LINE or RANGE PLOT
            if y_low:
                ax.fill_between(x_values, y_low, y_high, color=color, label=line_title, alpha=self.range_alpha)
            elif x_values:
                # ax.plot(x_values, y_values, '-', ms=self.marker_size, markerfacecolor=color, markeredgecolor=self.edge_color, 
                #     color=color, markeredgewidth=1, marker=self.marker_shape, 
                #     label=line_title, alpha=self.alpha)

                if err_values is not None:
                    ax.errorbar(x_values, y_values, yerr=err_values, label=line_title, capsize=self.cap_size)  # , elinewidth=3, markeredgewidth=10)
                else:
                    ax.plot(x_values, y_values, label=line_title, marker=self.marker_shape)

            #     markers = True if self.marker_shape else False
            #     sns.lineplot(x_values, y_values, label=line_title, ax=ax, markers=markers)
            else:
                ax.plot(y_values, '-', ms=self.marker_size, markerfacecolor=color, markeredgecolor=self.edge_color, 
                    color=color, markeredgewidth=1, label=line_title, alpha=self.alpha)

            #sns.relplot(x=x_col, y=col, kind="line", data=data_frame)
                    
        elif self.plot_type == "scatter":

            # SCATTER PLOT
            if not x_values:
                errors.combo_error("must specify x_col for scatterplots")

            ax.scatter(x_values, y_values, color=color,  label=line_title, s=self.marker_size, alpha=self.alpha)
            # '-', ms=3, markerfacecolor=color, markeredgecolor=color, 
            #     color=color, markeredgewidth=1,

        elif self.plot_type == "histogram":

            # HISTOGRAM
            ax.hist(y_values, color=color, label=line_title)
            
        else:
            errors.syntax_error("unknown plot type={}".format(self.plot_type))

        if self.plot_titles:
            plot_title = self.plot_titles[line_index % len(self.plot_titles)]
            plot_title = self.fixup_text(plot_title, run_name, col)

            ax.set_title(plot_title)

        if self.show_legend:
            ax.legend()

    def fixup_text(self, text, run_name, col):
        text = text.replace("$run", run_name)
        text = text.replace("$col", col)
        return text

    def get_default_metric_column(self, metric_sets):
        # remove x-col names from y_cols
        x_names = ["epoch", "step", "iter", "epochs", "steps", "iters"]
        x_col = None
        keys = None

        for ms in metric_sets:
            keys = ms["keys"]
            if len(keys) == 1 and keys[0].lower() == "epoch":
                # skip isolated epoch reporting
                continue

            for xn in x_names:
                if xn in keys:
                    if not x_col:
                        x_col = xn
                    keys.remove(xn)
                    break

            break

        return keys, x_col

    def range_runs(self, runs_dict, range):
        runs = list(runs_dict.values())

        if range == "minmax":
            min_values = np.min(runs, axis=0)
            max_values = np.max(runs, axis=0)
        elif range == "std":
            means = np.mean(runs, axis=0)
            max_values = means + np.std(runs, axis=0)
            min_values = means - np.std(runs, axis=0)
        elif range == "error":
            from scipy import stats

            means = np.mean(runs, axis=0)
            max_values = means + stats.sem(runs, axis=0)
            min_values = means - stats.sem(runs, axis=0)
        else:
            errors.syntax_error("unrecognized range value: {}".format(range))

        return min_values, max_values

    def get_values_by_run(self, col, run_log_records):
        runs_dict = {}

        for rr in run_log_records:
            run_name = rr["_id"]
            value_recs = rr["metrics"]["records"]
            new_values = [vr[col] for vr in value_recs]

            runs_dict[run_name] = new_values

        return runs_dict

    