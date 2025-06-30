from csv import DictReader, QUOTE_NOTNULL
from argparse import ArgumentParser
from pathlib import Path
import json

parser = ArgumentParser()
parser.add_argument("source", type=str)
parser.add_argument("table", type=str)

def main(args):
    input_path = Path(args.source)
    table_name = args.table
    output_path = Path(f"./output/data/{table_name}.nljson")

    with open(output_path, "w") as outfile:
        with open(input_path) as csvfile:
            reader = DictReader(csvfile, quoting=QUOTE_NOTNULL)
            for row in reader:
                json.dump(row, outfile, indent=None, ensure_ascii=True, sort_keys=True)
                outfile.write("\n")

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("source", type=str)
    parser.add_argument("table", type=str)
    main(parser.parse_args())
