"""Main module."""

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd
import pickle
import sys

from datetime import date, datetime
from loguru import logger
from matplotlib import cm
from pyfreya.cohort import Cohort
from pyfreya.retention import Retention
from pyfreya.revenue import BaseRevenue
from typing import List, Union
from uncertainties.core import Variable
from uncertainties.unumpy import nominal_values, std_devs

try:
    logger.remove()
except ValueError:
    pass
finally:
    logger.add(sys.stderr, level='INFO')
logger.disable(__name__)

allowed_multi_cohort_plots = ['line', 'bar']


@logger.catch
def create_retention(days_since_install: List[int], retention_values: List[Union[float, Variable]]):
    r"""
    Creates a retention profile that can be used in cohorts.

    :param days_since_install: Days since install that accompanies the retention values.
    :param retention_values: Retention values can either be formatted in values below like
    >>> [0.5, 0.05, 0.01]

    or

    >>> [50, 5, 1]

    for values 50%, 5% and 1%.
    :return:
    """
    retention = Retention(days_since_install, retention_values)
    return retention


@logger.catch
def create_cohort(new_users,
                  days_since_install: List[int] = None,
                  retention_values: List[Union[float, Variable]] = None,
                  retention_function='power',
                  retention_profile: Retention = None,
                  start_date: Union[datetime, date, int] = 1,
                  revenue_profile: BaseRevenue = None,
                  name=''):
    r"""
    Creates a cohort class. "new_users" parameter must be provided. Retention information must
    also be provided, by either: add retention values and days since install values **or**
    supply a pre-made retention profile - see :class:`Retention`.
    A revenue profile can also be attached to a cohort - see :ref:`revenue_example`.

    The main variables of the class to keep track of is:

    * **df_user_dist:** Contains information about the user by days since install (index of the
      pandas dataframe) and date (column of the pandas dataframe).

    * **df_dau:** Contains information about daily active user and revenue. The index is date and
      the columns are *dau*, *revenue* and *revenueUnc*. Assuming each measure have been calculated.

    :param new_users: The amount of starting users.
    :param days_since_install: The days since install values to go along with *retention_values*.
    :param retention_values: The retention values to go along with *days_since_install*.
    :param retention_function: Function to fit the retention to.
    :param retention_profile: A premade retention profile using the *Retention* class.
    :param start_date: The start date of the first cohort.
    :param revenue_profile: A revenue profile object who had inherited its behaviour after
                            *BaseRevenue*.
    :param name: Name of cohort - is mostly used as identifier when working with multiple cohorts.
    :return:
    """
    cohort = Cohort(new_users, days_since_install, retention_values, retention_function,
                    retention_profile, start_date, revenue_profile, name)
    return cohort


@logger.catch
def multi_cohort_dau_plot(cohorts: List[Cohort], kind='line'):
    r"""
    Plot DAU by date for each cohort. With **kind='line'** a line plot is used, where all values
    are plotted from 0. With **kind='bar'** a stacked bar plot is used, meaning each value on each
    date is placed on top of each other.

    :param cohorts: List of cohotrs.
    :param kind: Type of plot, choose between **line** (default) and **bar**.
    :return:
    """
    if len(cohorts) < 2:
        raise ValueError('multi cohort plot requires at least 2 cohorts')

    assert kind in allowed_multi_cohort_plots, f'kind must be one of the following values: ' \
                                               f'{allowed_multi_cohort_plots}'

    if kind == 'line':
        c0 = cohorts[0]
        dau = nominal_values(c0.df_dau['dau'])
        dau_unc = std_devs(c0.df_dau['dau'])
        index = c0.df_dau.index.values
        index_type = type(index[0])

        plt.figure(figsize=(16, 9))
        if dau_unc.sum() > 0:
            plt.errorbar(index, dau, dau_unc, capsize=10, capthick=5, label=c0.name)
        else:
            plt.plot(index, dau, lw=3, label=c0.name)

        for c in cohorts[1:]:
            dau = nominal_values(c.df_dau['dau'])
            dau_unc = std_devs(c.df_dau['dau'])
            index = c.df_dau.index.values
            assert isinstance(index[0],
                              index_type), f'All indices must be of same type. Cohort {c0.name} ' \
                                           f'had type {index_type} whereas cohort {c.name} had ' \
                                           f'type {type(index[0])}.'
            if dau_unc.sum() > 0:
                plt.errorbar(index, dau, dau_unc, capsize=10, capthick=5, label=c.name)
            else:
                plt.plot(index, dau, lw=3, label=c.name)

        plt.legend()
        # only rotate datetime labels
        if not isinstance(index[0], (float, int)):
            plt.xticks(rotation=90)

    elif kind == 'bar':
        cohort_formatted = [None] * len(cohorts)
        for c_counter, c in enumerate(cohorts):
            df_temp = c.df_dau.copy()
            df_temp['dau'] = nominal_values(df_temp['dau'])
            df_temp = df_temp[['dau']].rename(columns={'dau': c.name})
            cohort_formatted[c_counter] = df_temp
        df_multi = pd.concat(cohort_formatted, axis=1, sort=False)
        df_multi.plot.bar(figsize=(16, 9), stacked=True)

    plt.xlabel('Date')
    plt.ylabel('DAU')
    plt.title('Daily Active User by Date')
    plt.tight_layout()
    plt.show()


