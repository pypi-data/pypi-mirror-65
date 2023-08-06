=====
flats
=====

Python library for common functionalities related to flattening nested values of container types.

.. image:: https://badge.fury.io/py/flats.svg
   :target: https://badge.fury.io/py/flats
   :alt: PyPI version and link.

Package Installation and Usage
------------------------------
The package is available on PyPI::

    python -m pip install flats

The library can be imported in the usual ways::

    import flats
    from flats import flats

Examples
--------
Examples of usage are provided  below::

    >>> from flats import flats
    >>> list(flats([[1, [2, 3]], [4, 5, 6, 7]]))
    [1, 2, 3, 4, 5, 6, 7]
