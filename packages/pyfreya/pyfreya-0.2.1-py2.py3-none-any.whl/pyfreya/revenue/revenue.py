"""

.. include:: tutorials/revenue/Revenue_Example.rst

Revenue Classes
===============
"""

import pandas as pd
import pickle
import sys

from loguru import logger


class BaseRevenue:
    """
    Base class for the revenue profile. Revenue profiles are created by defining a new class which
    inherits functions from the BaseRevenue class::

        class MyClass(BaseRevenue)
            def __init__(self):
                super().__init__()
            def _revenue():
                return 0

    """
    def __init__(self):
        self.logger = logger
        try:
            self.logger.remove()
        except ValueError:
            pass
        finally:
            self.logger.add(sys.stderr, level='INFO')
        self.logger.disable(__name__)

    def __call__(self, cohort):
        r"""
        Returns the revenue by dates and the uncertainty of the revenue by date. If the given
        method does not have uncertainty implemented an array of same length as revenue with NaN
        values.

        :return: (*revenue*, *revenue uncertainty*), the revenue and revenue uncertainty.
        """
        if cohort.df_user_dist.shape[0] == 0 and cohort.new_users is not None:
            self.logger.debug('Replicating cohort and calculating dau')
            cohort.replicate_cohort(1, 30)
            cohort._calculate_dau()
        elif cohort.df_dau.shape[0] == 0:
            self.logger.debug('Calculating dau')
            cohort._calculate_dau()

        cohort.df_dau['revenue'] = self._revenue(cohort.df_dau)

    def _revenue(self, cohort):
        r"""
        Calculates revenue by date.

        :return: Revenue.
        """
        raise NotImplementedError

    def save(self, filename: str):
        r"""
        Saves the revenue model. As revenue models can have quite different properties *pickle* is
        used to save instances of the class.

        :return: 0
        """
        self.logger.debug('saving revenue class')
        # WTF some bug that only exist on linux (and windows?)
        # seems to make it impossible to pickle with the logger. WTF!?!
        self.logger = None
        with open(filename, 'wb') as file_handle:
            pickle.dump(self, file_handle, pickle.HIGHEST_PROTOCOL)
        return 0


class ARPDAU(BaseRevenue):
    r"""
    A basic revenue spending class. It applies an average revenue to each active users on a given
    date. There is no uncertainty applied to this class.
    """

    def __init__(self, arpdau=0.0):
        r"""
        Set the ARPDAU value.

        :param arpdau: Average revenue per daily active user.
        """
        super().__init__()
        self.arpdau = arpdau

    def _revenue(self, df_dau: pd.DataFrame) -> pd.Series:
        r"""
        Add ARAPDAU to dau dataframe.

        :param df_dau: dau dataframe.
        :return: Revenue by date.
        """
        self.logger.debug('Calculating revenue.')
        return df_dau['dau'] * self.arpdau
