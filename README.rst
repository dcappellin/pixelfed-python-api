Pixelfed Python API
===================
A limited Python library for Pixelfed (https://pixelfed.org). Only few methods are implemented.

Authentication
==============
You need a token from a Pixelfed instance. Navigate to /settings/applications on the Pixelfed instance and generate a new Personal Access Tokens. Use that token for authentication.
The token must be available in the environment variable PIXELFED_API_TOKEN.

Pixelfed Domain
===============
The domain can be stored in the environment variable PIXELFED_DOMAIN_URI or passed as a parameter to the ``Pixelfed()`` constructor.

Installing
===========

.. code-block:: bash

    pip install pixelfed-python-api

Usage
=====

.. code-block:: bash

    >>> from pixelfed_python_api import Pixelfed
    >>> pfi = Pixelfed().instance()
    >>> print(pfi['version'])
    '2.7.2 (compatible; Pixelfed 0.11.4)'
