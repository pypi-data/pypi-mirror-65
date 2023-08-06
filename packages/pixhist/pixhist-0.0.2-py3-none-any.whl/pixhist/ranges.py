""" Functions that deal with ranges that aren't exposed directly in API.
"""
from numba import njit


@njit
def make_xy_proportional_in_window(width, height, x_low, x_high, y_low, y_high):
    """Pad the x or y range to keep x and y proportional to each other in the window.
    
    Parameters
    ----------
    width : int
        The width of the window,
        equivalent to the number of bins on the x dimension.
    height : int
        The height of the window,
        equivalent to the number of bins on the y dimension.
    x_low : float
        The position of the left edge of the window, 
        equivalent to the lower range of the x bins.
        E.g. x_vals.min().
    x_high : float
        The position of the right edge of the window, 
        equivalent to the lower range of the x bins.
        E.g. x_vals.max().
    y_low : float
        The position of the bottom edge of the window, 
        equivalent to the lower range of the y bins.
        E.g. y_vals.min().
    y_high : float
        The position of the top edge of the window, 
        equivalent to the upper range of the y bins.
        E.g. y_vals.max().

    Returns
    -------
    x_low_, x_high_, y_low_, y_high_ : float, float, float, float
        The new, padded, ranges, that allow the window to fit to 
        the x and y ranges, while keeping x and y to scale
        with each other.

    Notes
    -----
    There are three possibilities:
    case 1:
        No padding needs to be done.
    case 2:
        The x range is scaled to the full window width.
        The y range is padded, to keep y to scale with x.
    case 3:
        The y range is scaled to the full window height.
        The x range is padded, to keep x to scale with y.

    """
    delta_x = x_high - x_low
    delta_y = y_high - y_low

    if delta_x == 0 or delta_y == 0:
        return x_low, x_high, y_low, y_high
    elif delta_y / delta_x < height / width:
        k = 0.5 * (delta_x * height / width - delta_y)
        return x_low, x_high, y_low - k, y_high + k
    else:
        k = 0.5 * (delta_y * width / height - delta_x)
        return x_low - k, x_high + k, y_low, y_high


@njit
def scale_range_1d(low, high, amount):
    """Multiply range by `amount`, keeping the range centered."""
    span = high - low
    center = low + span / 2
    new_span = amount * span
    return center - new_span / 2, center + new_span / 2


@njit
def pad_range_1d(low, high, amount):
    """Pad range by `amount`, keeping the range centered."""
    pad = amount / 2
    return low - pad, high + pad


@njit
def shift_range_1d(low, high, amount):
    "Shift range by `amount`."
    return low + amount, high + amount
