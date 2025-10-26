"""
Purpose
    Determine whether the number of runs of ones and zeros of various length
    is as expected for a random sequence

Description
    Compute the pre-test proportion π of ones in the input sequence: π = ∑ (j^ε j) / n
    
    Determine if the prerequisite Frequency test is passed
        |π - 0.5| >= τ then no test needed
        p_value set to 0.0, τ = 2 / sqrt(n) has been pre-defined in the test code
    
    Compute the test statistic V_n(obs) = ∑ n -1, k = 1: r(k) + 1, where r(k) = 0 if ε_k = ε_k+1 and r(k) = 1 otherwise

    Compute the p_value = erfc(|V_n(obs) - 2nπ(1 - π))| / (2sqrt(2n)π(1-π)))

Decision Rule
    If the P-value is < 0.01, the sequence is non-random; otherwise random

Input Size Recommendation
    Each sequence tested should consist of a minimum of 100 bits

"""

from scipy import special
from math import sqrt

def test(bits):
    """
    Runs Test

    Parameters
    bits : list[int]
        Binary sequence (0/1) to test for randomness.

    Returns
    dict
        {'p_value': float, 'pass': bool}
    """

    n = len(bits)
    if n < 100:
        raise ValueError("Sequence must be at least 100 bits")

    # pre-test frequency check
    num_ones = sum(bits)
    pi = num_ones / n
    tau = 2 / sqrt(n)
    if abs(pi - 0.5) >= tau:
        return {'p_value': 0.0, 'pass': False}
    v_n_obs = 1
    for k in range(1, n):
        if bits[k] != bits[k - 1]:
            v_n_obs += 1
    p_value = special.erfc((abs(v_n_obs - 2 * n * pi * (1 - pi))) / (2 * sqrt(2 * n) * pi * (1 - pi)))

    result = p_value >= 0.01

    return {'p_value': p_value, 'pass': result}