'''
Utilities for descriptive analytics.

:author: Andreas Kanz

'''

# Imports
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import pandas as pd
import seaborn as sns


# Missing value plot
def missingval_plot(data, cmap='PuBuGn', figsize=(20, 12), sort=False, spine_color='#EEEEEE'):
    '''
    Two-dimensional visualization of the missing values in a dataset.

    Parameters
    ----------
    data: 2D dataset that can be coerced into Pandas DataFrame. If a Pandas DataFrame is provided, the index/column information is used to label the plots.

    cmap: colormap, default 'PuBuGn'
        Any valid colormap can be used. E.g. 'Greys', 'RdPu'. More information can be found in the matplotlib documentation.

    figsize: tuple, default (20,12)
        Use to control the figure size.

    sort: bool, default False
        Sort columns based on missing values in descending order and drop columns without any missing values

    spine_color: color-code, default '#EEEEEE'
    Set to 'None' to hide the spines on all plots or use any valid matplotlib color argument.

    Returns
    -------
    ax: matplotlib Axes. Axes object with the heatmap.
    '''

    data = pd.DataFrame(data)

    if sort:
        mv_cols_sorted = data.isna().sum(axis=0).sort_values(ascending=False)
        final_cols = mv_cols_sorted.drop(mv_cols_sorted[mv_cols_sorted.values == 0].keys().tolist()).keys().tolist()
        data = data[final_cols]
        print('Displaying only columns with missing values.')

    # Identify missing values
    mv_cols = data.isna().sum(axis=0)
    mv_rows = data.isna().sum(axis=1)
    mv_total = mv_cols.sum()
    mv_cols_rel = mv_cols / data.shape[0]
    total_datapoints = data.shape[0]*data.shape[1]

    if mv_total == 0:
        print('No missing values found in the dataset.')
    else:
        # Create figure and axes
        fig = plt.figure(figsize=figsize)
        grid = fig.add_gridspec(nrows=6, ncols=6, left=0.05, right=0.48, wspace=0.05)
        ax1 = fig.add_subplot(grid[:1, :5])
        ax2 = fig.add_subplot(grid[1:, :5])
        ax3 = fig.add_subplot(grid[:1, 5:])
        ax4 = fig.add_subplot(grid[1:, 5:])

        # ax1 - Barplot
        colors = plt.get_cmap(cmap)(mv_cols / np.max(mv_cols))  # color bars by height
        ax1.bar(range(len(mv_cols)), np.round((mv_cols_rel)*100, 2), color=colors)
        ax1.get_xaxis().set_visible(False)
        ax1.set(frame_on=False, xlim=(-.5, len(mv_cols)-0.5))
        ax1.set_ylim(0, np.max(mv_cols_rel)*100)
        ax1.grid(linestyle=':', linewidth=1)
        ax1.yaxis.set_major_formatter(ticker.PercentFormatter(decimals=0))
        ax1.tick_params(axis='y', colors='#111111', length=1)

        # annotate values on top of the bars
        for rect, label in zip(ax1.patches, mv_cols):
            height = rect.get_height()
            ax1.text(.1 + rect.get_x() + rect.get_width() / 2, height+0.5, label,
                     ha='center',
                     va='bottom',
                     rotation='90',
                     alpha=0.5,
                     fontsize='small')

        ax1.set_frame_on(True)
        for _, spine in ax1.spines.items():
            spine.set_visible(True)
            spine.set_color(spine_color)
        ax1.spines['top'].set_color(None)

        # ax2 - Heatmap
        sns.heatmap(data.isna(), cbar=False, cmap='binary', ax=ax2)
        ax2.set_yticks(np.round(ax2.get_yticks()[0::5], -1))
        ax2.set_yticklabels(ax2.get_yticks())
        ax2.set_xticklabels(
            ax2.get_xticklabels(),
            horizontalalignment='center',
            fontweight='light',
            fontsize='medium')
        ax2.tick_params(length=1, colors='#111111')
        for _, spine in ax2.spines.items():
            spine.set_visible(True)
            spine.set_color(spine_color)

        # ax3 - Summary
        fontax3 = {'color':  '#111111',
                   'weight': 'normal',
                   'size': 12,
                   }
        ax3.get_xaxis().set_visible(False)
        ax3.get_yaxis().set_visible(False)
        ax3.set(frame_on=False)

        ax3.text(0.1, 0.9, f"Total: {np.round(total_datapoints/1000,1)}K",
                 transform=ax3.transAxes,
                 fontdict=fontax3)
        ax3.text(0.1, 0.7, f"Missing: {np.round(mv_total/1000,1)}K",
                 transform=ax3.transAxes,
                 fontdict=fontax3)
        ax3.text(0.1, 0.5, f"Relative: {np.round(mv_total/total_datapoints*100,1)}%",
                 transform=ax3.transAxes,
                 fontdict=fontax3)
        ax3.text(0.1, 0.3, f"Max-col: {np.round(mv_cols.max()/data.shape[0]*100)}%",
                 transform=ax3.transAxes,
                 fontdict=fontax3)
        ax3.text(0.1, 0.1, f"Max-row: {np.round(mv_rows.max()/data.shape[1]*100)}%",
                 transform=ax3.transAxes,
                 fontdict=fontax3)

        # ax4 - Scatter plot
        ax4.get_yaxis().set_visible(False)
        for _, spine in ax4.spines.items():
            spine.set_color(spine_color)
        ax4.tick_params(axis='x', colors='#111111', length=1)

        ax4.scatter(mv_rows, range(len(mv_rows)), s=mv_rows, c=mv_rows, cmap=cmap, marker=".")
        ax4.set_ylim(0, len(mv_rows))
        ax4.set_ylim(ax4.get_ylim()[::-1])  # invert y-axis
        ax4.grid(linestyle=':', linewidth=1)


