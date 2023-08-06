"""Class for functions to fit"""
import inspect
import numpy as np

from typing import Callable


class BaseFitFunction:
    r"""
    Base class for fit functions.
    """

    def __init__(self, fit_func: Callable, integrate_func: Callable):
        r"""
        Initialize a new fit function by giving a fit functions in its original form and in its
        integrated from a constant (recommended is 1) to *b*.

        :param fit_func: Fit function, takes at least 2 arguments: 1) days since install 2+)
        parameters for fitting. Each parameter must be a new input variable.
        :param integrate_func: Fit function from 1 to *b*. Takes exactly 2 inputs, *b* and a list
        of parameters.
        """
        self.fit_func = fit_func
        self.integrate_func = integrate_func

        sig = inspect.signature(fit_func)
        n_params = [p.name for p in sig.parameters.values()].__len__() - 1
        self.fit_start_guess = [1] * n_params

    def __call__(self, t: np.ndarray, *args) -> np.ndarray:
        r"""
        Given a list of days since install it returns retention according to the function and
        parameter values.

        :param t: Days dince install
        :param args: Additional arguments to be passed to the fit function.
        :return: Retention values.
        """
        return self.fit_func(t, *args)

    def integrate(self, b=180, **kwargs) -> float:
        r"""
        Calculates the integral of the fit function from a constant (suggested is 1) to *b*.
        Additional arguments are parameter values.

        :param b: Last day since install value.
        :param kwargs: Parameter values.
        :return: Integrated value over the fit function.
        """
        return self.integrate_func(b, **kwargs)


def power_fit(t: np.ndarray, p0: float, p1: float):
    r"""
    Power function for fitting. Identifier is *power*.

    .. math::
        f(x) = k_1x^{k_2}

    :param t: Days since install.
    :param p0: Constant.
    :param p1: Constant.
    :return: Result of applying the power function to *t*.
    """
    return p0 * np.power(t, p1)


def power_integrate(b: int, fit_params: np.ndarray):
    r"""
    The integral over a power function

    .. math::
        \int^a_b f(x) dx = \frac{k_1}{k_2+1}\left( b^{ k_2 + 1} - a^{k_2 + 1}\right)

    :param b: The last day since install.
    :param fit_params: The parameter values.
    :return:
    """
    if not isinstance(b, int):
        raise TypeError('b must be an integer')
    if b < 1:
        raise ValueError('b must be bigger than 1')
    return fit_params[0] / (fit_params[1] + 1) * (
        b ** (fit_params[1] + 1) - 1 ** (fit_params[1] + 1)) + 1


power = BaseFitFunction(power_fit, power_integrate)
