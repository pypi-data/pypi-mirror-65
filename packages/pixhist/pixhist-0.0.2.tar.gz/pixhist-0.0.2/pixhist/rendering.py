""" Functions that might be slightly more convenient than using Matplotlib directly.
"""
try:
    import matplotlib.pyplot as plt
except ModuleNotFoundError:
    MESSAGE = """
Module Matplotlib not found.
To use pixhist.rendering please install Matplotlib.
E.g. `pip install matplotlib` or `conda install matplotlib`.
"""
    print(MESSAGE)


def plot(array2d, cmap="inferno", savepath=None, scale_save=1.0):
    """Turn 2D array into matplotlib plot. Returns `fig, im`."""
    DPI = 80
    fig = plt.figure(figsize=(array2d.shape[1] / DPI, array2d.shape[0] / DPI))
    ax = plt.Axes(fig, [0.0, 0.0, 1.0, 1.0])
    ax.set_axis_off()
    fig.add_axes(ax)
    im = ax.imshow(array2d, aspect="equal", origin="lower", cmap=cmap)
    if savepath:
        plt.savefig(savepath, dpi=DPI * scale_save)
    return fig, im


def update_plot(array2d, fig, im):
    """Update an already existing plot (if array2d of same size)."""
    im.set_data(array2d)
    fig.canvas.draw()


def cmap_list():
    """List of Matplotlib cmaps (alias of plt.colormaps() )"""
    return plt.colormaps()
