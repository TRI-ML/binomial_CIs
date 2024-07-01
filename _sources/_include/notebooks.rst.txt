Notebooks
=========

The ``notebooks/`` directory in the Github repository has notebooks which explore different aspects of the code.
To run the notebooks, first clone the repository

.. code-block::

   gh repo clone TRI-ML/binomial_cis


Then, create a virtual environment and load the dependencies (these commands are for Unix/macOS)

.. code-block::

   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt



tradeoff_table.ipynb
********************
This notebook is used to compute maximum expected shortage (MES) vs miscoverage rate (alpha) and number of samples :math:`n`. 
Precomputed values have been stored in ``MES_table.csv`` which is visualized in a plot from the last cell of the notebook.


conf_set_validation.ipynb
*************************
This notebook is used to visualize the mixed-monotonic forms of expected shortage and expected width.
Also visualized is how these functions vary with :math:`p` and their maxima.