import argparse
import vcftoabook


def main():
    parser = argparse.ArgumentParser(
        prog="vcftoabook",
        description="Convert .vcf files into addressbook files to be used in "
                    "abook/Mutt"
    )

    parser.add_argument(
        'input',
        type=str,
        help="the input path of a .vcf file, or directory full of .vcf files",
    )

    parser.add_argument(
        '-o',
        '--output',
        type=str,
        default='addressbook',
        help="the output path/filename (default: ./addressbook)"
    )

    '''
    parser.add_argument(
        '-a',
        '--add',
        help="append new contacts to existing address book"
    )
    '''
    args = parser.parse_args()

    vcftoabook.main(args)


if __name__ == '__main__':
    main()
