"""
===========================
Creating annotated heatmaps
===========================

It is often desirable to show data which depends on two independent
variables as a color coded image plot. This is often referred to as a
heatmap. If the data is categorical, this would be called a categorical
heatmap.
Matplotlib's :meth:`imshow <matplotlib.axes.Axes.imshow>` function makes
production of such plots particularly easy.

The following examples show how to create a heatmap with annotations.
We will start with an easy example and expand it to be usable as a
universal function.
"""


##############################################################################
#
# A simple categorical heatmap
# ----------------------------
#
# We may start by defining some data. What we need is a 2D list or array
# which defines the data to color code. We then also need two lists or arrays
# of categories; of course the number of elements in those lists
# need to match the data along the respective axes.
# The heatmap itself is an :meth:`imshow <matplotlib.axes.Axes.imshow>` plot
# with the labels set to the categories we have.
# Note that it is important to set both, the tick locations
# (:meth:`set_xticks<matplotlib.axes.Axes.set_xticks>`) as well as the
# tick labels (:meth:`set_xticklabels<matplotlib.axes.Axes.set_xticklabels>`),
# otherwise they would become out of sync. The locations are just
# the ascending integer numbers, while the ticklabels are the labels to show.
# Finally we can label the data itself by creating a
# :class:`~matplotlib.text.Text` within each cell showing the value of
# that cell.


import numpy as np
import matplotlib.colors
from matplotlib import pyplot as plt
import ccalafiore.strings as cc_str
import ccalafiore.Formatter as cc_Formatter
import ccalafiore.Checker as cc_Checker

# from mpl_toolkits.axes_grid1 import make_axes_locatable
# sphinx_gallery_thumbnail_number = 2


#############################################################################
# Using the helper function code style
# ------------------------------------
#
# As discussed in the :ref:`Coding styles <coding_styles>`
# one might want to reuse such code to create some kind of heatmap
# for different input data and/or on different axes.
# We create a function that takes the data and the row and column labels as
# input, and allows arguments that are used to customize the plot
#
# Here, in addition to the above we also want to create a colorbar and
# position the labels above of the heatmap instead of below it.
# The annotations shall get different colors depending on a threshold
# for better contrast against the pixel color.
# Finally, we turn the surrounding axes spines off and create
# a grid of white lines to separate the cells.

my_dpi = 100


