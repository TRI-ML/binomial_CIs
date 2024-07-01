Potential Pitfalls
==================


Randomized Confidence Intervals
*******************************
The methods used in this package to construct CIs are based on the inversion of randomized hypothesis tests. 
This means that calling ``binom_ci()`` with the same ``k,n,alpha`` will result in different CIs. 
For the guarantees of the CI to hold it is critical that the user only construct one CI for the experiment they have. 
Constructing multiple CIs and choosing the best one invalidates the guarantees of the CI. 

For the 1-sided bounds there is the option to get less efficient but non-randomized CIs:

.. code-block::

   lb = binom_ci(k, n, alpha, 'lb', randomized=False)
   ub = binom_ci(k, n, alpha, 'ub', randomized=False)

These non-randomized 1-sided bounds are equivalent to 1-sided Clopper-Pearson bounds. 
We currently don't have an implementation of non-randomized 2-sided bounds.
Randomization allows the CIs to be UMA. 
Although randomization has been a point of debate amongst statisticians, we take the view (first given by Mark Eudey) that insofar as construction of confidence intervals can be treated as a (von Neumann) game, randomization merely allows the statistician to employ a mixed strategy.



Multiple Tests
**************
As with all CIs one must take special care when interpreting the results of multiple CIs constructed from independent tests. 
If one constructs :math:`m` CIs where the probability of each CI containing the true parameter is 1-alpha, then the probability that **all** :math:`m` CIs contain their respective parameters is less than 1-\alpha.
For more explanation, see the `Wikipedia article <https://en.wikipedia.org/wiki/Multiple_comparisons_problem>`_ on the multiple comparisons problem.
