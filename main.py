from bit_generator import generate_bits
from nist_tests import monobit, frequency_block, runs_test, longest_run

def main():
    bits = generate_bits(100)
    more_bits = generate_bits(150)
    print("Monobit test:", monobit.test(bits))
    print("Frequency block test:", frequency_block.test(bits))
    print("Runs test:", runs_test.test(bits))
    print("Longest runs test:", longest_run.test(more_bits))

if __name__ == "__main__":
    main()