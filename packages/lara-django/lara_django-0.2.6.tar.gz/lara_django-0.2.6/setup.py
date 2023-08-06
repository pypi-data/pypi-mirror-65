"""_____________________________________________________________________

:PROJECT: LARA

*lara_django setup *

:details: lara_people setup file for installation.
         - For installation, run:
           run pip3 install .
           or  python3 setup.py install

:file:    setup.py
:authors:

:date: (creation)         2019-10-16

.. note:: -
.. todo:: -
________________________________________________________________________
"""
__version__ = "0.2.6"

import os
import sys

from setuptools import setup, find_packages

package_name = 'lara_django'

def read(filename):
    with open(os.path.join(os.path.dirname(__file__), filename), 'r') as file:
        return file.read().strip()

install_requires = ['Django>=3,<3.2', 'django-autoadmin>=1.1,<2']
#lara-django-containers
#lara-django-data
#lara-django-devices
#lara-django-labstore
#lara-django-library
#lara-django-material
#lara-django-ordering-concepts
#lara-django-organism
#lara-django-organisms-store
#lara-django-parts
#lara-django-people
#lara-django-processes
#lara-django-projects
#lara-django-sequences
#lara-django-substances
#lara-django-substances-store
#lara-simpleprocman
#lara-aggregator

data_files = []

package_data = {package_name: [
                               'static/css/*.css',
                               'static/js/*.js',
                               'static/icons/*.svg'
                              ]}

setup(name=package_name,
    version=__version__,
    description='LARA-django is a python django project of the Lab Automation Suite LARA - (lara.uni-greifswald.de/larasuite) ',
    long_description=read('README.rst'),
    long_description_content_type='text/x-rst',
    author='mark doerr',
    author_email='mark.doerr@uni-greifswald.de',
    keywords='lab automation, experiments, database, evaluation, visualisation, SiLA2, robots',
    url='https://gitlab.com/LARAsuite/lara-django',
    license='GPL',
    packages=find_packages(), #['lara_django'],
    #~ package_dir={'lara_django':'lara_django'},
    scripts=['lara_django/bin/lara-django.py'],
    install_requires = install_requires,
    test_suite='',
    classifiers=[  'Development Status :: 3 - Alpha',
                   'Environment :: Console',
                   'Framework :: Django :: 3.0',
                   'Intended Audience :: Developers',
                   'Intended Audience :: Science/Research',
                   'Intended Audience :: Education',
                   'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Programming Language :: Python :: 3.7',
                   'Programming Language :: Python :: 3.8',
                   'Topic :: Scientific/Engineering',
                   'Topic :: Scientific/Engineering :: Information Analysis',
                   'Topic :: Scientific/Engineering :: Visualization',
                   'Topic :: Scientific/Engineering :: Bio-Informatics',
                   'Topic :: Scientific/Engineering :: Chemistry'
                ],
    include_package_data=True,
    package_data = package_data,
    data_files=data_files,
)
