import numpy as np
import sys; sys.path.insert(0, '..')
from binomial_cis import binom_ci, UMAU_lb, UMAU_ub
from scipy.stats import binomtest
from math import isclose
import pandas as pd

from binomial_cis.conf_intervals import llc_accept_prob, llc_accept_prob_2_sided
from binomial_cis.volume import expected_excess, max_expected_excess
from binomial_cis.volume import expected_shortage, max_expected_shortage
from binomial_cis.volume import expected_width, max_expected_width


# define range of test conditions
ns = np.array(range(1,50+1))
alphas = np.array([0.01, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.99])








#########################################
############ Helper Functions ###########
#########################################

def scipy_cp(k, n, alpha, side):
    """
    Inputs
    k: number of successes
    n: number of samples
    alpha: miscoverage rate, P(p_ <= p) >= 1-alpha
    side: 'lb' for lower bound, 'ub' for upper bound

    Returns
    p_cp: Clopper-Pearson lower confidence bound
    """
    assert side == 'lb' or side == 'ub'

    alternative = 'greater' if side=='lb' else 'less'
    stat_model = binomtest(k=k, n=n, alternative=alternative)
    ci = stat_model.proportion_ci(confidence_level=1-alpha, method='exact')
    p_cp = ci.low if side=='lb' else ci.high

    return p_cp


def fill_our_df(df, alpha):
    """
    Inputs
    df: dataframe of 2-sided bound values from Blyth paper
    alpha: miscoverage raate

    Returns
    my_df: dataframe filled with bound values we compute
    """
    # make a copy of the df with all values as nan
    my_df = df.copy()
    my_df.loc[:, :] = np.nan

    # fill all values that aren't nans in the original df
    for t in my_df.index:
        # print("t:", t)
        for n in my_df.columns.get_level_values(0).unique():
            # print("n:", n)
            lb_val = df[n]['l'].loc[t]
            
            # only fill if value in original df
            if not np.isnan(lb_val):
                lb, ub = get_lb_ub(t, n, alpha)
                my_df.loc[t, n] = [round(100*lb), round(100*ub)]
    
    return my_df


def get_lb_ub(t_o, n, alpha):
    """
    Inputs
    t_o: value of the test statistic
    n: number of samples
    alpha: miscoverage rate

    Returns
    p_lb, p_ub: lower and upper confidence bounds
    """
    # check edge cases
    # see "Nonoptimality of Randomized Confidence Sets" by Casella
    if t_o < alpha:
        p_lb, p_ub = 0, 0
    elif t_o > n + 1-alpha:
        p_lb, p_ub = 1, 1
    else:
        # typical case
        p_lb = UMAU_lb(t_o, n, alpha)
        p_ub = UMAU_ub(t_o, n, alpha)
    return p_lb, p_ub






#########################################
################# Tests #################
#########################################

def test_lb():
    """
    Tests 
    1. Our non-randomized lower confidence bound is equivalent to Clopper-Pearson
    2. Our randomized lower confidence bound is always greater than the non-randomized version
    """
    for n in ns:
        print("\nn:", n)
        for alpha in alphas:
            print("   alpha:", alpha)
            p_lb_prev = 0.0
            for k in range(n):
                print("      k:", k)
                p_lb = binom_ci(k, n, alpha, side='lb', randomized=True, verbose=False)
                p_lb_cp = binom_ci(k, n, alpha, side='lb', randomized=False, verbose=False)
                p_lb_cp_scipy = scipy_cp(k, n, alpha, side='lb')
                
                # check agreement up to 4 decimals
                assert isclose(p_lb_cp, p_lb_cp_scipy, abs_tol=10**-4)

                # check p_lb is between clopper pearson bounds
                assert round(p_lb, 4) >= round(p_lb_cp, 4)
                assert round(p_lb_prev, 4) <= round(p_lb_cp, 4)
                p_lb_prev = p_lb



