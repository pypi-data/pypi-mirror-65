"""

.. include:: tutorials/cohort/Cohort_Example.rst

Cohort Class
============
"""

from __future__ import annotations

import pickle
import sys
import uuid
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from datetime import datetime, date, timedelta
from io import StringIO
from loguru import logger
from pandas.plotting import register_matplotlib_converters
from pyfreya.retention import Retention
from pyfreya.revenue import BaseRevenue
from typing import List, Union, Callable
from uncertainties.unumpy import nominal_values, std_devs
from uncertainties.core import Variable

register_matplotlib_converters()


class Cohort:
    r"""Cohort class
    *new_users* parameter must be provided. To add retention, either add retention and days since
    install values or supply a pre-made retention profile - see :class:`Retention`.
    """

    def __init__(self,
                 new_users: int,
                 days_since_install: List[int] = None,
                 retention_values: List[Union[float, Variable]] = None,
                 retention_function='power',
                 retention_profile: Retention = None,
                 start_date: Union[datetime, date, int] = 1,
                 revenue_profile: BaseRevenue() = None,
                 name=''):
        r"""
        Inits the cohort class. "new_users" parameter must be provided. Retention information must
        also be provided, by either: add retention values and days since install values **or**
        supply a pre-made retention profile - see :class:`Retention`.
        A revenue profile can also be attached to a cohort -
        see :doc:`Revenue <pyfreya.revenue.rst>`.

        The main variables of the class to keep track of is:

        * **df_user_dist:** Contains information about the user by days since install (index of the
        pandas dataframe) and date (column of the pandas dataframe).
        * **df_dau:** Contains information about daily active user and revenue. The index is date
        and the columns are *dau*, *revenue* and *revenueUnc*. Assuming each measure have been
        calculated.

        :param new_users: The amount of starting users.
        :param days_since_install: The days since install values to go along with
        *retention_values*.
        :param retention_values: The retention values to go along with *days_since_install*.
        :param retention_function: Function to fit the retention to.
        :param retention_profile: A premade retention profile using the *Retention* class.
        :param start_date: The start date of the first cohort.
        :param revenue_profile: A revenue profile object who had inherited its behaviour after
        *BaseRevenue*.
        :param name: Name of cohort - is mostly used as identifier when working with multiple
        cohorts.
        """
        self.logger = logger
        try:
            self.logger.remove()
        except ValueError:
            pass
        finally:
            self.logger.add(sys.stderr, level='INFO')
        self.logger.disable(__name__)

        if days_since_install is None and retention_profile is None:
            self.logger.debug('No retention information provided.')
            raise RuntimeError('Missing retention information, please add "days_since_install" '
                               'and "retention_values" or a retention profile in '
                               '"retention_profile"')
        if days_since_install is not None:
            self.logger.debug('Using retention and days since install values')
            retention_profile = Retention(days_since_install, retention_values)

        self.retention_profile = retention_profile
        self.new_users = new_users
        self.start_date = start_date
        self.revenue_profile = revenue_profile

        self._fit_retention(function=retention_function)
        self.replicate_cohort(1, 30)

        if not name:
            self.logger.debug('Creating random name')
            self.name = uuid.uuid4().__str__()[:8]
        else:
            self.logger.debug('Adding supplied name.')
            self.name = name

    def __str__(self):
        r"""
        Make the print look like pandas dataframe of user distribution.
        :return: Pandas dataframe.
        """
        with pd.option_context('display.max_rows', 40, 'display.max_columns', None,
                               'display.width', 200):
            return self.df_user_dist.__str__()

    def __repr__(self):
        r"""
        Make the print with repr look like a pandas dataframe of user distribution.
        :return: Pandas dataframe.
        """
        with pd.option_context('display.max_rows', 40, 'display.max_columns', None,
                               'display.width', 200):
            return self.df_user_dist.__str__()

    def _fit_retention(self, function: Union[str, Callable] = 'power', **kwargs):
        r"""
        Fit retention with the fit function defined the retention profile.

        :param function: Function to fit.
        :param kwargs: Additional  arguments supported by `Scipy Curve_fit
<https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.curve_fit.html>`_.
        :return:
        """
        self.logger.debug('Fitting retention.')
        self.retention_profile.fit(function, **kwargs)

    def _age_cohort(self, age: int, set_user_dist=True) -> (np.ndarray, np.ndarray):
        r"""
        Age a cohort from days since install 0 to *age*. To not overwrite the **df_user_dist** set
        *set_user_dist*=False.

        :param age: The amount of days since install a cohort should be aged by.
        :param set_user_dist: Boolean to decide if **df_user_dist** should be overwritten.
        :return: The aged cohort.
        """
        self.logger.debug('Aging cohort.')

        days_since_install = np.arange(1, age + 1)
        retention = self.retention_profile(days_since_install)
        if isinstance(self.start_date, (date, datetime)):
            self.logger.debug('Using datetime for dates.')
            start_date = self.start_date
        else:
            self.logger.debug('Using integers for dates.')
            start_date = 1

        aged_cohort = self.new_users * retention
        if set_user_dist:
            self.logger.debug('Setting dataframes.')
            self.df_user_dist = pd.DataFrame(data=aged_cohort,
                                             index=days_since_install,
                                             columns=[start_date],
                                             dtype=pd.Int64Dtype)
            self.df_user_dist.index.name = 'DaysSinceInstall'
        return aged_cohort, days_since_install + 1

    def replicate_cohort(self, n_days_since_install: int, post_influx_duration=0):
        r"""
        Replicate the cohort over multiple days. The number of dates are concurrent and given in
        the first parameter. If it is of any interest to see the cohorts after the influx of them
        have stopped *post_influx_duration* can be set to some amount of days.

        :param n_days_since_install: Number of days a new (equivalent) cohort starts.
        :param post_influx_duration: The number of days to wait after the last cohort have been
        added.
        :return:
        """
        self.logger.debug('Replicating cohort.')
        if isinstance(self.start_date, (date, datetime)):
            self.logger.debug('Using datetime for dates')
            dates = [self.start_date + timedelta(days=n) for n in range(n_days_since_install)]
        else:
            self.logger.debug('Using integers for dates.')
            dates = np.arange(self.start_date, n_days_since_install + self.start_date)

        aged_cohort, _ = self._age_cohort(n_days_since_install + post_influx_duration)

        data = np.full(
            (n_days_since_install + post_influx_duration + 1, n_days_since_install),
            np.nan,
            dtype=object)

        data[0, :] = self.new_users
        for current_date in range(1, n_days_since_install + 1):
            dsi_end = current_date + 1 + post_influx_duration
            data[1:dsi_end, current_date - 1] = aged_cohort[:current_date + post_influx_duration]

        user_dist_index = np.arange(n_days_since_install + post_influx_duration + 1)
        self.df_user_dist = pd.DataFrame(data=data,
                                         index=user_dist_index,
                                         columns=dates)
        self.df_user_dist.index.name = 'DaysSinceInstall'

        # OKAY THIS IS FUCKING STUPID
        # For some reason, when using the uncertainties package, some calculations are performed
        # wrongly (given a bunch of zeros) unless a print statement of the df_user_dist is used.
        # I don't know why, I don't know how come, I have cried many tears and lost a lot of hair
        # trying to debug it... Now I uses the absolute dumbest, most embarrassingly and quite
        # frankly worst solution. It does seem to work though.

        print(self.df_user_dist, file=StringIO())

        self._calculate_dau()

    def _calculate_dau(self):
        r"""
        Calculates daily active users (DAU) by date.
        :return:
        """
        self.logger.debug('Calculating dau.')
        base_time = self.df_user_dist.columns[-1]
        non_influx_days = self.df_user_dist.shape[0] - self.df_user_dist.shape[1]
        if isinstance(self.start_date, (date, datetime)):
            self.logger.debug('Using datetime for dates')
            non_influx_dates = [(base_time + timedelta(days=i + 1)).date() for i in
                                range(non_influx_days)]
            dates = self.df_user_dist.columns.date
        else:
            self.logger.debug('Using integers for dates.')
            non_influx_dates = [base_time + 1 + i for i in range(non_influx_days)]
            dates = self.df_user_dist.columns.values

        dates = np.append(dates, non_influx_dates)

        diag_offsets = np.arange(self.df_user_dist.shape[1] - 1, -non_influx_days, -1)
        dau_values = np.zeros(diag_offsets.shape, dtype=object)
        dau_dates = np.zeros(diag_offsets.shape, dtype=object)

        for diag_counter, diag_index in enumerate(diag_offsets):
            dau = np.nansum(np.diag(self.df_user_dist, diag_index))
            current_date = dates[diag_counter]
            dau_values[diag_counter] = dau
            dau_dates[diag_counter] = current_date

        self.df_dau = pd.DataFrame(data=dau_values,
                                   index=dau_dates,
                                   columns=['dau'],
                                   )
        self.df_dau.index.name = 'Date'

    def plot_retention(self):
        r"""
        Plots the retention.

        :return:
        """
        self.logger.debug('Plotting retention.')
        self.retention_profile.plot()

    def plot_dau(self):
        r"""
        Plot daily active users.

        :return:
        """
        self.logger.debug('Plotting dau.')

        dau = nominal_values(self.df_dau['dau'])
        dau_unc = std_devs(self.df_dau['dau'])

        plt.figure(figsize=(16, 9))
        if dau_unc.sum() > 0:
            plt.errorbar(self.df_dau.index, dau, dau_unc, fmt='o-', markersize=10, capsize=10,
                         capthick=5)
        else:
            plt.plot(self.df_dau.index, dau, lw=4)
        # self.df_dau['dau'].plot(figsize=(16, 9), lw=4)
        plt.title('DAU by Date')
        plt.xticks(rotation=50)
        plt.xlabel('Date')
        plt.ylabel('DAU')
        plt.tight_layout()
        plt.show()

    def days_to_dau(self, goal: int, max_days=360):
        r"""
        Calculates the number of days until a given dau count have been reached. To not continue
        into infinity (and beyond) it is ensured that the maximum amount of days is *max_days*.

        :param goal: The amount of DAU that is the goal.
        :param max_days: The maximum number of days to look through.
        :return:
        """
        self.logger.debug('Calculating days until dau.')
        if max_days <= 1:
            self.logger.error('Max days since install is lower than 1.')
            raise ValueError('"max_days" must be larger than 1')
        current_day_count = 1
        while current_day_count <= max_days:
            dau, _ = self._age_cohort(current_day_count, False)
            if dau.sum() + self.new_users > goal:
                self.logger.debug(f'goal found on day {current_day_count + 1}')
                return current_day_count + 1
            current_day_count += 1
        self.logger.debug(
            f'Days until reaching goal surpassed "max_days" '
            f'needing {goal - dau.sum() + self.new_users} users. '
            f'Try another value than max_days={max_days}.')

    def apply_revenue(self, revenue_profile: BaseRevenue = None):
        r"""
        Given a revenue profile and a cohort apply the revenue profile to get revenue and revenue
        uncertainty.

        :param revenue_profile: The revenue profile to use, if none is provided it will assume that
        one was provided earlier.
        :return:
        """
        if revenue_profile is not None:
            self.revenue_profile = revenue_profile
        assert self.revenue_profile is not None, 'Must provide revenue profile'
        self.logger.debug('Apply revenue to cohorts')
        self.revenue_profile(self)

    def plot_revenue(self):
        r"""
        Plot the revenue with uncertainty (left y-axis) and cumulative revenue (right y-axis). The
        cumulative revenue could also have uncertainty, though it is not obvious how to calculate
        this. The best bet is probably `error propagation
         <https://en.wikipedia.org/wiki/Propagation_of_uncertainty>`_.

        :return:
        """
        self.logger.debug('Plotting revenue.')
        plt.figure(figsize=(16, 9))
        plt.suptitle('Revenue by Date')
        ax0 = plt.subplot(111)
        plt.xticks(rotation=50)
        ax1 = ax0.twinx()

        rev = nominal_values(self.df_dau['revenue'])
        rev_unc = std_devs(self.df_dau['revenue'])

        if rev_unc.sum() > 0:
            rev_line = ax0.errorbar(self.df_dau.index, rev,
                                    rev_unc, lw=4,
                                    fmt='o-', markersize=10, capsize=10,
                                    capthick=5)
        else:
            rev_line, = ax0.plot(self.df_dau.index, rev, '-', lw=4)

        cumu_rev_line = ax1.plot(self.df_dau.index, rev.cumsum(), '--', lw=4)
        lines = [rev_line, cumu_rev_line[0]]
        ax0.legend(lines, ['Revenue', 'Cumulative Revenue'], loc=2)
        ax1.grid(False)
        ax0.set_ylabel('Revenue')
        ax1.set_ylabel('Cumulative Revenue')
        plt.tight_layout()
        plt.show()

    def days_to_rev(self, goal: float, max_days=360):
        r"""
        Calculates the number of days until revenue of a single day hav reached *goal* or above.
        To not continue into infinity (and beyond) it is ensured that the maximum amount of days
        is *max_days*.

        :param goal: Daily revenue goal.
        :param max_days: The maximum number of days to look trough.
        :return:
        """
        self.logger.debug('Calculating days to daily revenue goal.')
        if max_days <= 1:
            self.logger.error('Max days since install is lower than 1.')
            raise ValueError('"max_days" must be larger than 1')
        if self.revenue_profile is None:
            self.logger.error('Revenue profile not detected.')
            raise TypeError('"revenue_profile" is not added')
        current_day_count = 1
        while current_day_count <= max_days:
            dau, _ = self._age_cohort(current_day_count, False)
            dau = np.append([self.new_users], dau)
            df_temp = pd.DataFrame(data=dau, index=np.arange(current_day_count + 1),
                                   columns=['dau'])
            revenue = self.revenue_profile._revenue(df_temp)
            if revenue.sum() > goal:
                self.logger.debug(f'goal found on day {current_day_count + 1}')
                return current_day_count + 1
            current_day_count += 1
        self.logger.error(
            f'Days until reaching goal surpassed "max_days" '
            f'needing {goal - revenue.sum():.1f} users. '
            f'Try another value than max_days={max_days}.')

    def days_to_total_rev(self, goal: float, max_days=360):
        r"""
        Calculates the number of days until the cumulative revenue have reached *goal* To not
        continue into infinity (and beyond) it is ensured that the maximum amount of days is
        *max_days*.

        :param goal: Cumulative revenue goal.
        :param max_days: The maximum number of days to look through.
        :return:
        """
        self.logger.debug('Calculating days until total revenue.')
        if max_days <= 1:
            self.logger.error('Max days since install is lower than 1.')
            raise ValueError('"max_days" must be larger than 1')
        if self.revenue_profile is None:
            self.logger.error('Revenue profile not detected.')
            raise TypeError('"revenue_profile" is not added')

        current_day_count = 1
        while current_day_count <= max_days:
            dau, _ = self._age_cohort(current_day_count, False)
            dau = np.append([self.new_users], dau)
            df_temp = pd.DataFrame(data=dau, index=np.arange(current_day_count + 1),
                                   columns=['dau'])
            revenue = self.revenue_profile._revenue(df_temp)
            if revenue.cumsum().cumsum().iloc[-1] > goal:
                self.logger.debug(f'goal found on day {current_day_count + 1}')
                return current_day_count + 1
            current_day_count += 1

        rest = goal - revenue.cumsum().cumsum().iloc[-1]
        self.logger.error(
            f'Days until reaching goal surpassed "max_days" '
            f'needing {rest:.1f} users. '
            f'Try another value than max_days={max_days}.')

    def save(self, filename: str):
        """
        Saves the cohort as a pickle file.

        :param filename: Filename for the cohort.
        :return:
        """
        self.logger.debug('saving cohort class')
        # WTF some bug that only exist on linux (and windows?)
        # seems to make it impossible to pickle with the logger. WTF!?!
        self.logger = None
        with open(filename, 'wb') as file_handle:
            pickle.dump(self, file_handle, pickle.HIGHEST_PROTOCOL)
        return 0
