import os
import setuptools

README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setuptools.setup(
    name='whois_alt',
    version='2.4.4',
    packages=['whois_alt'],
    package_dir={"whois_alt":"whois_alt"},
    package_data={"whois_alt":["*.dat"]},
    install_requires=['argparse'],
    provides=['whois_alt'],
    scripts=["pwhois"],

    license="MIT",
    description='Module for retrieving and parsing the WHOIS data for a domain. Supports most domains. No dependencies. '
                'Fork of pythonwhois-alt as we need quick bug fixes',
    long_description=README,
    long_description_content_type="text/markdown",
    keywords='whois nic domain',

    author='KeyChest',
    author_email='support@keychest.net',
    url='https://gitlab.com/keychest/whois-alt-for-python',

    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Internet :: Name Service (DNS)',
    ],
)
