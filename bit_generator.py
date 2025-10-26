import secrets

def generate_bits(n):
    """Generate a random bitstring of length n"""
    return [secrets.randbits(1) for _ in range(n)]