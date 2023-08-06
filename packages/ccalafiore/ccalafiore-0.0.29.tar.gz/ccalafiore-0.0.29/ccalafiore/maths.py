from numbers import *
import numpy as np
import math


def factors_of_x(x, y=1):
    type_x = type(x)
    type_y = type(y)

    x_is_integer = isinstance(x, Integral)

    # The Numeric abstract base classes:
    # numbers.Complex
    # numbers.Real
    # numbers.Integral
    # numbers.Number

    if not x_is_integer:
        raise Exception('x must be ab integer. Now, type_x = {}'.format(type_x))

    y_is_integer = isinstance(y, Integral)
    if not y_is_integer:
        raise Exception('y must be ab integer. Now, type_y = {}'.format(type_y))

    factors = np.empty(0, int)

    for i in range(y, x + 1):
        if x % i == 0:
            factors = np.append(factors, i)

    return factors


def gamma(z):
    
    print('scipy.special.gamma(z) is more efficient')
    
    pos_inf = 100
    n_dx = 10000000
    dx = pos_inf / n_dx

    if not isinstance(z, np.ndarray):
        z = np.asarray(z)

    n_axes_z = len(z.shape)
    n_axes_x = n_axes_z + 1
    axis_delta = n_axes_x - 1
    x = np.arange(0, pos_inf, dx)
    while len(x.shape) < n_axes_x:
        x = np.expand_dims(x, axis=0)

    if n_axes_z > 0:
        z = np.expand_dims(z, axis_delta)

    with np.errstate(divide='ignore'):
        return np.sum(
            np.power(x, z - 1) * np.power(math.e, -x) * dx, axis=axis_delta)
