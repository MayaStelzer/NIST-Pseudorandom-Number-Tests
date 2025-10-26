"""
Purpose
    Test the proportion of ones within M-bit blocks to determine whether the frequency
    of ones in an M-bit block is approximately M/2

Description
    Partition the input sequence into N = |n / M| (floor) non-overlapping blocks, discarding any unused bits

    Determine the proportion of π_i of ones in each M-bit block using π_i = ∑M, j = 1 ε(i - 1)M +j / M for 1 <= i <= N

    Compute the X^2 statistic X^2(obs) = 4 M ∑ (π - 1/2)^2

    Compute the P_value = igamc(N/2, X^2(obs)/2) 

Decision Rule
    If the P-value is < 0.01, the sequence is non-random; otherwise random

Input Size Recommendation
    Each sequence tested should consist of a minimum of 100 bits

"""

from scipy import special
import math

def test(bits, block_size=28):
    """
    Frequency Test within a Block

    Parameters
    bits : list[int]
        Binary sequence (0/1) to test for randomness.

    Returns
    dict
        {'p_value': float, 'pass': bool}
    """

    n = len(bits)
    M = block_size
    if n < 100:
        raise ValueError("Sequence must be at least 100 bits")
    if block_size <= 0 or block_size > n:
        raise ValueError("Invalid block size")
    
    N = n // M
    if N == 0:
        raise ValueError("Block size too large")

    chi2 = 0.0
    for i in range(N):
        block = bits[i*M:(i+1)*block_size]
        pi_i = sum(block) / M
        chi2 += (pi_i - 0.5) ** 2
    
    chi2_obs = 4.0 * M * chi2

    p_value = special.gammaincc(N / 2, chi2_obs / 2)

    return {
        "p_value": p_value,
        "pass": p_value >= 0.01
    }