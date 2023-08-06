import configparser
from sys import exit
from os import path, listdir
import re


def parse_vcf(items):
    """
    Parse data from a vcf and attempt to return a usable dictionary
    """
    items = list(filter(lambda x: x != '', items.split('\n')))

    entry = {
        'name': '',
        'email': set(),
        'notes': '',
        'custom1': ''
    }

    for item in items:
        if 'FN:' in item:
            entry['name'] = item.split(':')[1]
        elif 'EMAIL;' in item:
            entry['email'].add(item.split(':')[1])
        elif 'NOTE:' in item:
            entry['notes'] = re.search(r'NOTE:(.+)', item).group(1)
        elif 'UID:' in item:
            entry['custom1'] = item.split(':')[1]

    return entry


def parse_contact(contact, configparser):
    """
    Parse data from an abook file and return a usable dictionary
    """

    return {
        'name': configparser[contact].get('name'),
        'email': set(configparser[contact].get('email').split(',')),
        'notes': configparser[contact].get('notes'),
        'custom1': configparser[contact].get('custom1')
    }


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
    match_count = 0
    new_count = 0
    for new_contact in new:
        match = False
        for contact in existing:
            if new_contact['custom1'] == contact['custom1']:
                contact['email'] = contact['email'].union(new_contact['email'])
                match_count += 1
                match = True
                break

        if not match:
            existing.append(new_contact)
            new_count += 1

    print(f'\n{match_count} contacts merged into addressbook')
    print(f'{new_count} new contacts added')
    
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