def test_ub():
    """
    Tests 
    1. Our non-randomized upper confidence bound is equivalent to Clopper-Pearson
    2. Our randomized upper confidence bound is always less than the non-randomized version
    """
    for n in ns:
        print("\nn:", n)
        for alpha in alphas:
            print("   alpha:", alpha)
            p_ub_prev = 1.0
            for k in range(n, -1, -1):
                print("      k:", k)
                p_ub = binom_ci(k, n, alpha, side='ub', randomized=True, verbose=False)
                p_ub_cp = binom_ci(k, n, alpha, side='ub', randomized=False, verbose=False)
                p_ub_cp_scipy = scipy_cp(k, n, alpha, side='ub')
                
                # check up to 4 decimals
                assert isclose(p_ub_cp, p_ub_cp_scipy, abs_tol=10**-4)
                
                # check p_lb is between clopper pearson bounds
                assert round(p_ub, 4) <= round(p_ub_cp, 4)
                assert round(p_ub_prev, 4) >= round(p_ub_cp, 4)
                p_ub_prev = p_ub



def test_paper_data():
    """
    Test that functions don't error on the data used in the paper, 
    'How Generalizable Is My Behavior Cloning Policy? A Statistical Approach to Trustworthy Performance Evaluation'
    """
    
    # data from hardware experiment
    n = 50
    k1 = 38
    k2 = 4
    lb_pour_good = binom_ci(k1, 50, 0.05, 'lb', verbose=False)
    lb_pour_bad = binom_ci(k2, 50, 0.05, 'lb', verbose=False)


    # data from policy comparison experiment
    n_rollouts = np.array([50, 110, 30])
    vc1_successes = np.array([6, 12, 4])
    rt2_successes = np.array([40, 53, 16])

    alpha = 1-np.sqrt(0.95)

    vc1_ubs = np.array([binom_ci(vc1_successes[i], n_rollouts[i], alpha, 'ub', randomized=True, verbose=False) for i in range(3)])
    rt2_lbs = np.array([binom_ci(rt2_successes[i], n_rollouts[i], alpha, 'lb', randomized=True, verbose=False) for i in range(3)])

    return None



def test_2_sided():
    """
    Test that our 2-sided intervals match those in the 1960 paper:
    Table of Neyman-Shortest Unbiased Confidence Intervals for the Binomial Parameter
    by Colin R. Blyth and David W. Hutchinson
    """

    sheets = ['95_T1', '95_T2', '95_T3', '95_T4',
              '99_T1', '99_T2', '99_T3', '99_T4']

    for sheet in sheets:
        alpha = (100 - int(sheet[:2])) / 100

        # these values are from Blyth and Hutchinson's 1960 paper
        df = pd.read_excel('2_sided_val_table.xlsx', header=[0,1], index_col=0, sheet_name=sheet)
        df.index = np.round(df.index, 1) # make sure indices are rounded to 1 decimal place

        # these values are generated using our code
        our_df = fill_our_df(df, alpha)

        # check that our 2-sided bounds generally agree with the Blyth paper
        assert (our_df - df).abs().max().max() <= 1.0



def test_mixed_monotonicity():
    """
    Test that our values for MES, MEE, and MEW actually upper bound the
    sample-based maximum of these quantities
    """
    n = 10
    alpha = 0.05
    mes_ub, _, _, _ = max_expected_shortage(alpha, n, verbose=False)
    mee_ub, _, _, _ = max_expected_excess(alpha, n, verbose=False)
    mew_ub, _, _, _ = max_expected_width(alpha, n, verbose=False)

    sample_mes = max([expected_shortage(llc_accept_prob, alpha, n, p) for p in np.linspace(0.01, 0.99, num=50)])
    sample_mee = max([expected_excess(llc_accept_prob, alpha, n, p) for p in np.linspace(0.01, 0.99, num=50)])
    sample_mew = max([expected_width(llc_accept_prob_2_sided, alpha, n, p) for p in np.linspace(0.01, 0.99, num=50)])

    assert mes_ub >= sample_mes
    assert mee_ub >= sample_mee
    assert mew_ub >= sample_mew

