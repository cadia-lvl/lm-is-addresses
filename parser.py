import argparse
import csv
import sys


parser = argparse.ArgumentParser(description='Parse a CSV file with addresses.')
parser.add_argument('file', type=argparse.FileType('r'), help='CSV file with addresses')
parser.add_argument('--output', type=argparse.FileType('w'), default='-', help='Output file')
args = parser.parse_args()


def load_area_codes(fname):
    """
    Loads area codes from a CSV file.
    """
    with open(fname, 'r') as f:
        reader = csv.DictReader(f, delimiter=';')
        for line in reader:
            yield line["Póstnúmer"], "{} {}".format(line["Póstnúmer"], line["Staður"])


def load_data(fname):
    """
    Loads data from a CSV file.
    """
    with open(fname, 'r') as f:
        reader = csv.DictReader(f)
        for line in reader:
            yield line


def print_line(line):
    print("="*10)
    for key, val in line.items():
        print(key, val)

def create_addresses(line, area_codes):
    area_code = line["POSTNR"]
    area_name = f", {area_codes[area_code]}" if area_code else ""
    yield "{} {}".format(line["HEITI_NF"], line["HUSNR"])
    yield "{} {}".format(line["HEITI_TGF"], line["HUSNR"])
    yield "{} {}{}".format(line["HEITI_NF"], line["HUSNR"], area_name)
    yield "{} {}{}".format(line["HEITI_TGF"], line["HUSNR"], area_name)


def create_address_list(fname, area_codes):
    for line in load_data(fname):
        for address in create_addresses(line, area_codes):
            yield address


if __name__ == '__main__':
    if args.output == "-":
        fout = sys.stdout
    else:
        fout = open(args.output.name, 'w')

    area_codes = {}
    for area_code, area_name in load_area_codes("raw/postnumer.txt"):
        area_codes[area_code] = area_name

    for address in create_address_list(args.file.name, area_codes):
        print(address, file=fout)