.. binomial_cis documentation master file, created by
   sphinx-quickstart on Thu Jun 27 09:55:48 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

binomial_cis
========================================

This is a Python package for computing confidence intervals for the probability of success parameter, :math:`p`, of a binomial distribution. 
The binomial distribution represents the likelihood of observing :math:`k` successes in :math:`n` trials where the probability of success for each trial is :math:`p`. 
For example, :math:`p` may be the probability of a coin flip landing on heads, and :math:`k` the number of heads we observe after :math:`n` flips. 
One often does not know the value of :math:`p` and wishes to estimate it. A confidence interval is a set, constructed based on :math:`k, n`, that covers the unknown parameter :math:`p` with some user-specified probability.
The binomial_cis package computes confidence intervals that lower and/or upper bound :math:`p` with a user-specified probability.



Source Code
===========
The source code for this package is available at `https://github.com/TRI-ML/binomial_cis/ <https://github.com/TRI-ML/binomial_cis/>`_.


Installation
============
Install the package with pip:

.. code-block::

    pip install binomial_cis



Example Usage
=============

Lower Bounds
************
Find a lower bound on :math:`p`:

.. code-block::

   from binomial_cis import binom_ci

   k = 5 # number of successes
   n = 10 # number of trials
   alpha = 0.05 # miscoverage probability

   lb = binom_ci(k, n, alpha, 'lb')


Find maximum expected shortage given miscoverage rate and number of samples:

.. code-block::

   from binomial_cis import max_expected_shortage

   mes_ub, mes_lb, p_lb, num_iters = max_expected_shortage(alpha, n, tol=1e-3)




Upper Bounds
************
Find an upper bound on :math:`p`:

.. code-block::

   from binomial_cis import binom_ci

   k = 5 # number of successes
   n = 10 # number of trials
   alpha = 0.05 # miscoverage probability

   ub = binom_ci(k, n, alpha, 'ub')


Find maximum expected excess given miscoverage rate and number of samples:

.. code-block::

   from binomial_cis import max_expected_excess
   
   mee_ub, mee_lb, p_lb, num_iters = max_expected_excess(alpha, n, tol=1e-3)





2-Sided Bounds
**************
Find simultaneous lower and upper bounds on :math:`p`:

.. code-block::

   from binomial_cis import binom_ci

   k = 5 # number of successes
   n = 10 # number of trials
   alpha = 0.05 # miscoverage probability

   lb, ub = binom_ci(k, n, alpha, 'lb,ub')


Find maximum expected width given miscoverage rate and number of samples:

.. code-block::

   from binomial_cis import max_expected_width

   mew_ub, mew_lb, p_lb, num_iters = max_expected_width(alpha, n, tol=1e-3)




More Resources
==============
.. toctree::
   :maxdepth: 1

   _include/background
   _include/notebooks
   _include/tests
   _include/api_reference
   _include/potential_pitfalls
   _include/community_guidelines
   
   
   

Index
==================

* :ref:`genindex`
