"""
Purpose
    Determine whether the number of ones and zeros in a sequence are approximately 
    the same as would be expected for a truly random sequence

Description
    Conversion to += 1: The zeros and ones of the input sequence are converted to -1 and 1 
    and added together to produce S_n

    Compute the test statistic s_obs = |S_n|/sqrt(n)

    Compute P-value = erfc((s_obs)/sqrt(2))

Decision Rule
    If the P-value is < 0.01, the sequence is non-random; otherwise random

Input Size Recommendation
    Each sequence tested should consist of a minimum of 100 bits
"""

from scipy import special

def test(bits):
    """
    Monobit (Frequency) Test

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
    transformed = [1 if bit else -1 for bit in bits]

    s_n = sum(transformed)
    s_obs = abs(s_n) / (n ** 0.5)
    p_value = special.erfc(s_obs / (2 ** 0.5))

    return {
        "p_value": p_value,
        "pass": p_value >= 0.01
    }