def heatmap(
        data, dict_axes=None, ax=None, add_cbar=True, maximum_n_pixels_per_plot=500,
        annot=False, array_annot=None, fmt_annot='{:.2f}', colors_annot=["black", "white"],
        threshold_change_color_anno=None, **kwargs):

    """
    Create a heatmap from a numpy array and two lists of labels.

    Parameters
    ----------
    data
        A 2D numpy array of shape (N, M).
    y_labels
        A list or array of length N with the labels for the rows.
    x_labels
        A list or array of length M with the labels for the columns.
    ax
        A `matplotlib.axes.Axes` instance to which the heatmap is plotted.  If
        not provided, use current axes or create a new one.  Optional.
    cbar_kw
        A dictionary with arguments to `matplotlib.Figure.colorbar`.  Optional.
    cbarlabel
        The label for the colorbar.  Optional.
    **kwargs
        title=None, label_x=None, label_y=None,
        fontsize_annot=None,
        labels_ticks_x, n_ticks_x, ticks_x,
        labels_ticks_y, n_ticks_y, ticks_y,
        fontsize_title=None, rotation_title=None,
        fontsize_label_x=None, rotation_label_x=None,
        fontsize_label_y=None, rotation_label_y=None,
        stagger_labels_ticks_x, fontsize_labels_ticks_x=None, rotation_labels_ticks_x=None,
        stagger_labels_ticks_y, fontsize_labels_ticks_y=None, rotation_labels_ticks_y=None,
        cmap=None, n_levels_cmap,
        labels_ticks_cbar, n_ticks_cbar, ticks_cbar, fontsize_labels_ticks_cbar=None,
        label_cbar=None, fontsize_label_cbar=None,

    """

    shape_data = np.asarray(data.shape, dtype=int)
    n_axes = shape_data.size
    if n_axes != 2:
        raise ValueError('data must have either 2 axes')

    keys_axes_expected = np.asarray(['y', 'x'], dtype=str)
    values_axes_expected = np.arange(n_axes)
    if dict_axes is None:
        dict_axes = dict(zip(keys_axes_expected, values_axes_expected))
    else:

        keys_axes, axes_data = cc_Formatter.dict_to_key_array_and_value_array(dict_axes)
        axes_negative = axes_data < 0
        axes_data[axes_negative] += n_axes
        for k in keys_axes[axes_negative]:
            dict_axes[k] += n_axes

        cc_Checker.keys_necessary_known_and_values_necessary_known_exist_and_other_keys_and_values_do_not_exist(
            dict_axes, keys_axes_expected, values_axes_expected, name_dictionary='dict_axes')
        cc_Checker.values_are_not_repeated(dict_axes, name_dictionary='dict_axes')

    if ax is None:
        figures_existing = plt.get_fignums()
        n_figures_new = 1
        i = 0
        f = 0
        while f < n_figures_new:
            if i in figures_existing:
                pass
            else:
                id_figures = i
                f += 1
            i += 1
        if data.shape[dict_axes['x']] > data.shape[dict_axes['y']]:
            ratio_x = 1
            ratio_y = data.shape[dict_axes['y']] / data.shape[dict_axes['x']]
        elif data.shape[dict_axes['x']] < data.shape[dict_axes['y']]:
            ratio_x = data.shape[dict_axes['x']] / data.shape[dict_axes['y']]
            ratio_y = 1
        else:
            ratio_x = 1
            ratio_y = 1
        fig = plt.figure(
            id_figures, frameon=False, dpi=my_dpi,
            figsize=((maximum_n_pixels_per_plot * ratio_x) / my_dpi, (maximum_n_pixels_per_plot * ratio_y) / my_dpi))
        ax = plt.gca()

    fig = ax.figure

    # Plot the heatmap
    # im = ax.imshow(data)

    if (isinstance(kwargs.get('cmap'), list) or isinstance(kwargs.get('cmap'), np.ndarray)):
        kwargs['cmap'] = matplotlib.colors.ListedColormap(kwargs['cmap'], N=kwargs.get('n_levels_cmap'))
    elif isinstance(kwargs.get('cmap'), matplotlib.colors.ListedColormap):
        pass
    elif (kwargs.get('cmap') is not None) and (kwargs.get('n_levels_cmap') is not None):
            kwargs['cmap'] = plt.get_cmap(kwargs['cmap'], kwargs['n_levels_cmap'])

    im = ax.imshow(data, cmap=kwargs.get('cmap'))

    # Create colorbar
    # divider = make_axes_locatable(ax)
    # cax = divider.append_axes("right", size="5%", pad=0.05)
    if add_cbar:
        # cbar = ax.figure.colorbar(
        #     im, ax=ax, ticks=np.arange(kwargs.get('levels_cmap')))

        if kwargs.get('labels_ticks_cbar') is None:
            if kwargs.get('ticks_cbar') is None:
                if kwargs.get('n_ticks_cbar') is None:
                    cbar = ax.figure.colorbar(im, ax=ax)
                else:
                    max_cbar = data.max()
                    min_cbar = data.min()
                    n_labels_ticks_cbar = kwargs['n_ticks_cbar']
                    delta_cbar = (max_cbar - min_cbar) / (n_labels_ticks_cbar - 1)
                    tick_cbar_lower = min_cbar
                    tick_cbar_higher = max_cbar
                    kwargs['ticks_cbar'] = np.arange(
                        tick_cbar_lower, tick_cbar_higher + delta_cbar, delta_cbar)
                    cbar = ax.figure.colorbar(im, ax=ax, ticks=kwargs['ticks_cbar'])
            else:
                cbar = ax.figure.colorbar(im, ax=ax, ticks=kwargs['ticks_cbar'])
        else:
            if kwargs.get('ticks_cbar') is None:
                max_cbar = data.max()
                min_cbar = data.min()
                n_labels_ticks_cbar = len(kwargs['labels_ticks_cbar'])
                delta_cbar = (max_cbar - min_cbar) / n_labels_ticks_cbar
                tick_cbar_lower = min_cbar + (delta_cbar / 2)
                tick_cbar_higher = max_cbar - (delta_cbar / 2)
                kwargs['ticks_cbar'] = np.arange(tick_cbar_lower, tick_cbar_higher + delta_cbar, delta_cbar)
                cbar = ax.figure.colorbar(im, ax=ax, ticks=kwargs['ticks_cbar'])
                cbar.ax.set_yticklabels(kwargs['labels_ticks_cbar'])
            else:
                cbar = ax.figure.colorbar(im, ax=ax, ticks=kwargs['ticks_cbar'])
                cbar.ax.set_yticklabels(kwargs['labels_ticks_cbar'])

        # cbar = plt.colorbar(im, ax=ax)
        ax.set_aspect('auto')
        if kwargs.get('fontsize_labels_ticks_cbar') is not None:
            cbar.ax.tick_params(labelsize=kwargs['fontsize_labels_ticks_cbar'])
        if kwargs.get('label_cbar') is not None:
            cbar.ax.set_ylabel(kwargs['label_cbar'], rotation=-90, va="bottom", fontsize=kwargs.get('fontsize_label_cbar'))
    # if fontsize_cbar_ticklabels != 'auto':
    #     # fontsize_cbar_ticklabels = 8
    #     # use matplotlib.colorbar.Colorbar object
    #     cbar = ax.collections[0].colorbar
    #     # here set the labelsize
    #     cbar.ax.tick_params(labelsize=fontsize_cbar_ticklabels)

    if kwargs.get('title') is not None:
        plt.title(kwargs['title'], fontsize=kwargs.get('fontsize_title'), rotation=kwargs.get('rotation_title'))
    if kwargs.get('label_x') is not None:
        plt.xlabel(kwargs['label_x'], fontsize=kwargs.get('fontsize_label_x'), rotation=kwargs.get('rotation_label_x'))
    if kwargs.get('label_y') is not None:
        plt.ylabel(kwargs['label_y'], fontsize=kwargs.get('fontsize_label_y'), rotation=kwargs.get('rotation_label_y'))

    ticks_x_are_applied = False
    if kwargs.get('labels_ticks_x') is None:
        max_x = data.shape[dict_axes['x']] - 1
        if kwargs.get('ticks_x') is None:
            if kwargs.get('n_ticks_x') is None:
                pass
            else:
                max_x = data.shape[dict_axes['x']] - 1
                min_x = 0
                n_labels_ticks_x = kwargs['n_ticks_x']
                delta_x = (max_x - min_x) / (n_labels_ticks_x - 1)
                tick_x_lower = min_x
                tick_x_higher = max_x
                kwargs['ticks_x'] = np.arange(tick_x_lower, tick_x_higher + delta_x, delta_x)
                ax.set_xticks(kwargs['ticks_x'])
                ticks_x_are_applied = True
        else:
            ax.set_xticks(kwargs['ticks_x'])
            ticks_x_are_applied = True

        if (kwargs.get('stagger_labels_ticks_x') or
                (kwargs.get('fontsize_labels_ticks_x') is not None) or
                (kwargs.get('rotation_labels_ticks_x') is not None)):
            fig.canvas.draw()
            tmp_labels_ticks_x = ax.get_xticklabels()
            n_labels_ticks_x = len(tmp_labels_ticks_x)
            kwargs['labels_ticks_x'] = [None] * n_labels_ticks_x
            for l, label_l in enumerate(tmp_labels_ticks_x):
                kwargs['labels_ticks_x'][l] = label_l.get_text()

    if kwargs.get('labels_ticks_x') is not None:
        if not ticks_x_are_applied:
            if kwargs.get('ticks_x') is None:
                max_x = data.shape[dict_axes['x']] - 1
                min_x = 0
                n_labels_ticks_x = len(kwargs['labels_ticks_x'])
                delta_x = (max_x - min_x) / (n_labels_ticks_x - 1)
                tick_x_lower = min_x
                tick_x_higher = max_x
                kwargs['ticks_x'] = np.arange(tick_x_lower, tick_x_higher + delta_x, delta_x)

            ax.set_xticks(kwargs['ticks_x'])
        if kwargs.get('stagger_labels_ticks_x'):
            kwargs['labels_ticks_x'] = (
                [l if not i % 2 else '\n' + l for i, l in enumerate(kwargs['labels_ticks_x'])])
        ax.set_xticklabels(
            kwargs['labels_ticks_x'], fontsize=kwargs.get('fontsize_labels_ticks_x'),
            rotation=kwargs.get('rotation_labels_ticks_x'))

    ticks_y_are_applied = False
    if kwargs.get('labels_ticks_y') is None:
        max_y = data.shape[dict_axes['y']] - 1
        if kwargs.get('ticks_y') is None:
            if kwargs.get('n_ticks_y') is None:
                pass
            else:
                max_y = data.shape[dict_axes['y']] - 1
                min_y = 0
                n_labels_ticks_y = kwargs['n_ticks_y']
                delta_y = (max_y - min_y) / (n_labels_ticks_y - 1)
                tick_y_lower = min_y
                tick_y_higher = max_y
                kwargs['ticks_y'] = np.arange(tick_y_lower, tick_y_higher + delta_y, delta_y)
                ax.set_yticks(kwargs['ticks_y'])
                ticks_y_are_applied = True

        else:
            ax.set_yticks(kwargs['ticks_y'])
            ticks_y_are_applied = True

        if (kwargs.get('stagger_labels_ticks_y') or
                (kwargs.get('fontsize_labels_ticks_y') is not None) or
                (kwargs.get('rotation_labels_ticks_y') is not None)):
            fig.canvas.draw()
            tmp_labels_ticks_y = ax.get_yticklabels()
            n_labels_ticks_y = len(tmp_labels_ticks_y)
            kwargs['labels_ticks_y'] = [None] * n_labels_ticks_y
            for l, label_l in enumerate(tmp_labels_ticks_y):
                kwargs['labels_ticks_y'][l] = label_l.get_text()

    if kwargs.get('labels_ticks_y') is not None:
        if not ticks_y_are_applied:
            if kwargs.get('ticks_y') is None:
                max_y = data.shape[dict_axes['y']] - 1
                min_y = 0
                n_labels_ticks_y = len(kwargs['labels_ticks_y'])
                delta_y = (max_y - min_y) / (n_labels_ticks_y - 1)
                tick_y_lower = min_y
                tick_y_higher = max_y
                kwargs['ticks_y'] = np.arange(tick_y_lower, tick_y_higher + delta_y, delta_y)

            ax.set_yticks(kwargs['ticks_y'])
        if kwargs.get('stagger_labels_ticks_y'):
            kwargs['labels_ticks_y'] = (
                [l if not i % 2 else '\n' + l for i, l in enumerate(kwargs['labels_ticks_y'])])
        ax.set_yticklabels(
            kwargs['labels_ticks_y'], fontsize=kwargs.get('fontsize_labels_ticks_y'),
            rotation=kwargs.get('rotation_labels_ticks_y'))

    if annot:
        """"
        A function to add_annotate a heatmap.
    
        Parameters
        ----------
        im
            The AxesImage to be labeled.
        data
            Data used to annotate.  If None, the image's data is used.  Optional.
        valfmt
            The format of the annotations inside the heatmap.  This should either
            use the string format method, e.g. "$ {x:.2f}", or be a
            `matplotlib.ticker.Formatter`.  Optional.
        textcolors
            A list or array of two color specifications.  The first is used for
            values below a threshold, the second for those above.  Optional.
        threshold
            Value in data units according to which the colors from textcolors are
            applied.  If None (the default) uses the middle of the colormap as
            separation.  Optional.
        **kwargs
            All other arguments are forwarded to each call to `text` used to create
            the text labels.
        """

        if array_annot is None:
            array_annot = data

        # Normalize the threshold to the images color range.
        if (isinstance(colors_annot, list) or
                isinstance(colors_annot, tuple) or
                isinstance(colors_annot, np.ndarray)):
            n_colors_annot = len(colors_annot)
        else:
            colors_annot = [colors_annot]
            n_colors_annot = 1

        if n_colors_annot == 1:
            # Set default alignment to center, but allow it to be
            # overwritten by textkw.
            kw = dict(horizontalalignment="center",
                      verticalalignment="center",
                      fontsize=kwargs['fontsize_annot'],
                      color=colors_annot[0])

        elif n_colors_annot == 2:
            # Set default alignment to center, but allow it to be
            # overwritten by textkw.
            kw = dict(horizontalalignment="center",
                      verticalalignment="center",
                      fontsize=kwargs['fontsize_annot'])

            if threshold_change_color_anno is not None:
                threshold = im.norm(threshold)
            else:
                threshold = im.norm(data.max()) / 2




        kw = dict(horizontalalignment="center",
                  verticalalignment="center",
                  fontsize=kwargs['fontsize_annot'],
                  color=colors_annot[0])

        # Get the formatter in case a string is supplied
        # if isinstance(fmt_annot, str):
        #     fmt_annot = ticker.StrMethodFormatter(fmt_annot)

        # Loop over the data and create a `Text` for each "pixel".
        # Change the text's color depending on the data.
        # texts = []
        for i in range(data.shape[dict_axes['y']]):
            for j in range(data.shape[dict_axes['x']]):
                if n_colors_annot == 2:
                    kw.update(color=colors_annot[int(im.norm(data[i, j]) > threshold)])

                annot_i_j = fmt_annot.format(array_annot[i, j])

                if annot_i_j[0] in ['-', '+']:
                    if annot_i_j[slice(1, 3, 1)] == '0.':
                        annot_i_j = annot_i_j[0] + annot_i_j[slice(2, None, 1)]
                else:
                    if annot_i_j[slice(0, 2, 1)] == '0.':
                        annot_i_j = annot_i_j[slice(1, None, 1)]



                text = im.axes.text(j, i, annot_i_j, **kw)
                # texts.append(text)

        # return texts


