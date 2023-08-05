.. start-badges

|travis| |appveyor| |requires| |codecov| |coveralls| |docs| |version| |wheel| |supported-versions| |supported-implementations|

.. |docs| image:: https://readthedocs.org/projects/python-asn1/badge/?style=flat
    :target: https://readthedocs.org/projects/python-asn1
    :alt: Documentation Status

.. |travis| image:: https://api.travis-ci.org/andrivet/python-asn1.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/andrivet/python-asn1

.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/andrivet/python-asn1?branch=master&svg=true
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/andrivet/python-asn1

.. |requires| image:: https://requires.io/github/andrivet/python-asn1/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/andrivet/python-asn1/requirements/?branch=master

.. |codecov| image:: https://codecov.io/gh/andrivet/python-asn1/branch/master/graphs/badge.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/andrivet/python-asn1

.. |version| image:: https://img.shields.io/pypi/v/asn1.svg?style=flat
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/asn1/

.. |wheel| image:: https://img.shields.io/pypi/wheel/asn1.svg?style=flat
    :alt: PyPI Wheel
    :target: https://pypi.org/project/asn1/

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/asn1.svg?style=flat
    :alt: Supported versions
    :target: https://pypi.org/project/asn1/

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/asn1.svg?style=flat
    :alt: Supported implementations
    :target: https://pypi.org/project/asn1/


.. end-badges

========
Overview
========

Python-ASN1 is a simple ASN.1 encoder and decoder for Python 2.7 and 3.5+.

Features
========

- Support BER (parser) and DER (parser and generator) encoding
- 100% python, compatible with version 2.6, 2.7, 3.3 and higher
- Can be integrated by just including a file into your project


Dependencies
==============

Python-ASN1 relies on `Python-Future <http://python-future.org>`_ for Python 2 and 3 compatibility. To install Python-Future:

.. code-block:: sh

  pip install future


How to install Python-asn1
==========================

Install from PyPi with the following:

.. code-block:: sh

  pip install asn1

or download the repository from `GitHub <https://github.com/andrivet/python-asn1>`_ and install with the following:

.. code-block:: sh

  python setup.py install

You can also simply include ``asn1.py`` into your project.


How to use Python-asn1
======================

.. note:: You can find more detailed documentation on the `Usage`_ page.

.. _Usage: usage.html

Encoding
--------

If you want to encode data and retrieve its DER-encoded representation, use code such as:

.. code-block:: python

  import asn1

  encoder = asn1.Encoder()
  encoder.start()
  encoder.write('1.2.3', asn1.Numbers.ObjectIdentifier)
  encoded_bytes = encoder.output()


Decoding
--------

If you want to decode ASN.1 from DER or BER encoded bytes, use code such as:

.. code-block:: python

  import asn1

  decoder = asn1.Decoder()
  decoder.start(encoded_bytes)
  tag, value = decoder.read()


Documentation
=============

The complete documentation is available on Read The Docs:

`python-asn1.readthedocs.io <https://python-asn1.readthedocs.io/en/latest/>`_


License
=======

Python-ASN1 is free software that is made available under the MIT license.
Consult the file LICENSE that is distributed together with this library for
the exact licensing terms.

Copyright
=========

The following people have contributed to Python-ASN1. Collectively they own the copyright of this software.

* Geert Jansen (geert@boskant.nl): `original implementation <https://github.com/geertj/python-asn1>`_.
* Sebastien Andrivet (sebastien@andrivet.com)
