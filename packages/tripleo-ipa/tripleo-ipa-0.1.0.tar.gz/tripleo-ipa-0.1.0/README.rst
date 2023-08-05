===========
tripleo-ipa
===========

This repository contains Ansible for use integrating TripleO with FreeIPA.

Installation
============

.. code-block:: bash

   $ pip install --prefix=/usr tripleo-ipa

Or, if you are installing from source, in the project directory:

.. code-block:: bash

   $ python setup.py install --prefix=/usr


Contributing
============

You can create an environment to develop locally using the following.

.. code-block:: bash

   $ python3.7 -m virtualenv --system-site-packages .venv
   $ .venv/bin/pip3 install -r molecule-requirements.txt
