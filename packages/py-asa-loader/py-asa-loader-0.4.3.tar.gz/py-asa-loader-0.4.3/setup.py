import os
import asaloader

from setuptools import setup, find_packages
from utils.l10n import create_mo_files, get_l10n_files

REQUIREMENTS = [
    'setuptools',
    'pyserial',
    'progressbar2',
]

create_mo_files()

l10n_files = get_l10n_files()
data_files = [(os.path.split(f)[0], [f]) for f in l10n_files]

setup(
    name='py-asa-loader',
    version=asaloader.__version__,
    description='The program to load binary into ASA series board.',
    long_description='',
    author='MVMC-lab',
    author_email='ncumvmclab@gmail.com',
    url='https://gitlab.com/MVMC-lab/hervor/py-asa-loader',
    license='MIT',
    packages=['asaloader'],
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'asaloader = asaloader.__main__:run'
        ],
    },
    data_files=data_files,
    install_requires=REQUIREMENTS
)