@logger.catch
def multi_cohort_rev_plot(cohorts: List[Cohort], kind='line', cumulative=True):
    """
    Plot revenue from multiple cohorts. With **kind='line'** a line plot is used, where all revenue
    is plotted from 0. With **kind='bar'** a stacked bar plot is used, meaning each revenue on each
    date is placed on top of each other.

    :param cohorts: List of cohorts.
    :param kind: Type of plot, choose between **line** (default) and **bar**.
    :param cumulative: Denotes if the cumulative lines should be included.
    :return:
    """
    if len(cohorts) < 2:
        raise ValueError('multi cohort plot requires at least 2 cohorts')

    assert kind in allowed_multi_cohort_plots, f'kind must be one of the following values: ' \
                                               f'{allowed_multi_cohort_plots}'

    c0 = cohorts[0]
    index = c0.df_dau.index.values
    index_type = type(index[0])

    df = c0.df_dau['revenue'].copy()
    df = df.to_frame().rename(columns={'revenue': c0.name})
    for c in cohorts[1:]:
        index = c.df_dau.index.values
        assert isinstance(index[0], index_type), f'All indices must be of same type. Cohort ' \
                                                 f'{c0.name} had type {index_type} whereas cohort' \
                                                 f' {c.name} had type {type(index[0])}.'
        if c.df_dau.index.max() > df.index.max():
            print(f'WARNING: Days since install for cohort {c.name} goes above that of the first'
                  f' cohort given ({c0.name}) which only goes to {df.index.max()}.',
                  file=sys.stderr)
        df[c.name] = c.df_dau['revenue']

    if kind == 'line':
        plt.figure(figsize=(16, 9))
        for col in df.columns.values:
            rev = nominal_values(df[col])
            rev_unc = std_devs(df[col])
            index = df[col].index.values
            if rev_unc.sum() > 0:
                plt.errorbar(index, rev, rev_unc, capsize=10, capthick=5, label=col)
            else:
                plt.plot(df[col], label=col, lw=3)

        df['Cumulative'] = df.sum(axis=1).cumsum()
        # only rotate datetime labels
        if not isinstance(index[0], (float, int)):
            plt.xticks(rotation=90)

        ax1 = plt.gca()
        ax1.set_ylabel('Revenue')

        if cumulative:
            ax2 = ax1.twinx()
            ax2.plot(df['Cumulative'].index.values, nominal_values(df['Cumulative']), 'k--',
                     label='Cumulative', lw=3)
            ax2.grid(False)
            ax2.set_ylabel('Cumulative Revenue')
            ax2.legend(loc=8)
            ax1.legend(loc=2)

    elif kind == 'bar':
        fig, ax1 = plt.subplots(figsize=(16, 9))
        bottom = None
        for col in df.columns.values:
            ax1.bar(df[col].index.values, df[col], label=col, lw=3, bottom=bottom)
            if bottom is None:
                bottom = df[col]
            else:
                bottom += df[col]

        plt.xticks(rotation=90)
        ax1.set_ylabel('Revenue')
        ax1.set_xlabel('Date')
        plt.legend(loc=2)
        df['Cumulative'] = df.sum(axis=1).cumsum()
        if cumulative:
            ax2 = ax1.twinx()
            ax2.plot(df['Cumulative'], 'k--', label='Cumulative', lw=3)
            ax2.grid(False)
            ax2.set_ylabel('Cumulative Revenue')
            ax2.legend(loc=8)

    plt.xlabel('Date')
    plt.title('Revenue by Date')
    plt.tight_layout()
    plt.show()


@logger.catch
def multi_cohort_ret_plot(cohorts: List[Cohort]):
    r"""
    Plot retention for multiple cohorts.

    :param cohorts: List of cohorts.
    :return:
    """
    if len(cohorts) < 2:
        raise ValueError('multi cohort plot requires at least 2 cohorts')

    c0 = cohorts[0]
    index = c0.df_dau.index.values
    index_type = type(index[0])

    for c in cohorts[1:]:
        index = c.df_dau.index.values
        assert isinstance(index[0], index_type), f'All indices must be of same type. Cohort ' \
                                                 f'{c0.name} had type {index_type} whereas cohort' \
                                                 f' {c.name} had type {type(index[0])}.'

    plt.figure(figsize=(16, 9))
    ax = plt.gca()
    max_dsi = -1
    for c_counter, c in enumerate(cohorts):
        color = cm.Set1(c_counter)
        plt.plot(c.retention_profile.df_retention.index,
                 c.retention_profile.df_retention['Retention'],
                 'o', markersize=20, label=c.name, color=color[:3])
        if 'RetentionFit' in c.retention_profile.df_retention.columns:
            c.retention_profile.df_retention.plot(y='RetentionFit', ax=ax, lw=4, label=c.name,
                                                  color=color[:3])
        max_dsi = max([c.retention_profile.df_retention.index.max(), max_dsi])
    ax.set_xlim([-1, max_dsi + 1])

    plt.xlabel('DaysSinceInstall')
    plt.ylabel('Retention')
    plt.title('Retention')
    ax.yaxis.set_major_formatter(ticker.PercentFormatter(xmax=1))
    plt.tight_layout()
    plt.show()


@logger.catch
def save_class(filename: str, class_instance):
    r"""

    :param filename:
    :param objet:
    :return:
    """
    with open(filename, 'wb') as file_handle:
        pickle.dump(class_instance, file_handle)


@logger.catch
def load_class(filename: str):
    r"""

    :param filename:
    :return:
    """
    with open(filename, 'rb') as file_handle:
        return pickle.load(file_handle)
