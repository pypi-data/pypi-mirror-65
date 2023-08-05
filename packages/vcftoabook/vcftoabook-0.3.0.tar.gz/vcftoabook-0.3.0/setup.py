import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

VERSION = "0.3.0"

setuptools.setup(
    name="vcftoabook",
    version=VERSION,
    author="Trevor Richards",
    author_email="trev@trevdev.ca",
    description="A cli tool for converting vcf files to abook",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/trev-dev/vcftoabook",
    packages=['vcftoabook'],
    entry_points={
        "console_scripts": ["vcftoabook=vcftoabook.cli:main"],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Topic :: Communications :: Email :: Address Book"
    ],
    python_requires='>=3.6',
)
