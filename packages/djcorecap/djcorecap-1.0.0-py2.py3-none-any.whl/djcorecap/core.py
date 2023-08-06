# -*- coding: utf-8 -*-

'''
djcorecap/core
---------------

core module for the djcorecap app
'''


from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import CDN


def bokeh_plot(data, plots, f_config={}, p_config=[]):
    '''
    create HTML elements for a Bokeh plot

    :returns: `str`, `str` with script and div data for HTML rendering
    :param data: a `dict` of `dict`s where {field: {x: y, ... }, ... }
    :param plots: a `list` of (`str`, `str`, `dict`) `tuples`
                  identifying (field, type, s_config) for each plot series
    :param f_config: a `dict` with Bokeh figure settings
    :param p_config: a `list` of (`str`, `str`, `str`) `tuples`
                     with Bokeh figure settings post-instantiation
    '''

    plot = figure(**f_config)

    for field, _type, s_config in plots:

        # get x, y values from data
        x, y = zip(*data[field].items())

        # plot the series
        getattr(plot, _type)(x, y, legend=field, **s_config)

    for attr, field, value in p_config:
        setattr(getattr(plot, attr), field, value)

    return components(plot, CDN)  # script, div


def inject_plot(context_data, data, plot_config):
    '''
    inject Bokeh plot HTML elements into django view

    :returns: django `context` with injected 'bokeh_script', 'bokeh_div' fields
    :param context_data: django `context` object
    :param data: see `bokeh_plot`
    :param plot_config: `dict` with 'plots', 'f_config', 'p_config'
    '''

    bokeh_script = context_data.get('bokeh_script', '')
    bokeh_div = context_data.get('bokeh_div', '')

    for label, chart in plot_config.items():

        script, div = bokeh_plot(
            data,
            chart['plots'],
            chart['f_config'],
            chart['p_config'],
        )

        bokeh_script += script
        bokeh_div += div

    context_data['bokeh_script'] = bokeh_script
    context_data['bokeh_div'] = bokeh_div

    return context_data


def api_get_xy(source, obj=None, keys_method=None, values_method=None):
    '''
    get x: y data from an api endpoint

    :returns: `obj`, `obj` tuple
    :param source: either a `str` url or a django view
    :param obj: object to use for x and y vectors
    :param x_method: `list` of `str` method(s) to call on x object
    :param y_method: `list` of `str` method(s) to call on y object
    '''

    pass
