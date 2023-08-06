# VCF to addressbook

A python script for converting .vcf contact files into abook files to be used in the addressbook program for Mutt/Neomutt.

**Note:** This project is in the Alpha stage. Help with testing on various distros/vcf versions would be appreciated

## Requirements
* Python 3.6+

## Installation

Run `pip install --user vcftoabook`

## Usage

Simply run `vcftoabook file.vcf` to generate an addressbook file. VCFtoAbook also works on directories and will parse all the .vcf files in a given directory and output one addressbook file. You may also specify an output file/path with `vcftoabook file.vcf -o <path>/<filename>`. Run `vcftoabook -h` for help.

To update an existing addressbook file, specify the `-a` flag and point your `-o` flag at the path to your addressbook file. VCFtoAbook will attempt to merge new incoming contacts with your existing ones and _overwrite_ your output addressbook. Backups not included. Example: `vcftoabook -ao ~/.abook/addressbook somecontact.vcf`

License: [GPLv3](https://www.gnu.org/licenses/gpl-3.0.en.html)
