from argparse import ArgumentParser
import my_math

def main(a: int, b: int) -> None:
    result = my_math.raise_to_power(a,b)
    print(f"{a} raised to the power of {b} is {result}")

if __name__ == '__main__':
    parser = ArgumentParser()
    # `source` must include domain and protocol
    parser.add_argument("base", type=int)
    # `output` must be an existing directory
    parser.add_argument("power", type=int)

    args = parser.parse_args()
    main(args.base, args.power)
