---
title: 'binomial_CIs: A Python Package for Optimal Binomial Confidence Intervals'
tags:
  - Python
  - statistics
  - confidence intervals
  - binomial
authors:
  - name: Joseph A. Vincent
    orcid: 0000-0002-2270-7395
    affiliation: 1
affiliations:
 - name: Department of Aeronautics and Astronautics, Stanford University
   index: 1
date: 10 June 2020
bibliography: paper.bib
---



# Summary

\href{[https://github.com/sisl/POMDPStressTesting.jl](https://github.com/TRI-ML/binomial_CIs)}{binomial_CIs} is a Python package for computing confidence intervals for the probability of success parameter, $p$, of a binomial distribution.



# Statement of Need

Constructing confidence intervals for an unknown probability success given samples of successes and failures is one of the most fundamental problems in statistical inference.
Research into this question dates back to the 1920s.
One of the key culminations of this research effort were procedures given by [REF Eudey, Lehmann Book] to construct uniformly most accurate (UMA) and uniformly most accurate unbiased (UMAU) confidence intervals.
These intervals have desirable optimality properties, and provide much better inference at small sample sizes than other methods.
The need for binomial_CIs arose out of these methods not having an open-source implementation.



# Research Usage

binomial_CIs has been used to compute confidence intervals for the probability of task success robot manipulators in simulation and the real world [REF].



# Acknowledgements

Financial support was provided by Toyota Research Institute.



# References