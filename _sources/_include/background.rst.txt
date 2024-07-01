Background
##########


What is a binomial confidence interval?
***************************************
The binomial distribution represents the likelihood of observing :math:`k` successes in :math:`n` trials where the probability of success for each trial is :math:`p`. 
One often does not know the true value of :math:`p` and wishes to estimate this value. 
After observing :math:`k` successes in :math:`n` trials with unknown probability of success :math:`p`, a confidence interval (CI) is constructed in such a way that it contains the true value of :math:`p` with some high probability.

In constructing confidence intervals one has to tradeoff between three quantities:

#. Confidence: The probability that the CI contains the true parameter. Often written as :math:`1-\alpha` where :math:`\alpha` is small.
#. Volume: The length of the CI. If the CI is constructed as a lower bound on :math:`p` (i.e. :math:`[\underline{p}, 1]`), then we care about the length of the CI which is below :math:`p`. This is known as the `shortage`. 
#. Number of samples: In general, with more samples one can construct CIs with higher confidence and smaller volume.



Why does this package exist?
****************************
Existing implementations of binomial CIs do not optimally control the tradeoffs between confidence, volume, and number of samples. 
In practice, this means that if a user specifies :math:`k` and :math:`n`, existing implementations return CIs with higher/lower confidence than desired and/or with higher volume than necessary.
CIs which optimally trade-off between these quantities have the property of being `uniformly most accurate` (UMA) or   `uniformly most accurate unbiased` (UMAU).
Methods for constructing UMA and UMAU binomial confidence intervals has existed since the mid-20th century, but until now have not been implemented in an open-source software package.
We implement UMA and UMAU binomial confidence intervals using methods from   

* `On the treatment of discontinuous random variables <https://search.library.berkeley.edu/permalink/01UCS_BER/s4lks2/cdi_proquest_journals_301822201>`_ by Eudey,
* `Testing Statistical Hypotheses <https://link.springer.com/book/10.1007/978-3-030-70578-7>`_ by Lehmann and Romano,
* `Table of Neyman-shortest unbiased confidence intervals for the binomial parameter <https://www.jstor.org/stable/2333308>`_ by Blyth and Hutchinson.


Existing software implementations for binomial CIs include:

* `statsmodels.stats.proportion.proportion_confint <https://www.statsmodels.org/devel/generated/statsmodels.stats.proportion.proportion_confint.html>`_ (Python)
* `scipy.stats._result_classes.BinomTestResult.proportion_ci <https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats._result_classes.BinomTestResult.proportion_ci.html>`_ (Python)
* `astropy.stats.binom_conf_interval <https://docs.astropy.org/en/stable/api/astropy.stats.binom_conf_interval.html>`_ (Python)
* `scipy.stats.binom <https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.binom.html>`_ (Python)
* `EBCIC <https://github.com/KazKobara/ebcic>`_ (Python)
* `binom.test <https://stat.ethz.ch/R-manual/R-devel/library/stats/html/binom.test.html>`_ (R)
* `binom.confint <https://cran.r-project.org/web/packages/binom/binom.pdf>`_ (R)
* `BinomCI <https://search.r-project.org/CRAN/refmans/DescTools/html/BinomCI.html>`_ (R)
* `HypothesisTests.jl <https://juliastats.org/HypothesisTests.jl/stable/methods/#Confidence-interval>`_ (Julia)
* `RobustStats.jl <https://github.com/mrxiaohe/RobustStats.jl/tree/67cec0ea9ac9c4c8a3fe8f2a4e93cadbe68b1d77>`_ (Julia)
* `ClinicalTrialUtilities.jl <https://docs.juliahub.com/ClinicalTrialUtilities/lEJUs/0.3.1/>`_ (Julia)
* `binofit <https://www.mathworks.com/help/stats/binofit.html>`_ (Matlab)

The methods these packages implement include:

* Wald/Normal [1]
* Agresti-Coull [1]
* Clopper-Pearson (*) [1]
* Wilson [1]
* Modified Wilson [1]
* Wilson with continuity correction (*) [1]
* Jeffreys [1]
* Bayesian uniform prior
* Inverting the binomial test (*) [3]
* Arcsine [1]
* Logit [1]
* Probit [8]
* Complementary log [8]
* Likelihood (Profile) [1]
* Witting (*) [4]
* Pratt [5]
* Mid-p [7]
* Blaker (*) [6]
* Second-order corrected [2]

The reference of each method points to a survey paper (if possible) rather than the original derivation of the method.

Only the methods marked with (*) are guaranteed to provide at least as much confidence as desired. 
However, none of these methods provide exactly the confidence level desired (Witting might, but the listed reference is not freely available online and is only published in German).

It is also worth noting the `ump <http://CRAN.R-project.org/package=ump>`_ R package. 
This package implements UMP and UMPU hypothesis tests for the binomial distribution. 
Such tests could be leveraged to construct UMA and UMAU confidence intervals, but this doesn't appear to be implemented based on the documented functions. 
In addition, the authors of this package note that their implemetation has issues with numerical stability.

Existing software implementations for computing binomial CIs with exact confidence levels are then either non-existent or unsatisfactory. 
Unsurprisingly then, there is also no open-source implementation for computing the expected shortage (or expected excess or expected width) of binomial CIs, and no implementation for computing the worst-case values of these quantities. 
This package exists to fill this gap.









