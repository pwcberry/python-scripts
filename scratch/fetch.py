from argparse import ArgumentParser

def main(source_url: str, output_dir: str) -> None:
    print(f"{source_url} downloads to {output_dir}")

if __name__ == '__main__':
    parser = ArgumentParser()
    # `source` must include domain and protocol
    parser.add_argument("source", type=str)
    # `output` must be an existing directory
    parser.add_argument("output", type=str)

    args = parser.parse_args()
    main(args.source, args.output)
