"""Simple bokeh plotting API."""

import bokeh.io as bkio
from bokeh.layouts import gridplot


__version__ = '0.0.4'


class Grid(list):
    """Create a list of lists of fixed length."""

    def __init__(self, width=4):
        """Initialize the Grid."""
        self.width = width
        self.append(list())

    def add(self, item):
        """Add an item to the grid.

        :param item: item to add

        """
        self[-1].append(item)
        if len(self[-1]) == self.width:
            self.append(list())

    def extend(self, items):
        """Add multiple items.

        :param items: items to add.

        """
        for item in items:
            self.add(item)


def show(plot):
    """Show a plot in a notebook."""
    bkio.output_notebook(hide_banner=True)
    bkio.show(plot)


def grid(plots, ncol=4):
    """Show a grid of plots in a notebook.

    :param plots: a list of bokeh plots.
    :param ncol: number of columns.

    """
    grid = Grid(width=ncol)
    grid.extend(plots)
    plot = gridplot(grid)
    show(plot)