What exactly does this package do?
**********************************
This package constructs optimal confidence intervals for the probability of success parameter of a binomial distribution.

Lower Bounds
============
Given user specified miscoverage rate (:math:`\alpha`) and maximum expected shortage (:math:`\text{MES}`), return a lower bound on :math:`p` that satisfies the following requirements:

#. achieves exact desired coverage: :math:`\mathbb{P}[\underline{p} \le p] = 1-\alpha`,
#. :math:`[\underline{p}, 1]` is uniformly most accurate,
#. achieves exact desired maximum expected shortage: :math:`\max_p \ \mathbb{E}_p[\max (p - \underline{p}, 0)] = \text{MES}`,
#. uses the minimum number of samples :math:`n` to achieve requirements 1,2,3.


Upper Bounds
============
Given user specified miscoverage rate (:math:`\alpha`) and maximum expected excess (:math:`\text{MEE}`), return an upper bound on :math:`p` that satisfies the following requirements:

#. achieves exact desired coverage: :math:`\mathbb{P}[p \le \overline{p}] = 1-\alpha`,
#. :math:`[0, \overline{p}]` is uniformly most accurate,
#. achieves exact desired maximum expected excess: :math:`\max_p \ \mathbb{E}_p[\max (\overline{p} - p, 0)] = \text{MEE}`,
#. uses the minimum number of samples :math:`n` to achieve requirements 1,2,3.




Simultaneous Lower and Upper Bounds
===================================
Given the user specified miscoverage rate (:math:`\alpha`) and maximum expected width (:math:`\text{MEW}`), return simultaneous lower and upper bounds on :math:`p` that satisfy the following requirements:

#. achieves exact desired coverage: :math:`\mathbb{P}[\underline{p} \le p \le \overline{p}] = 1-\alpha`,
#. :math:`[\underline{p}, \overline{p}]` is uniformly most accurate unbiased,
#. achieves exact desired maximum expected width: :math:`\max_p \ \mathbb{E}_p[\overline{p} - \underline{p}] = \text{MEW}`,
#. uses the minimum number of samples :math:`n` to achieve requirements 1,2,3.





Relevant Literature
===================
For more information on the mathematics behind these confidence intervals see our affiliated paper `How Generalizable Is My Behavior Cloning Policy? A Statistical Approach to Trustworthy Performance Evaluation <https://arxiv.org/abs/2405.05439>`_

Below are some of the resources that we found most useful for understanding binomial confidence intervals.

* `Testing Statistical Hypotheses <https://link.springer.com/book/10.1007/978-3-030-70578-7>`_ by Lehmann and Romano
* `On the treatment of discontinuous random variables <https://search.library.berkeley.edu/permalink/01UCS_BER/s4lks2/cdi_proquest_journals_301822201>`_ by Eudey
* `Table of Neyman-shortest unbiased confidence intervals for the binomial parameter <https://www.jstor.org/stable/2333308>`_ by Blyth and Hutchinson
* `Length of Confidence Intervals <https://www.tandfonline.com/doi/abs/10.1080/01621459.1961.10480644>`_ by Pratt
* `More on length of confidence intervals <https://www.tandfonline.com/doi/abs/10.1080/01621459.1962.10500547>`_ by Madansky
* `Binomial confidence intervals <https://www.tandfonline.com/doi/abs/10.1080/01621459.1983.10477938>`_ by Blyth and Still
* `Smallest confidence intervals for one binomial proportion <https://www.sciencedirect.com/science/article/pii/S0378375805002430>`_ by Wang
* `Fuzzy and randomized confidence intervals and p-values <https://www.jstor.org/stable/20061193>`_ by Geyer and Meeden
* `Nonoptimality of Randomized Confidence Sets <https://www.stat.purdue.edu/docs/research/tech-reports/1988/tr88-09.pdf>`_ by Casella and Robert









References
==========

#. `Interval Estimation for a Binomial Proportion <https://www.jstor.org/stable/2676784>`_ by Brown, Cai, and DasGupta
#. `One-sided confidence intervals in discrete distributions <https://www.sciencedirect.com/science/article/pii/S0378375804000679>`_ by Cai
#. `Some Remarks on Confidence or Fiducial Limits <https://www.jstor.org/stable/2333026>`_ by Sterne
#. `Mathematische Statistik I. <https://link.springer.com/book/10.1007/978-3-322-90150-7>`_ by Witting
#. `Binomial Confidence Intervals <https://www.jstor.org/stable/2287116>`_ by Blyth and Still
#. `Confidence Curves and Improved Exact Confidence Intervals for Discrete Distributions <https://www.jstor.org/stable/3315916>`_ by Blaker
#. `Comment: Randomized Confidence Intervals and the Mid-P Approach <https://www.semanticscholar.org/paper/Comment%3A-Randomized-Confidence-Intervals-and-the-Agresti-Gottard/596fd2a98486f65599b56ac81aef32e5c1a0d586>`_ by Agresti and Gottard
#. `binom <https://cran.r-project.org/web/packages/binom/binom.pdf>`_ by Sundar Dorai-Raj
#. `Fuzzy and randomized confidence intervals and p-values <https://www.jstor.org/stable/20061193>`_ by Geyer and Meeden.