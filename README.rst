=============
Mini Vouchers
=============

A minimal implementation of a voucher system.

Usage
-----

TODO

Installation
------------

Simply install using the setup command, e.g. within a virtual environment:

.. code-block:: shell

    $ virtualenv -p python3 venv
    $ . ./venv/bin/activate
    (venv)$ pip install .

Requirements
^^^^^^^^^^^^

Python 3.6 is required.

Development
^^^^^^^^^^^

The Python files are formatted with `Black`_ and linted with `flake8`_ and
`pylint`_.
A `pre-commit`_ hook is defined to automate the mundane work.

To start developing, initialise the development environment and install the
pre-commit hook with:

.. code-block:: shell

    $ virtualenv -p python3 venv
    $ . ./venv/bin/activate
    (venv)$ pip install -r requirements-dev.txt
    (venv)$ pre-commit install

License
-------

This project is free software and licensed under the GNU General Public License
v3 or later.

Authors
-------

`mini-vouchers` was written by `Borjan Tchakaloff <borjan@tchakaloff.fr>`_.

Credits
-------

This package was created with `Cookiecutter`_ and is based on the
`audreyr/cookiecutter-pypackage`_ and
`kragniz/cookiecutter-pypackage-minimal`_ project templates.

.. _`Black`: https://github.com/ambv/black
.. _`Cookiecutter`: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`:
    https://github.com/audreyr/cookiecutter-pypackage
.. _`flake8`: https://gitlab.com/pycqa/flake8
.. _`kragniz/cookiecutter-pypackage-minimal`:
    https://github.com/kragniz/cookiecutter-pypackage-minimal
.. _`pre-commit`: https://pre-commit.com
.. _`pylint`: https://github.com/PyCQA/pylint
