Tests
=====
A variety of tests have been implemented to check the validity of the provided functions.
Each test file is located in the ``tests/`` directory of the Github repository.
To run the tests, first clone the repository

.. code-block::

   gh repo clone TRI-ML/binomial_cis


Then, create a virtual environment and load the dependencies (these commands are for Unix/macOS)

.. code-block::

   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt


binom_ci_test.py
******************
This file contains functions to test the correctness of the lower, upper, 2-sided bounds, and the mixed monotonic solver.
The lower/upper bound tests ensure the bounds we compute are better than Clopper-Pearson bounds (without being too optimistic).
The 2-sided test ensures that our 2-sided bounds agree with those computed by Blyth and Hutchinson in their 1960 paper titled "Table of Neyman-Shortest Unbiased Confidence Intervals for the Binomial Parameter".
The mixed monotonic test ensures that the computed maximum of expected shortage/excess/width is greater than the sample-based maximum of these quantities.
We use a Github Action to automatically run the tests in this file via ``pytest``. 
To run the tests yourself simply navigate to the ``tests/`` directory and run

.. code-block::

    pytest -v




2_side_validation.ipynb
***********************
This notebook can be used to more easily inspect any differences between our 2-sided bounds and those from the Blyth paper.


binom_helper_validation.ipynb
*****************************
This notebook is used to validate the binomial helper functions from ``binomial_cis/binomial_helper.py```.
Accuracy and speed of our implementation is tested against the SciPy implementation.


conf_set_validation.ipynb
*************************
This notebook is used to validate the probabilistic guarantees of the confidence intervals using Monte Carlo simulation.