def heatmaps_in_1_figure(
        data, dict_axes=None, id_figure=None, array_annot=None, add_letters_to_titles=True,
        hspace=0.5, maximum_n_pixels_per_plot=500, **kwargs):

        # kwargs:
        # annot=False, fmt_annot='{:.2f}', fontsize_annot=None, colors_annot="black",
        # title=None, x_label=None, y_label=None,
        # xticklabels='auto', yticklabels='auto',
        # fontsize_title=None, rotation_title=None,
        # fontsize_x_label=None, rotation_x_label=None,
        # fontsize_y_label=None, rotation_y_label=None,
        # fontsize_xticklabels=None, rotation_xticklabels=None,
        # fontsize_yticklabels=None, rotation_yticklabels=None,
        # cmap=None, fontsize_cbar_ticklabels=None, cbarlabel=None, fontsize_cbarlabel=None):

    shape_data = np.asarray(data.shape, dtype=int)
    n_axes = shape_data.size
    if n_axes != 4:
        raise ValueError('data must have either 4 axes')

    keys_axes_expected = np.asarray(['rows', 'columns', 'y', 'x'], dtype=str)
    values_axes_expected = np.arange(n_axes)
    if dict_axes is None:
        dict_axes = dict(zip(keys_axes_expected, values_axes_expected))
    else:

        keys_axes, axes_data = cc_Formatter.dict_to_key_array_and_value_array(dict_axes)
        axes_negative = axes_data < 0
        axes_data[axes_negative] += n_axes
        for k in keys_axes[axes_negative]:
            dict_axes[k] += n_axes

        cc_Checker.keys_necessary_known_and_values_necessary_known_exist_and_other_keys_and_values_do_not_exist(
            dict_axes, keys_axes_expected, values_axes_expected, name_dictionary='dict_axes')
        cc_Checker.values_are_not_repeated(dict_axes, name_dictionary='dict_axes')

    axes_subplots = np.asarray([dict_axes['rows'], dict_axes['columns']], dtype=int)
    n_axes_subplots = axes_subplots.size
    n_rows, n_columns = shape_data[axes_subplots]
    axes_subplots = np.sort(axes_subplots)
    n_subplots_per_fig = n_rows * n_columns
    shape_subplots = shape_data[axes_subplots]

    from ccalafiore.combinations import n_conditions_to_combinations
    subplot_conbinations = n_conditions_to_combinations(shape_subplots)

    figures_existing = plt.get_fignums()
    n_figures_existing = len(figures_existing)
    if id_figure is None:
        i = 0
        while id_figure is None:
            if i in figures_existing:
                pass
            else:
                id_figure = i
            i += 1
    else:
        if id_figure in figures_existing:
            print('Warning: overwriting figure {}.'.format(id_figure))

    dict_axes_next = {}
    if dict_axes['y'] > dict_axes['x']:
        dict_axes_next['y'] = 1
        dict_axes_next['x'] = 0
    elif dict_axes['y'] < dict_axes['x']:
        dict_axes_next['y'] = 0
        dict_axes_next['x'] = 1

    dict_axes_in_kwargs = {}
    if dict_axes['rows'] > dict_axes['columns']:
        dict_axes_in_kwargs['rows'] = 1
        dict_axes_in_kwargs['columns'] = 0
    elif dict_axes['rows'] < dict_axes['columns']:
        dict_axes_in_kwargs['rows'] = 0
        dict_axes_in_kwargs['columns'] = 1


    if add_letters_to_titles:
        a_num = ord('a')
        addition = '*) '
        # len_addition = len(addition)
        if kwargs.get('title') is None:
            kwargs['title'] = addition
        elif isinstance(kwargs['title'], str):
            kwargs['title'] = addition + kwargs['title']
        elif (isinstance(kwargs['title'], np.ndarray) or
              isinstance(kwargs['title'], list) or
              isinstance(kwargs['title'], tuple)):

            if (isinstance(kwargs['title'], list) or
                    isinstance(kwargs['title'], tuple)):
                kwargs['title'] = np.asarray(kwargs['title'], dtype=str)

            if kwargs['title'].dtype.char != 'U':
                idx = np.empty(n_axes_subplots, dtype=int)
                idx[:] = 0
                if kwargs['title'][tuple(idx)] is None:
                    kwargs['title'] = addition
                else:
                    kwargs['title'] = np.char.add(addition, kwargs['title'].astype(str))

            else:
                kwargs['title'] = np.char.add(addition, kwargs['title'])
            # try:
            #     kwargs['title'] = np.char.add(addition, kwargs['title'])
            # except TypeError:
            #     kwargs['title'] = addition

        else:
            kwargs['title'] = np.char.add(
                addition, np.asarray(kwargs['title'], dtype=str))

    n_kwargs = len(kwargs)
    if n_kwargs > 0:
        kwargs = cc_Formatter.format_shape_arguments(kwargs, shape_subplots)
        index_kwargs = np.empty(n_axes_subplots, dtype=object)
        index_kwargs[:] = slice(None)

    if data.shape[dict_axes['x']] > data.shape[dict_axes['y']]:
        ratio_x = 1
        ratio_y = data.shape[dict_axes['y']] / data.shape[dict_axes['x']]
    elif data.shape[dict_axes['x']] < data.shape[dict_axes['y']]:
        ratio_x = data.shape[dict_axes['x']] / data.shape[dict_axes['y']]
        ratio_y = 1
    else:
        ratio_x = 1
        ratio_y = 1

    plt.figure(
        id_figure, frameon=False, dpi=my_dpi,
        figsize=(((maximum_n_pixels_per_plot * ratio_x) * n_columns) / my_dpi,
                 ((maximum_n_pixels_per_plot * ratio_y) * n_rows) / my_dpi))

    index = np.empty(n_axes, dtype=object)
    index[:] = slice(None)

    keys = kwargs.keys()
    if array_annot is None:
        for s in range(n_subplots_per_fig):

            ax = plt.subplot(n_rows, n_columns, s + 1)

            if n_kwargs > 0:
                index_kwargs[slice(0, n_axes_subplots)] = subplot_conbinations[s]
                if add_letters_to_titles:
                    kwargs['title'][tuple(index_kwargs)] = (
                        chr(a_num + s) + kwargs['title'][tuple(index_kwargs)][slice(1, None, 1)])

            index[axes_subplots] = subplot_conbinations[s]

            heatmap(
                data[tuple(index)], dict_axes=dict_axes_next, ax=ax,
                ** dict(zip(keys, [value[tuple(index_kwargs)] for value in kwargs.values()])))
    else:
        for s in range(n_subplots_per_fig):
            ax = plt.subplot(n_rows, n_columns, s + 1)

            if n_kwargs > 0:
                index_kwargs[slice(0, n_axes_subplots)] = subplot_conbinations[s]
                if add_letters_to_titles:
                    kwargs['title'][tuple(index_kwargs)] = (
                        chr(a_num + s) + kwargs['title'][tuple(index_kwargs)][slice(1, None, 1)])

            index[axes_subplots] = subplot_conbinations[s]

            heatmap(
                data[tuple(index)], dict_axes=dict_axes_next, ax=ax, array_annot=array_annot[tuple(index)],
                **dict(zip(keys, [value[tuple(index_kwargs)] for value in kwargs.values()])))

        # ax = sns.heatmap(
        #     data[f, s], annot=annot, fmt=fmt_annot[s], cmap=cmap[s],
        #     xticklabels=xticklabels,
        #     yticklabels=yticklabels,
        #     annot_kws=dict([('fontsize', fontsize_annot)]))
    plt.subplots_adjust(hspace=hspace)
    plt.tight_layout()
    # plt.show()
    # save_figure(id_figure=id_figure, directories=directories_images, formats=formats_images, hspace=hspace)


