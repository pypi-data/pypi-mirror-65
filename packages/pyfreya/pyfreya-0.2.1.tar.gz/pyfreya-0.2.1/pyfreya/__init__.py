"""Top-level package for PyFreya."""

__author__ = """Morten Andreasen"""
__email__ = 'yggdrasil.the.binder@gmail.com'
__version__ = '0.2.1'

import sys


try:
    from uncertainties import ufloat
    from uncertainties.unumpy import nominal_values, std_devs
except ModuleNotFoundError:
    print('The uncertainties package was not found. Visit https://pypi.org/project/uncertainties/ '
          'to install. Functionality of PyFreya without this package have not been tested.',
          file=sys.stderr)
from pyfreya.pyfreya import create_cohort, create_retention, multi_cohort_dau_plot, \
    multi_cohort_ret_plot, multi_cohort_rev_plot, save_class, load_class
from pyfreya.cohort.cohort import Cohort
from pyfreya.retention.retention import Retention
from pyfreya.retention.fit_functions import BaseFitFunction
from pyfreya.revenue.revenue import BaseRevenue
