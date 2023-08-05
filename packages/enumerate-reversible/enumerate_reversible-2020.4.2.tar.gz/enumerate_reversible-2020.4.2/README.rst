.. image:: https://travis-ci.org/cjrh/enumerate_reversible.svg?branch=master
    :target: https://travis-ci.org/cjrh/enumerate_reversible

.. image:: https://coveralls.io/repos/github/cjrh/enumerate_reversible/badge.svg?branch=master
    :target: https://coveralls.io/github/cjrh/enumerate_reversible?branch=master

.. image:: https://img.shields.io/pypi/pyversions/enumerate_reversible.svg
    :target: https://pypi.python.org/pypi/enumerate_reversible

.. image:: https://img.shields.io/github/tag/cjrh/enumerate_reversible.svg
    :target: https://img.shields.io/github/tag/cjrh/enumerate_reversible.svg

.. image:: https://img.shields.io/badge/install-pip%20install%20enumerate_reversible-ff69b4.svg
    :target: https://img.shields.io/badge/install-pip%20install%20enumerate_reversible-ff69b4.svg

.. image:: https://img.shields.io/pypi/v/enumerate_reversible.svg
    :target: https://img.shields.io/pypi/v/enumerate_reversible.svg

.. image:: https://img.shields.io/badge/calver-YYYY.MM.MINOR-22bfda.svg
    :target: http://calver.org/


enumerate_reversible
====================

Alternative to the builtin ``enumerate()``, that can be fed into another
builtin, ``reversed()``, as long as the collection being passed in implements
the ``Sized`` abstract base class, which means that it implements
``__len__()``. Note that it does not need to implement ``__getitem__``.
