"""Plotting of spatial/3D data."""

from bokeh.models import ColorBar, LinearColorMapper, Range1d
from bokeh.palettes import Blues9
from bokeh.plotting import figure
from bokeh.transform import linear_cmap, log_cmap
from bokeh.util.hex import hexbin

from aplanat import util


def heatmap(x, y, z, name=None, **kwargs):
    """Create a heatmap from three columns.

    :param x: x-axis coordinates.
    :param y: y-axis coordinates.
    :param z: z-axis coordinates (e.g. counts or frequencies).
    :param name: title for z-axis.
    :param kwargs: kwargs for bokeh figure.

    :returns: a bokeh plot.

    """
    data = {'x': x, 'y': y, 'z': z}

    defaults = {
        "output_backend": "webgl",
        "height": 300, "width": 600}
    defaults.update(kwargs)
    p = figure(**defaults)

    # define a colour map
    colors = Blues9[::-1]
    mapper = LinearColorMapper(
        palette=colors, low=min(data['z']), high=max(data['z']))

    # plot heatmap rectangles
    p.rect(
        source=data, x="x", y="y", width=1, height=1,
        fill_color={'field': 'z', 'transform': mapper},
        line_color=None)

    # add colour scale
    color_bar = ColorBar(
        title=name, color_mapper=mapper, label_standoff=10,
        location=(0, 0))
    p.add_layout(color_bar, 'right')

    # hide some plotting artefacts
    p.x_range.range_padding = 0
    p.y_range.range_padding = 0
    p.xaxis.visible = False
    p.yaxis.visible = False
    # set up the axes
    xbounds = util.pad(data['x'])
    ybounds = util.pad(data['y'])
    p.x_range = Range1d(start=xbounds[0], end=xbounds[1], bounds=xbounds)
    p.y_range = Range1d(start=ybounds[0], end=ybounds[1], bounds=ybounds)
    return p


def hexmap(
        x, y, name=None, log=False, match_aspect=True, kernel_size=0.1,
        xlim=(None, None), ylim=(None, None), **kwargs):
    """Create a heatmap from two columns.

    :param x: x-axis coordinates.
    :param y: y-axis coordinates.
    :param name: title for z-axis.
    :param kwargs: kwargs for bokeh figure.

    :returns: a bokeh plot.

    """
    bins = hexbin(x, y, kernel_size)

    defaults = {
        "output_backend": "webgl",
        "height": 400, "width": 500,
        "background_fill_color": "#440154"}
    defaults.update(kwargs)
    p = figure(**defaults)

    cmap = log_cmap if log else linear_cmap
    mapper = cmap('counts', 'Viridis256', 0, max(bins.counts))
    p.hex_tile(
        q="q", r="r", size=kernel_size, line_color=None, source=bins,
        fill_color=mapper)

    color_bar = ColorBar(
        title="observations", color_mapper=mapper['transform'],
        label_standoff=10, location=(0, 0))
    p.add_layout(color_bar, 'right')
    p.grid.visible = False

    x_lim = util.Limiter().accumulate(x).fix(*xlim)
    y_lim = util.Limiter().accumulate(y).fix(*ylim)
    # limit the display range
    p.x_range = Range1d(
        start=x_lim.min, end=x_lim.max, bounds=(x_lim.min, x_lim.max))
    p.y_range = Range1d(
        start=y_lim.min, end=y_lim.max, bounds=(y_lim.min, y_lim.max))
    return p, bins