def heatmaps_in_multi_figures(
        data, dict_axes=None, id_figures=None, array_annot=None, hspace=0.5, add_letters_to_titles=True,
        maximum_n_pixels_per_plot=500, **kwargs):

    # keys =
    # [annot=False, fmt_annot='{:.2f}', fontsize_annot=None, colors_annot="black",
    # title=None, x_label=None, y_label=None,
    # xticklabels='auto', yticklabels='auto',
    # fontsize_title=None, rotation_title=None,
    # fontsize_x_label=None, rotation_x_label=None,
    # fontsize_y_label=None, rotation_y_label=None,
    # fontsize_xticklabels=None, rotation_xticklabels=None,
    # fontsize_yticklabels=None, rotation_yticklabels=None,
    # cmap=None, fontsize_cbar_ticklabels=None, cbarlabel=None, fontsize_cbarlabel=None]

    shape_data = np.asarray(data.shape, dtype=int)
    n_axes = shape_data.size
    if n_axes != 5:
        raise ValueError('data must have either 5 axes')

    keys_axes_expected = np.asarray(['figures', 'rows', 'columns', 'y', 'x'], dtype=str)
    values_axes_expected = np.arange(n_axes)
    if dict_axes is None:
        dict_axes = dict(zip(keys_axes_expected, values_axes_expected))
    else:

        keys_axes, axes_data = cc_Formatter.dict_to_key_array_and_value_array(dict_axes)
        axes_negative = axes_data < 0
        axes_data[axes_negative] += n_axes
        for k in keys_axes[axes_negative]:
            dict_axes[k] += n_axes

        cc_Checker.keys_necessary_known_and_values_necessary_known_exist_and_other_keys_and_values_do_not_exist(
            dict_axes, keys_axes_expected, values_axes_expected, name_dictionary='dict_axes')
        cc_Checker.values_are_not_repeated(dict_axes, name_dictionary='dict_axes')

    axes_subplots = np.asarray([dict_axes['figures'], dict_axes['rows'], dict_axes['columns']], dtype=int)
    n_axes_subplots = axes_subplots.size
    n_figures, n_rows, n_columns = shape_data[axes_subplots]
    axes_subplots = np.sort(axes_subplots)
    shape_subplots = shape_data[axes_subplots]

    figures_existing = plt.get_fignums()
    # n_figures_existing = len(figures_existing)
    if id_figures is None:
        id_figures = [None] * n_figures
        i = 0
        f = 0
        while f < n_figures:
            if i in figures_existing:
                pass
            else:
                id_figures[f] = i
                f += 1
            i += 1
    else:
        for f in id_figures:
            if f in figures_existing:
                print('Warning: overwriting figure {}.'.format(f))

    dict_axes_next = {}
    for k in dict_axes:
        if k == 'figures':
            continue
        if dict_axes[k] < dict_axes['figures']:
            dict_axes_next[k] = dict_axes[k]
        elif dict_axes[k] > dict_axes['figures']:
            dict_axes_next[k] = dict_axes[k] - 1
        else:
            raise ValueError('\n\tThe following condition is not met:\n'
                             '\t\tdict_axes[\'{}\'] \u2260 dict_axes[\'figures\']'.format(k))

    axis_figures_in_kwargs = 0
    if dict_axes['figures'] > dict_axes['rows']:
        axis_figures_in_kwargs += 1
    if dict_axes['figures'] > dict_axes['columns']:
        axis_figures_in_kwargs += 1

    dict_arguments = cc_Formatter.format_shape_arguments(
        dict(hspace=hspace, add_letters_to_titles=add_letters_to_titles,
             maximum_n_pixels_per_plot=maximum_n_pixels_per_plot), [n_figures])

    hspace = dict_arguments['hspace']
    add_letters_to_titles = dict_arguments['add_letters_to_titles']
    maximum_n_pixels_per_plot = dict_arguments['maximum_n_pixels_per_plot']


    n_kwargs = len(kwargs)
    if n_kwargs > 0:
        kwargs = cc_Formatter.format_shape_arguments(kwargs, shape_subplots)
        index_kwargs = np.empty(n_axes_subplots, dtype=object)
        index_kwargs[:] = slice(None)

        # if array_annot is None:
        #     array_annot = kwargs.update(array_annot=array_annot)

    index = np.empty(n_axes, dtype=object)
    index[:] = slice(None)

    keys = kwargs.keys()

    if array_annot is None:

        for f in range(n_figures):

            if n_kwargs > 0:
                index_kwargs[axis_figures_in_kwargs] = f

            index[dict_axes['figures']] = f

            heatmaps_in_1_figure(
                data[tuple(index)], dict_axes=dict_axes_next, id_figure=id_figures[f],
                hspace=hspace[f], maximum_n_pixels_per_plot=maximum_n_pixels_per_plot[f],
                add_letters_to_titles=add_letters_to_titles[f],
                ** dict(zip(keys, [value[tuple(index_kwargs)] for value in kwargs.values()])))
    else:

        for f in range(n_figures):

            if n_kwargs > 0:
                index_kwargs[axis_figures_in_kwargs] = f

            index[dict_axes['figures']] = f

            heatmaps_in_1_figure(
                data[tuple(index)], dict_axes=dict_axes_next, id_figure=id_figures[f],
                array_annot=array_annot[tuple(index)],
                hspace=hspace[f], maximum_n_pixels_per_plot=maximum_n_pixels_per_plot[f],
                add_letters_to_titles=add_letters_to_titles[f],
                ** dict(zip(keys, [value[tuple(index_kwargs)] for value in kwargs.values()])))

    # if n_subplots_per_fig == 1:

    # plt.show()
    # save_figure(id_figures=id_figures, directories=directories_images, formats=formats_images, hspace=hspace)


def save_figure(id_figures=None, directories=None, formats=['svg']):
    # def save_figure(id_figures=None, directories=None, formats=['svg'], hspace=0.5):

    if id_figures is None:
        id_figures = plt.get_fignums()

    n_figures = len(id_figures)

    if directories is None:
        directories = id_figures
    else:
        if not (isinstance(directories, np.ndarray) or
                isinstance(directories, list) or
                isinstance(directories, tuple)):
            directories = [directories]
        
        n_directories = len(directories)
        if n_figures != n_directories:
            raise ValueError('n_figures and n_directories must be equal.\n'
                             'Now, n_figures = {} and n_directories = {}'.format(n_figures, n_directories))

    # my_dpi = 100
    n_formats = len(formats)
    for i in range(n_figures):

        plt.figure(id_figures[i])

        for j in range(n_formats):
            # plt.subplots_adjust(hspace=hspace)
            directory_i_j = '.'.join([directories[i], formats[j]])
            plt.savefig(directory_i_j, format=formats[j], bbox_inches='tight', pad_inches=0.0, dpi=my_dpi)
