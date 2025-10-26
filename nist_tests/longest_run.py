"""
Purpose
    Determine whether the length of the longest run of ones within the tested sequence is consistent 
    with the length of the longest run of ones that would be expected in a random sequence
    
Description
    Divide the sequence into M-bit blocks

    Tabulate the frequencies v_i of the longest runs of ones in each block into categories,
    where each cell contains the number of runs of ones of a given length

    Compute X^2(obs) = ∑ K, i = 0: (v_i - Nπ_i)^2 / (Nπ_i)

    Compute the P_value = igamc(K / 2, X^2(obs) / 2)
    
Decision Rule
    If the P-value is < 0.01, the sequence is non-random; otherwise random

Input Size Recommendation
    Each sequence tested should consist of a minimum of 128 bits if M = 8, 6272 if M = 128, 750000 if M = 10^4


"""

from scipy import special
from math import sqrt

def test(bits, M=8):
    """
    Longest Run of Ones in a Block

    Parameters
    bits : list[int]
        Binary sequence (0/1) to test for randomness.

    Returns
    dict
        {'p_value': float, 'pass': bool}
    """

    n = len(bits)
    if M == 8 and n < 128:
        raise ValueError("Sequence must be at least 128 bits for M=8")
    elif M == 128 and n < 6272:
        raise ValueError("Sequence must be at least 6272 bits for M=128")
    elif M == 10000 and n < 750000:
        raise ValueError("Sequence must be at least 750000 bits for M=10000")

    N = n // M
    blocks = [bits[i*M:(i+1)*M] for i in range(N)]

    longest_runs = []
    for block in blocks:
        max_run = 0
        current_run = 0
        for bit in block:
            if bit == 1:
                current_run += 1
                max_run = max(max_run, current_run)
            else:
                current_run = 0
        longest_runs.append(max_run)

    categories = [1, 2, 3, 4]
    pi = [0.2148, 0.3672, 0.2305, 0.1875]

    v = [0] * len(categories)
    for run in longest_runs:
        if run <= 1:
            v[0] += 1
        elif run == 2:
            v[1] += 1
        elif run == 3:
            v[2] += 1
        else:  # run >= 4
            v[3] += 1


    X2 = sum((v[i] - N*pi[i])**2 / (N*pi[i]) for i in range(len(categories)))

    p_value = special.gammaincc(len(categories)/2, X2/2)

    result = p_value >= 0.01

    return {'p_value': p_value, 'pass': result}