# Correlation matrix / heatmap
def corr_plot(data, split=None, threshold=0, cmap='BrBG', figsize=(12, 10), annot=True, dev=False, **kwargs):
    '''
    Two-dimensional visualization of the correlation between feature-columns, excluding NA values.

    Parameters
    ----------
    data: 2D dataset that can be coerced into Pandas DataFrame. If a Pandas DataFrame is provided, the index/column information is used to label the plots.

    split: {None, 'pos', 'neg', 'high', 'low'}, default None
        Type of split to be performed.

        * None: visualize all correlations between the feature-columns.
        * pos: visualize all positive correlations between the feature-columns above the threshold.
        * neg: visualize all negative correlations between the feature-columns below the threshold.
        * high: visualize all correlations between the feature-columns for which abs(corr) > threshold is True.
        * low: visualize all correlations between the feature-columns for which abs(corr) < threshold is True.

    threshold: float, default 0
        Value between 0 <= threshold <= 1

    cmap: matplotlib colormap name or object, or list of colors, default 'BrBG'
        The mapping from data values to color space.

    figsize: tuple, default (12, 10)
        Use to control the figure size.

    annot: bool, default True
        Use to show or hide annotations.

    dev: bool, default False
        Display figure settings in the plot by setting dev = True. If False, the settings are not displayed. Use for presentations.

    **kwargs: optional
        Additional elements to control the visualization of the plot, e.g.:

        * mask: bool, default True
        If set to False the entire correlation matrix, including the upper triangle is shown. Set dev = False in this case to avoid overlap.
        * vmax: float, default is calculated from the given correlation coefficients.
        Value between -1 or vmin <= vmax <= 1, limits the range of the colorbar.
        * vmin: float, default is calculated from the given correlation coefficients.
        Value between -1 <= vmin <= 1 or vmax, limits the range of the colorbar.
        * linewidths: float, default 0.5
        Controls the line-width inbetween the squares.
        * annot_kws: dict, default {'size' : 10}
        Controls the font size of the annotations. Only available when annot = True.
        * cbar_kws: dict, default {'shrink': .95, 'aspect': 30}
        Controls the size of the colorbar.
        * Many more kwargs are available, i.e. 'alpha' to control blending, or options to adjust labels, ticks ...

        Kwargs can be supplied through a dictionary of key-value pairs (see above).

    Returns
    -------
    ax: matplotlib Axes. Axes object with the heatmap.
    '''

    data = pd.DataFrame(data)

    if split == 'pos':
        corr = data.corr().where((data.corr() >= threshold) & (data.corr() > 0))
        print('Displaying positive correlations. Use "threshold" to further limit the results.')
    elif split == 'neg':
        corr = data.corr().where((data.corr() <= threshold) & (data.corr() < 0))
        print('Displaying negative correlations. Use "threshold" to further limit the results.')
    elif split == 'high':
        corr = data.corr().where(np.abs(data.corr()) >= threshold)
        print('Displaying absolute correlations above a chosen threshold.')
    elif split == 'low':
        corr = data.corr().where(np.abs(data.corr()) <= threshold)
        print('Displaying absolute correlations below a chosen threshold.')
    else:
        corr = data.corr()
        split = 'None'
        threshold = 'None'

    # Generate mask for the upper triangle
    mask = np.triu(np.ones_like(corr, dtype=np.bool))

    # Compute dimensions and correlation range to adjust settings
    vmax = np.round(np.nanmax(corr.where(mask == False))-0.05, 2)
    vmin = np.round(np.nanmin(corr.where(mask == False))+0.05, 2)

    # Set up the matplotlib figure and generate colormap
    fig, ax = plt.subplots(figsize=figsize)

    # kwargs for the heatmap
    kwargs = {'mask': mask,
              'cmap': cmap,
              'annot': annot,
              'vmax': vmax,
              'vmin': vmin,
              'linewidths': .5,
              'annot_kws': {'size': 10},
              'cbar_kws': {'shrink': .95, 'aspect': 30},
              **kwargs}

    # Draw heatmap with mask and some default settings
    sns.heatmap(corr,
                center=0,
                square=True,
                fmt='.2f',
                **kwargs
                )

    ax.set_title('Feature-correlation Matrix', fontdict={'fontsize': 18})

    if dev:  # show settings
        fig.suptitle(f"\
            Settings (dev-mode): \n\
            - split-mode: {split} \n\
            - threshold: {threshold} \n\
            - annotations: {annot} \n\
            - cbar: \n\
                - vmax: {vmax} \n\
                - vmin: {vmin} \n\
            - linewidths: {kwargs['linewidths']} \n\
            - annot_kws: {kwargs['annot_kws']} \n\
            - cbar_kws: {kwargs['cbar_kws']}",
                     fontsize=12,
                     color='gray',
                     x=0.35,
                     y=0.85,
                     ha='left')


