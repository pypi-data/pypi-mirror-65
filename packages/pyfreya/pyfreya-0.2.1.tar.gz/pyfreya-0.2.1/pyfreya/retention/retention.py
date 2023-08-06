r"""

.. include:: tutorials/retention/Retention_Example.rst

Retention Class
===============
"""

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import pandas as pd
import pickle
import sys

from scipy.optimize import curve_fit
from loguru import logger
from typing import List, Union, Callable
from pyfreya.retention.fit_functions import power
from uncertainties.core import Variable, correlated_values
from uncertainties.unumpy import nominal_values, std_devs

plt.style.use('ggplot')
font = {'size': 20}

matplotlib.rc('font', **font)


class Retention:
    r"""
    Retention class Start
    """

    def __init__(self,
                 days_since_install: List[int],
                 retention_values: List[Union[float, Variable]]):
        r"""
        Initializes the retention class by setting retention values and corresponding days since
        install values. Retention values can either be values below 1 like 0.8 or in hundreds like
        80, both denoting 80%.

        :param retention_values: Retention values.
        :param days_since_install:
        """
        self.logger = logger
        try:
            self.logger.remove()
        except ValueError:
            pass
        finally:
            self.logger.add(sys.stderr, level='INFO')
        logger.disable(__name__)

        if isinstance(retention_values[0], Variable):
            retention_values = np.array(retention_values)
        else:
            retention_values = pd.to_numeric(retention_values)
        days_since_install = pd.to_numeric(days_since_install)
        assert len(retention_values) == len(days_since_install), \
            'retention values and days since install must have equal length.'

        if retention_values[0] > 1:
            self.logger.debug('Normalizing retention values')
            retention_values = retention_values / 100
        if (retention_values > 1).sum() > 0:
            self.logger.error('retention value determination error')
            raise ValueError(
                'There are retention values above one - is input values of mixed notation? '
                '(10 and 0.1 for 10%)')

        if std_devs(retention_values).sum() > 0:
            std = std_devs(retention_values)
        else:
            std = None

        self.fit_data = {'dsi': days_since_install,
                         'ret': nominal_values(retention_values),
                         'ret_unc': std
                         }
        self.df_retention = pd.DataFrame(data=retention_values,
                                         index=days_since_install,
                                         columns=['Retention'])
        self.df_retention.index.name = 'DaysSinceInstall'

        self.fit_func = power
        self.fitted_params = np.array([])

    def __call__(self, days_since_install: Union[list, np.ndarray]) -> np.ndarray:
        r"""
        Returns retention from a fitted function for the days given in *days_since_install*.

        :param days_since_install: Days since install that retention is to be calculated for.
        :return: Retention.
        """
        self.logger.debug('Calling retention func')
        return self.fit_func(days_since_install, *self.fitted_params)

    def __str__(self):
        r"""
        Print the dataframe with retention as percent. This is done here with specific options for
        width and length, therefore, return is emtpy.
        :return: Empty string.
        """
        retention_print = self.df_retention.copy()
        retention_print['Retention'] = retention_print['Retention'].map('{0:3.1%}'.format)
        if 'RetentionFit' in retention_print.columns:
            retention_print['RetentionFit'] = retention_print['RetentionFit'].map('{0:3.1%}'.format)
        with pd.option_context('display.max_rows', 40, 'display.max_columns', None,
                               'display.width', 200):
            return retention_print.__str__()

    def __repr__(self):
        r"""
        Print the dataframe with retention as percent. This is done here with specific options for
        width and length, therefore, return is emtpy.
        :return: Empty string.
        """
        retention_print = self.df_retention.copy()
        retention_print['Retention'] = retention_print['Retention'].map('{0:3.1%}'.format)
        if 'RetentionFit' in retention_print.columns:
            retention_print['RetentionFit'] = retention_print['RetentionFit'].map('{0:3.1%}'.format)
        with pd.option_context('display.max_rows', 40, 'display.max_columns', None,
                               'display.width', 200):
            return retention_print.__str__()

    def fit(self, function: Union[str, Callable] = 'power', **kwargs):
        r"""
        Fits given values to a function. *function* can either be an identifier (string) of these:

        * *power*: Calls a power function.

        *function* can also be a custom callable function. Additional arguments can be passed to
        **scipy** s curve fitting tool: `curve fitting function <https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.curve_fit.html>`_

        :param function: String (identifier) or callable function.
        :return: 0
        """
        self.logger.debug('Fitting')
        if function == 'power':
            self.logger.debug('Using power fit function')
            self.fit_func = power
        else:
            assert callable(function), 'Custom provided function must be callable'
            self.logger.debug('Using custom fitting function')
            self.fit_func = function
        if 'p0' in kwargs.keys():
            self.logger.debug('Using custom start guess')
            start_guess = kwargs['p0']
            kwargs.pop('p0')
        else:
            self.logger.debug('Using standard start guess')
            start_guess = self.fit_func.fit_start_guess

        self.fitted_params, cov_matrix = curve_fit(self.fit_func,
                                                   self.fit_data['dsi'],
                                                   self.fit_data['ret'],
                                                   start_guess,
                                                   sigma=self.fit_data['ret_unc'],
                                                   **kwargs)
        if self.fit_data['ret_unc'] is not None:
            self.fitted_params = correlated_values(self.fitted_params, cov_matrix)

        if self.df_retention.index.max() < 30:
            self.logger.debug('Using standard mac days since install')
            index = np.arange(1, 31)
        else:
            self.logger.debug('Using custom max days since install')
            index = np.arange(1, self.df_retention.index.max() + 1)

        df_retention = pd.DataFrame(index=index, columns=['Retention', 'RetentionFit'])

        df_retention.loc[self.df_retention.index, 'Retention'] = self.df_retention['Retention']

        df_retention['RetentionFit'] = self.fit_func(index, *self.fitted_params)
        df_retention.index.name = 'DaysSinceInstall'
        self.df_retention = df_retention

        return 0

    def plot(self):
        r"""
        Plots the retention. If a fit have been performed it that is plotted too.

        :return: 0
        """
        self.logger.debug('Plotting')
        plt.figure(figsize=(16, 9))

        ret = nominal_values(self.df_retention['Retention'])
        ret_unc = std_devs(self.df_retention['Retention'])
        if ret_unc.sum() > 0:
            plt.errorbar(self.df_retention.index, ret, ret_unc, fmt='o', markersize=10, capsize=10,
                         capthick=5)
        else:
            plt.plot(self.df_retention.index, ret, 'o')
        ax = plt.gca()
        if 'RetentionFit' in self.df_retention.columns:
            self.logger.debug('Plotting fit')
            ret = nominal_values(self.df_retention['RetentionFit'])
            ret_unc = std_devs(self.df_retention['RetentionFit'])
            if ret_unc.sum() > 0:
                plt.errorbar(self.df_retention.index, ret, ret_unc, capsize=10, capthick=5)
            else:
                plt.plot(self.df_retention.index, ret)

        ax.set_xlim([-1, self.df_retention.index.max() + 1])
        ax.yaxis.set_major_formatter(ticker.PercentFormatter(xmax=1))

        if len(self.fitted_params) > 0:
            self.logger.debug('Calculating sum of retention')
            try:
                title = f'Sum of Retention day 180 = {self.retention_sum(180):.1f} days'
            except Exception as error:
                self.logger.error(f'Not possible to calculate integration, gave message: {error}')
                title = 'Retention'
        else:
            title = 'Retention'

        plt.title(title)
        plt.tight_layout()
        plt.show()
        return 0

    def retention_sum(self, dsi_end=180) -> float:
        r"""
        Calculates the sum of retention (mean average days the game have been opened at least once).
        It uses the parameters from a fit to calculate it and is only possible if the fit function
        is of the :class:`BaseFitFunction` class.

        :param dsi_end: The last day in the integration.
        :return: Sum of retention.
        """
        self.logger.debug('Calculating sum of retention.')
        return self.fit_func.integrate_func(dsi_end, self.fitted_params)

    def save(self, filename: str):
        r"""
        Saves an instance to the retention class as a pickled object.

        :param filename: Filename to be used.
        :return: 0
        """
        self.logger.debug('Saving instance.')
        # WTF some bug that only exist on linux (and windows?)
        # seems to make it impossible to pickle with the logger. WTF!?!
        self.logger = None
        with open(filename, 'wb') as file_handle:
            pickle.dump(self, file_handle, pickle.HIGHEST_PROTOCOL)
        return 0
