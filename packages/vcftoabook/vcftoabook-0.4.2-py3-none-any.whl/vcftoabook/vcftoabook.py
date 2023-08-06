import configparser
from sys import exit
from os import path, listdir
from parser import parse_vcf, parse_contact


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


def contacts_from_abook(abookfile):
    '''
    Load an addressbook file and return a list of contact dictionaries
    '''
    abook = configparser.ConfigParser()
    abook.read(abookfile)

    contacts = [
        parse_contact(c, abook) for c in abook.sections() if c.isnumeric()
    ]

    return contacts


def contact_from_vcf(vcf):
    '''
    Load a vcf file and reutrn a list of contact dictionaries whose details
    include email addresses
    '''
    try:
        with open(path.abspath(vcf), 'r') as f:
            data = f.read().split('BEGIN:VCARD')
    except FileNotFoundError:
        exit(f'File not found: {vcf}')

    parsed = [parse_vcf(entry) for entry in data]

    return list(filter(lambda x: x['email'], parsed))


def append_into_existing(existing, new):
    for new_contact in new:
        match = False
        for contact in existing:
            if new_contact['custom1'] == contact['custom1']:
                contact['email'] = contact['email'].union(new_contact['email'])
                match = True
                break

        if not match:
            existing.append(new_contact)

    return existing


def write_addressbook(contacts, outfile):
    if not contacts:
        exit('Unable to write file: Input vcf is corrupt or invalid')

    contacts = sorted(contacts, key=lambda c: c['name'])

    if outfile:
        with open(path.abspath(outfile), 'w') as f:
            f.write(build_template(contacts))
    else:
        with open('./addressbook', 'w') as f:
            f.write(build_template(contacts))


def main(args):
    abook_exists = path.isfile(args.output)

    if (path.isdir(args.input)):
        dir_list = listdir(args.input)

        files = [
            f for f in dir_list if path.isfile(path.join(args.input, f))
            and path.splitext(f)[1] == '.vcf'
        ]

        contacts = []
        for f in files:
            contacts += contact_from_vcf(path.join(args.input, f))
    else:
        contacts = contact_from_vcf(args.input)

    if abook_exists and not args.append:
        print(
            f'File already exits at {args.output}\n'
            'Use -a to append to existing file\n'
        )
    elif abook_exists:
        existing_contacts = contacts_from_abook(args.output)
        merged_contacts = append_into_existing(existing_contacts, contacts)
        write_addressbook(merged_contacts, args.output)
    else:
        write_addressbook(contacts, args.output)
