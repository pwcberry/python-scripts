from csv import DictReader
from argparse import ArgumentParser
import json

# Open source file

# Map data types from RDBMS to BQ
## bigint -> INTEGER (64 bit)
## character varying -> STRING
## integer -> INTEGER (32 bit)
## uuid -> STRING
## timestamp -> TIMESTAMP
## jsonb -> JSON
## text -> STRING
## double precision -> NUMERIC / FLOAT

# Map modes
## not nullable -> REQUIRED
## nullable -> NULLABLE

class TableField:
    def __init__(self, name, field_type, nullable, description):
        self.name = name
        self.type = field_type
        self.mode = "NULLABLE" if nullable else "REQUIRED"
        self.description = description

# Ensure we can encode the type into JSON
class TableFieldEncoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__

def map_type(sql_type):
    match sql_type:
        case "bigint" | "integer":
            return "INT64"
        case "character varying" | "text" | "uuid":
            return "STRING"
        case "timestamp":
            return "TIMESTAMP"
        case "double precision":
            return "FLOAT64"
        case "jsonb":
            return "JSON"
        case "date":
            return "DATE"
        case "boolean":
            return "BOOLEAN"
        case _:
            return "UNKNOWN"

def is_nullable(value):
    return False if value == "not null" else True

def set_description(name, table_name, is_pi):
    if is_pi:
        return "This field contains personal information. DO NOT USE"
    else:
        return 'This is the field "{}" of table "{}"'.format(name, table_name)

def check_for_id(column, table_name):
    if column == "id":
        return f"{table_name}_id"
    else:
        return column

def main(args):
    tables = {}

    with open(args.source) as csvfile:
        reader = DictReader(csvfile)
        fields = []

        for row in reader:
            table_name = row["table_name"]
            if table_name not in tables:
                fields = tables[table_name] = []

            field = TableField(
                check_for_id(row["column"], table_name),
                map_type(row["type"]),
                is_nullable(row["nullable"]),
                set_description(row["column"], table_name, row["pi"])
            )

            if field.mode == "REQUIRED" and field.type == "TIMESTAMP":
                field.defaultValueExpression = "CURRENT_TIMESTAMP"

            fields.append(field)

    for table_name in tables.keys():
        with open(f"./output/schema/{table_name}.json", "w") as jsonfile:
            json.dump(tables[table_name], jsonfile, indent=2, cls=TableFieldEncoder)

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("source", type=str)
    parser.add_argument("output", type=str)
    main(parser.parse_args())
