"""Main API of PixHist.
"""
from numba import njit
import numpy as np
from pixhist.histogram import hist_from_generator, hist_from_arrays
from pixhist import ranges


def from_gen(
    generator, n_iter, width, height, range, make_xy_proportional=False, log=False
):
    """Create a 2D histogram with `width * height` bins from `generator`.

    The generator should be compiled using Numba's `njit` or `jit`.

    Parameters
    ----------
    generator : generator() -> x, y
        A generator that takes no arguments, and that returns the values x, y.
        Compiled with Numba's njit / jit.
    n_iter : int
        The number of times to iterate the generator.
    width : int
        The number of bins/pixels on the x dimension.
    height : int
        The number of bins/pixels on the y dimension.
        
    range : array_like, shape (2,2), optional
        Optionally provide ranges for x and y,
        as range = [[x_low, x_high], [y_low, y_high]].
        Otherwise will use the min and max values from x_vals, y_vals.
    make_xy_proportional : bool, optional
        If true, makes x and y ranges proportional to eachother.
        Otherwise they will be stretched to fill the window.
    log : bool
        If true, returns the log of the histogram:
        log(hist + 1)

    Returns
    -------
    hist : array_like, shape (W,H)
        The histogram.

    """

    if make_xy_proportional:
        range = make_ranges_proportional(range, width, height)

    (x_low, x_high), (y_low, y_high) = range

    hist, x, y = hist_from_generator(
        generator, n_iter, width, height, x_low, x_high, y_low, y_high
    )

    if log:
        hist = np.log(hist + 1)

    return hist


def from_gen_f(
    generator, n_iter, width, height, range, make_xy_proportional=False, log=False
):
    """Same as `from_gen` but also return final `x, y` values.

    Parameters
    ----------
    generator : generator() -> x, y
        A generator that takes no arguments, and that returns the values x, y.
        Compiled with Numba's njit / jit.
    n_iter : int
        The number of times to iterate the generator.
    width : int
        The number of bins/pixels on the x dimension.
    height : int
        The number of bins/pixels on the y dimension.
        
    range : array_like, shape (2,2), optional
        Optionally provide ranges for x and y,
        as range = [[x_low, x_high], [y_low, y_high]].
        Otherwise will use the min and max values from x_vals, y_vals.
    make_xy_proportional : bool, optional
        If true, makes x and y ranges proportional to eachother.
        Otherwise they will be stretched to fill the window.
    log : bool
        If true, returns the log of the histogram:
        log(hist + 1)

    Returns
    -------
    hist : array_like, shape (W,H)
        The histogram.
    (x_f, y_f) : array_like, shape (2,)
        The final `x, y` values outputted by the generator.

    """

    if make_xy_proportional:
        range = make_ranges_proportional(range, width, height)

    (x_low, x_high), (y_low, y_high) = range

    hist, x, y = hist_from_generator(
        generator, n_iter, width, height, x_low, x_high, y_low, y_high
    )

    if log:
        hist = np.log(hist + 1)

    return hist, (x, y)


def from_arrays(
    x_vals, y_vals, width, height, range=None, make_xy_proportional=True, log=False
):
    """Create a 2D histogram with `width * height` bins from 1D arrays `x_vals`, `y_vals`.

    The bins are equally spaced along a given axis.

    Parameters
    ----------
    x_vals : array_like, shape (N,)
        The x values to be histogrammed.
    y_vals : array_like, shape (N,)
        The y values to be histogrammed.
    width : int
        The number of bins/pixels on the x dimension.
    height : int
        The number of bins/pixels on the y dimension.

    range : array_like, shape (2,2), optional
        Optionally provide ranges for x and y,
        as range = [[x_low, x_high], [y_low, y_high]].
        Otherwise will use the min and max values from x_vals, y_vals.
    make_xy_proportional : bool, optional
        If true, makes x and y proportional to eachother.
        Otherwise they will be stretched to fill the window.
    log : bool
        If true, returns the log of the histogram:
        log(hist + 1)

    Returns
    -------
    hist : array_like, shape (W,H)
        The histogram.

    """
    if not range:
        range = [[x_vals.min(), x_vals.max()], [y_vals.min(), y_vals.max()]]

    if make_xy_proportional:
        range = make_ranges_proportional(range, width, height)

    (x_low, x_high), (y_low, y_high) = range
    hist = hist_from_arrays(x_vals, y_vals, width, height, x_low, x_high, y_low, y_high)

    if log:
        hist = np.log(hist + 1)

    return hist


