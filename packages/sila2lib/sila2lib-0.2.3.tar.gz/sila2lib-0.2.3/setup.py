"""_____________________________________________________________________

:PROJECT: SiLA2_python

*SiLA2 python3 library setup*

:details: SiLA2 python3 libray setup. This installs the SiLA2 Python3 library.

:authors: mark doerr (mark@uni-greifswald.de)
          Florian Meinicke
          Timm Severin
          Maximilian Schulz (max@unitelabs.ch)

:date: (creation)    2019-8-29

.. todo:: - testing !!
________________________________________________________________________
"""

__version__ = "0.2.3"

from typing import List
import os

from setuptools import setup, find_packages

package_name = 'sila2lib'

def read(filename):
    with open(os.path.join(os.path.dirname(__file__), filename), 'r') as file:
        return file.read()


def generate_package_data(input_path: str, ending: str = '') -> List[str]:
    paths = []
    for (path, _, files) in os.walk(input_path):
        paths.extend([os.path.join('..', path, file) for file in files if file.endswith(ending)])

    return paths

setup(
    name=package_name,
    version=__version__,
    description='sila2lib - a SiLA 2 python3 library ',
    long_description=read('README.rst'),
    author=', '.join([
        'Mark Doerr',
        'Timm Severin (timm.severin@tum.de)',
        'Robert Giessmann (robert.giessmann@tu-berlin.de)',
        'Florian Meinicke',
        'Maximilian Schulz (max@unitelabs.ch)'
    ]),
    author_email='mark.doerr@uni-greifswald.de',
    keywords=('SiLA 2, lab automation, laboratory, instruments,'
              'experiments, evaluation, visualisation, serial interface, robots'),
    url='https://gitlab.com/SiLA2/sila_python',
    license='MIT',
    packages=find_packages(),
    install_requires=["grpcio>=1.7", "grpcio-tools", "lxml", "zeroconf"],
    test_suite='',
    classifiers=['License :: OSI Approved :: MIT License',
                 'Intended Audience :: Developers',
                 'Operating System :: OS Independent',
                 'Programming Language :: Python',
                 'Programming Language :: Python :: 3.6',
                 'Programming Language :: Python :: 3.7',
                 'Topic :: Utilities',
                 'Topic :: Scientific/Engineering',
                 'Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator',
                 'Topic :: Scientific/Engineering :: Information Analysis'],
    include_package_data=True,
    package_data={
        package_name:
            generate_package_data('sila2lib/framework', '.sila.xml')
            + generate_package_data('sila2lib/framework', '.proto')
            + generate_package_data('sila2lib/framework/schema', '.xsd')
            + generate_package_data('sila2lib/framework/std_features', '.pyi')
            + generate_package_data('sila2lib/framework/std_features', '.typed')
    },
    setup_requires=['wheel']
)