# _functions

def _memory_usage(data):
    '''
    Gives the total memory usage in kilobytes.

    Parameters
    ----------
    data: 2D dataset that can be coerced into Pandas DataFrame. If a Pandas DataFrame is provided, the index/column information is used to label the plots.

    Returns
    -------
    memory_usage: float

    '''

    data = pd.DataFrame(data)
    memory_usage = round(data.memory_usage(index=True, deep=True).sum()/1024, 2)

    return memory_usage


def _missing_vals(data):
    '''
    Gives metrics of missing values in the dataset.

    Parameters
    ----------
    data: 2D dataset that can be coerced into Pandas DataFrame. If a Pandas DataFrame is provided, the index/column information is used to label the plots.

    Returns
    -------
    total_mv: float, number of missing values in the entire dataset
    rows_mv: float, number of missing values in each row
    cols_mv: float, number of missing values in each column
    rows_mv_ratio: float, ratio of missing values for each row
    cols_mv_ratio: float, ratio of missing values for each column
    '''

    data = pd.DataFrame(data)
    rows_mv = data.isna().sum(axis=0)
    cols_mv = data.isna().sum(axis=1)
    total_mv = data.isna().sum().sum()
    rows_mv_ratio = rows_mv/data.shape[0]
    cols_mv_ratio = cols_mv/data.shape[1]

    return total_mv, rows_mv, cols_mv, rows_mv_ratio, cols_mv_ratio
