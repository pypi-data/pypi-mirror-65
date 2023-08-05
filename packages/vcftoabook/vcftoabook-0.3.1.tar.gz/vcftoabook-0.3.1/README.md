# VCF to addressbook

A python script for converting .vcf contact files into abook files to be used in the addressbook program for Mutt/Neomutt

**Note:** This project is in the Alpha stage. Help with testing on various distros/vcf versions would be appreciated

## Requirements
* Python 3.6+

## Installation

Run `pip install --user vcftoabook`

## Usage

Simply run `vcftoabook file.vcf` to generate an addressbook file. Vcftoabook also works on directories and will parse all the .vcf files in a given directory and output one addressbook file. You may also specify an output file/path with `vcftoabook file.vcf -o <path>/<filename>`. Run `vcftoabook -h` for help.

## Testing
Currently tested with:
* Arch Linux
* Nextcloud 16.x VCF version 4

## TODO
- [x] Refactor into a proper command line application
- [x] Test with multiple vcf versions.
- [x] Ability to add directory of vcf files
- [ ] Ability to update existing addressbook with new contacts/emails
- [ ] vdirsyncer/caldav support(?)
- [-] Build deployment packages
  - [ ] AUR
  - [x] Pypi

License: [GPLv3](https://www.gnu.org/licenses/gpl-3.0.en.html)
