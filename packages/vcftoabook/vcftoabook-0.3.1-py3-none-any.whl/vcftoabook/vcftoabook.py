from sys import exit
from os import path, listdir
from parser import parse_vcf


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
        if entry['custom1']:
            template += f'custom1={entry["custom1"]}\n'
    template += '\n'
    return template


def data_from_file(vcf):
    '''
    Load a vcf file and reutrn a list of contacts whose details
    include email addresses
    '''
    try:
        with open(path.abspath(vcf), 'r') as f:
            data = f.read().split('BEGIN:VCARD')
    except FileNotFoundError:
        exit(f'File not found: {vcf}')

    parsed = [parse_vcf(entry) for entry in data]

    return list(filter(lambda x: x['email'], parsed))


def write_addressbook(contacts, outfile):
    if not contacts:
        exit('Unable to write file: Input vcf is corrupt or invalid')

    contacts = sorted(contacts, key=lambda c: c['name'])

    if outfile:
        with open(path.abspath(outfile), 'w+') as f:
            f.write(build_template(contacts))
    else:
        with open('./addressbook', 'w+') as f:
            f.write(build_template(contacts))


def main(args):
    if (path.isdir(args.input)):
        dir_list = listdir(args.input)

        files = [
            f for f in dir_list if path.isfile(path.join(args.input, f))
            and path.splitext(f)[1] == '.vcf'
        ]

        contacts = []

        for f in files:
            contacts += data_from_file(path.join(args.input, f))

        write_addressbook(contacts, args.output)
    else:
        contacts = data_from_file(args.input)
        write_addressbook(contacts, args.output)
