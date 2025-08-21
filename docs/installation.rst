Installation
============

Requirements
-----------

* Python 3.11 or higher
* pip (Python package installer)

Installation
-----------

Install from PyPI
~~~~~~~~~~~~~~~~~

The easiest way to install bhopengraph is using pip:

.. code-block:: bash

   pip install bhopengraph

Install from source
~~~~~~~~~~~~~~~~~~

If you want to install the latest development version, you can install directly from the GitHub repository:

.. code-block:: bash

   git clone https://github.com/p0dalirius/bhopengraph.git
   cd bhopengraph
   pip install -e .

Development installation
~~~~~~~~~~~~~~~~~~~~~~~

For development purposes, you can install the package in editable mode with all development dependencies:

.. code-block:: bash

   git clone https://github.com/p0dalirius/bhopengraph.git
   cd bhopengraph
   pip install -e ".[dev]"

Verifying the installation
-------------------------

To verify that bhopengraph has been installed correctly, you can run:

.. code-block:: python

   python -c "import bhopengraph; print(bhopengraph.__version__)"

This should output the version number of the installed package.

Upgrading
---------

To upgrade to the latest version:

.. code-block:: bash

   pip install --upgrade bhopengraph

Uninstalling
------------

To uninstall bhopengraph:

.. code-block:: bash

   pip uninstall bhopengraph