@njit
def estimate_range(generator, n_iter=10_000):
    """Estimate the range of a generator, by iterating through the first `n_iter` values

    Parameters
    ----------
    generator : generator() -> x, y
        A generator that takes no arguments, and that returns the values x, y.
        Highly recommended to first compile the generator with Numba's njit / jit.
    n_iter : int
        The number of times to iterate the generator.

    Returns
    -------
    range : array_like, shape (2,2)
        The range of the first `n_iter` values:
        [[x_min, x_max], [y_min, y_max]]

    """
    x_min = y_min = np.inf
    x_max = y_max = -np.inf
    iterable = generator()
    for _ in range(n_iter):
        x, y = next(iterable)
        if x < x_min:
            x_min = x
        if x > x_max:
            x_max = x
        if y < y_min:
            y_min = y
        if y > y_max:
            y_max = y
    return [[x_min, x_max], [y_min, y_max]]


def scale_range(range, amount):
    """ Scale a 2D range. Multiplicative scaling, e.g. amount=2 doubles the ranges.

    Parameters
    ----------
    range : array_like, shape (2,2)
        A range in the form: [[x_low, x_high], [y_low, y_high]]
    amount : float or array_like (2,)
        Either a single value to scale both x and y,
        or [amount_x, amount_y].

    Returns
    -------
    range_ : array_like, shape (2,2)
        The scaled range.

    """
    try:
        amount_x, amount_y = amount
        range[0] = ranges.scale_range_1d(range[0][0], range[0][1], amount_x)
        range[1] = ranges.scale_range_1d(range[1][0], range[1][1], amount_y)
    except TypeError:
        range[0] = ranges.scale_range_1d(range[0][0], range[0][1], amount)
        range[1] = ranges.scale_range_1d(range[1][0], range[1][1], amount)
    return range


def pad_range(range, amount):
    """ Pad a 2D range.

    Parameters
    ----------
    range : array_like, shape (2,2)
        A range in the form: [[x_low, x_high], [y_low, y_high]]
    amount : float or array_like (2,)
        Either a single value to pad both x and y,
        or [amount_x, amount_y].

    Returns
    -------
    range_ : array_like, shape (2,2)
        The padded range.

    """
    try:
        amount_x, amount_y = amount
        range[0] = ranges.pad_range_1d(range[0][0], range[0][1], amount_x)
        range[1] = ranges.pad_range_1d(range[1][0], range[1][1], amount_y)
    except TypeError:
        range[0] = ranges.pad_range_1d(range[0][0], range[0][1], amount)
        range[1] = ranges.pad_range_1d(range[1][0], range[1][1], amount)
    return range


def shift_range(range, amount):
    """ Shift a 2D range.

    Parameters
    ----------
    range : array_like, shape (2,2)
        A range in the form: [[x_low, x_high], [y_low, y_high]]
    amount : float or array_like (2,)
        Either a single value to shift both the x and y,
        or [amount_x, amount_y].

    Returns
    -------
    range_ : array_like, shape (2,2)
        The shifted range.

    """
    try:
        amount_x, amount_y = amount
        range[0] = ranges.shift_range_1d(range[0][0], range[0][1], amount_x)
        range[1] = ranges.shift_range_1d(range[1][0], range[1][1], amount_y)
    except TypeError:
        range[0] = ranges.shift_range_1d(range[0][0], range[0][1], amount)
        range[1] = ranges.shift_range_1d(range[1][0], range[1][1], amount)
    return range


def make_ranges_proportional(range, width, height):
    """ Make the x range and y range stay proportional to each other, while fitting to the window.

    Do this by padding one of the ranges, such that the both ranges fit to the window 
    without clipping.
    
    Parameters
    ----------
    range : array_like, shape (2,2)
        A range in the form: [[x_low, x_high], [y_low, y_high]]
    width : int
        The number of bins/pixels on the x dimension.
    height : int
        The number of bins/pixels on the y dimension.

    Returns
    -------
    range_ : array_like, shape (2,2)
        The modified range.

    """
    (x_low, x_high), (y_low, y_high) = range
    x_low, x_high, y_low, y_high = ranges.make_xy_proportional_in_window(
        width, height, x_low, x_high, y_low, y_high
    )
    return [[x_low, x_high], [y_low, y_high]]
