""" Histogram functions that aren't exposed directly in API.
This is where the histograms are actually computed.
"""
from numba import njit
import numpy as np


@njit
def hist_from_generator(generator, n_iter, width, height, x_low, x_high, y_low, y_high):
    """Create 2D histogram, from a generator, with bins equally spaced for a given axis.

    Parameters
    ----------
    generator : generator
        A numba compiled generator with no args, that returns `x, y`.
    width : int
        The number of bins on the x dimension.
    height : int
        The number of bins on the y dimension.
    x_low : float
        The lower range of the x bins. E.g. x_vals.min().
    x_high : float
        The upper range of the x bins. E.g. x_vals.max().
    y_low : float
        The lower range of the y bins. E.g. y_vals.min().
    y_high : float
        The upper range of the y bins. E.g. y_vals.max().

    Returns
    -------
    grid : ndarray, shape(height, width)
        The 2D array containing the counts. I.e. the histogram.
    """
    iterable = generator()
    grid = _make_grid(width, height)
    for _ in range(n_iter):
        x, y = next(iterable)
        x_bin = _get_bin(x, x_low, x_high, width)
        y_bin = _get_bin(y, y_low, y_high, height)
        _increment_grid(grid, x_bin, y_bin)
    return grid, x, y


@njit
def hist_from_arrays(x_vals, y_vals, width, height, x_low, x_high, y_low, y_high):
    """Create 2D histogram, from `x_vals`, `y_vals`, with bins equally spaced for a given axis.

    Parameters
    ----------
    x_vals : array_like, shape (N,)
        The x values to be histogrammed.
    y_vals : array_like, shape (N,)
        The y values to be histogrammed.
    width : int
        The number of bins on the x dimension.
    height : int
        The number of bins on the y dimension.
    x_low : float
        The lower range of the x bins. E.g. x_vals.min().
    x_high : float
        The upper range of the x bins. E.g. x_vals.max().
    y_low : float
        The lower range of the y bins. E.g. y_vals.min().
    y_high : float
        The upper range of the y bins. E.g. y_vals.max().

    Returns
    -------
    grid : ndarray, shape(height, width)
        The 2D array containing the counts. I.e. the histogram.
    """
    grid = _make_grid(width, height)
    for i in range(len(x_vals)):
        x, y = x_vals[i], y_vals[i]
        x_bin = _get_bin(x, x_low, x_high, width)
        y_bin = _get_bin(y, y_low, y_high, height)
        _increment_grid(grid, x_bin, y_bin)
    return grid


@njit
def _get_bin(x, low, high, num_bins):
    """Returns bin number for value `x`, in 1D histogram defined by `low`, `high`, `num_bins`.

    There are `num_bins` bins, spaced evenly between `low` and `high`.
    The right most edge is put into bin: num_bins - 1.
    BEWARE: will return value outside the range [0, num_bins-1] 
    if `x` is outside the inclusive range [low, high].
    
    Parameters
    ----------
    x : float
        A value to be placed into a bin.
    low : float
        The lower range of the bins. E.g. x_vals.min().
    high : float
        The upper range of the bins. E.g. x_vals.max().
    num_bins : int
        The number of bins.

    Returns
    -------
    bin_number : int
        The bin number for `x` 
        (value can be outside the range [0, n_bins-1]).

    """
    if x == high:
        return num_bins - 1
    else:
        return int(num_bins * (x - low) / (high - low))


@njit
def _make_grid(width, height):
    """Returns a 2D numpy array of zeros."""
    return np.zeros(shape=(height, width))


@njit
def _increment_grid(grid, x_idx, y_idx):
    """Increment element of 2D array `grid`, in place, if `x_idx`, `y_idx` within grid."""
    if 0 <= x_idx < grid.shape[1] and 0 <= y_idx < grid.shape[0]:
        grid[y_idx, x_idx] += 1


def hist_from_arrays_np(
    x_vals, y_vals, width, height, x_low=None, x_high=None, y_low=None, y_high=None
):
    """ Compute histogram from values, using NumPy function np.histogram2d.

    Useful for testing correctness, and speed comparisons.
    https://docs.scipy.org/doc/numpy/reference/generated/numpy.histogram2d.html
    """
    if x_low and x_high and y_low and y_high:
        range = [[x_low, x_high], [y_low, y_high]]
    else:
        range = None
    # np.histogram2d puts first argument on axis 0.
    return np.histogram2d(y_vals, x_vals, bins=(height, width), range=range)[0]
