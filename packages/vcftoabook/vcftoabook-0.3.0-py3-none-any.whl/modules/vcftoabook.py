import re
import argparse
from sys import exit
from os import path


def parse_data(items):
    """
    Parse strings from vcf data and attempt to return the type and data
    """
    items = list(filter(lambda x: x != '', items.split('\n')))

    entry = {
        'name': '',
        'email': set(),
        'notes': ''
    }

    for item in items:
        if 'FN:' in item:
            entry['name'] = item.split(':')[1]
        elif 'EMAIL;' in item:
            entry['email'].add(item.split(':')[1])
        elif 'NOTE:' in item:
            entry['notes'] = re.search(r'NOTE:(.+)', item).group(1)

    return entry


def build_template(data):
    """
    Build and return an addressbook file template
    """
    template = (
        '# abook addressbook file\n\n'
        '[format]\n'
        'program=abook\n'
        'version=0.6.1\n\n'
    )

    for index, entry in enumerate(data):
        template += (
            f'\n[{index}]\n'
            f'name={entry["name"]}\n'
            f'email={",".join(entry["email"])}\n'
        )
        if entry["notes"]:
            template += f'notes={entry["notes"]}\n'
    template += '\n'
    return template


def main(args):
    try:
        with open(path.abspath(args.input), 'r') as f:
            data = f.read().split('BEGIN:VCARD')
    except FileNotFoundError:
        exit(f'File not found: {path.abspath(args.input)}')

    parsed_data = [parse_data(entry) for entry in data]

    # Prune contacts with no email address entered
    contacts = list(filter(lambda x: x['email'], parsed_data))

    # Don't write anything to disk if contacts are empty
    if not contacts:
        exit('Unable to write file: Input vcf is corrupt or invalid')
    if args.output:
        with open(path.abspath(args.output), 'w+') as f:
            f.write(build_template(contacts))
    else:
        with open('./addressbook', 'w+') as f:
            f.write(build_template(contacts))


parser = argparse.ArgumentParser(
    prog="vcftoabook",
    description="Convert .vcf files into addressbook files to be used in "
                "abook/Mutt"
)

parser.add_argument(
    '-i', '--input',
    metavar='input',
    type=str,
    help="the input path of a .vcf file"
)

parser.add_argument(
    '-o', '--output',
    metavar="output",
    type=str,
    default='addressbook',
    help="the output path/filename (default: ./addressbook)"
)

args = parser.parse_args()

if __name__ == '__main__':
    main(args)
