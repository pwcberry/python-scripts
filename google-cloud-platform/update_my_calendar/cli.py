import argparse
import os.path


def data_source_file(extension):
    def validate(path):
        if not os.path.isfile(path):
            raise argparse.ArgumentTypeError(f"'{path}' does not exist or is not a file")
        if not path.lower().endswith(extension):
            raise argparse.ArgumentTypeError(f"'{path}' is not a {extension} file")
        return path

    return validate


def parse_data_source(description, extension):
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        "data_source",
        type=data_source_file(extension),
        help=f"path to the {extension} data source file",
    )
    return parser.parse_args().data_source
