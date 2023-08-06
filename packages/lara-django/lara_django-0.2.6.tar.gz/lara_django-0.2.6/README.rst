lara-django
===========

LARA django is a collection of applications for storing, evaluating and presenting experimental data and its meta data, based on python-django.
LARA has the following features:

    * holistic approach, which covers:
      - project planning 
      - process generation and organisation
      - container management (barcodes, layout)
      - data evaluation and visualisation
      - subtances management and ordering
      - user management
    * small, efficient and fast code
    * modular, fully flexible plugin architecture, support for virtually any open programming language
    
    image:: docs/figures/lara-django-menu.png 


Overview of the packages
_________________________

  * lara-django [core]   - core of the lara-django project (required)
  * lara-people [core]   - management of all users/institutions/addresses
  * lara-projects [core] - management of all projects and experiments
  * lara-data [core]     - all data goes here
  * lara-metainfo [core] - all kind of meta information goes here
  
  * lara-substances [optional] - chemicals, substances, DNA, proteins
  * lara-devices    [optional] - lab devices
  

Installation of lara-django
___________________________

The simplest way to install lara-django and the rest of the core packages, simply execute

  cd [lara-django repository directory]
  python3 install-lara-django.py 


This will guide you through the complete setup


lara-django django can be installed : plain and in a virtual python environment (venv).

The recommended way to install lara-django is to install it in a virtualenv environment.

    
Acknowledgements
________________

The LARA-django developers thank 

    * the python team
    * the R team
    * the whole django team (https://www.djangoproject.com/) for their great tool !
    * mptt developers
    * the blockly team (https://developers.google.com/blockly/ and https://github.com/google/blockly) for their visual programming language
    * Vladimir (Владимир) from pyinto (https://github.com/pyinto) for his inspirations on how to setup the ordering system and what you can do with css and JavaSkript
    

References
__________

.. _pip: https://pypi.python.org/pypi/pip
.. _virtualenv: https://pypi.python.org/pypi/virtualenv
.. _virtualenvwrapper: http://virtualenvwrapper.readthedocs.org/
