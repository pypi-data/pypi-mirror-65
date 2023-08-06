=======
PyFreya
=======


.. image:: https://img.shields.io/pypi/v/pyfreya.svg
        :target: https://pypi.python.org/pypi/pyfreya

.. image:: https://img.shields.io/travis/morten/pyfreya.svg
        :target: https://travis-ci.org/morten/pyfreya

.. image:: https://readthedocs.org/projects/pyfreya/badge/?version=latest
        :target: https://pyfreya.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


Cohort Analysis Tool


* Free software: MIT license
* Documentation: https://pyfreya.readthedocs.io.


Features
--------

* Simulate retention
* Estimate daily active users
* Add revenue profiles
* Handles and propagates uncertainties

PyFreya Example
---------------

Simple Example of PyFreya::

   from pyfreya import create_cohort
   new_users = 100
   days_since_install = [1, 7, 30]
   retention_values= [50, 15, 5]
   facebook = create_cohort(new_users, days_since_install, retention_values)
   facebook.plot_dau()

.. image:: ../readme_dau.png

Lets add revenue::

   from pyfreya.revenue import ARPDAU
   facebook.apply_revenue(ARPDAU(1.79))
   facebook.plot_revenue()

.. image:: ../readme_revenue.png

Can even handle multiple cohorts - look at this DAU plot with uncertainties:

.. image:: ../readme_multi_cohort.png


Known Bugs/Problems
-------------------

* Cross-references in documentation does not produce hyperlinks.
* Seems that docs can only be build on linux... well use linux.

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
