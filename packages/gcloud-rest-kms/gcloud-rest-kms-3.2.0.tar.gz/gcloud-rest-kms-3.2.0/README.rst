(Asyncio OR Threadsafe) Python Client for Google Cloud KMS
==========================================================

    This is a shared codebase for ``gcloud-rest-kms`` and ``gcloud-rest-kms``

|pypi| |pythons-aio| |pythons-rest|

Installation
------------

.. code-block:: console

    $ pip install --upgrade gcloud-{aio,rest}-kms

Usage
-----

We're still working on more complete documentation, but roughly you can do:

.. code-block:: python

    from gcloud.rest.kms import KMS
    from gcloud.rest.kms import decode
    from gcloud.rest.kms import encode

    kms = KMS('my-kms-project', 'my-keyring', 'my-key-name')

    # encrypt
    plaintext = 'the-best-animal-is-the-aardvark'
    ciphertext = await kms.encrypt(encode(plaintext))

    # decrypt
    assert decode(await kms.decrypt(ciphertext)) == plaintext

    # close the HTTP session
    # Note that other options include:
    # * providing your own session: `KMS(.., session=session)`
    # * using a context manager: `async with KMS(..) as kms:`
    await kms.close()

Contributing
------------

Please see our `contributing guide`_.

.. _contributing guide: https://github.com/talkiq/gcloud-rest/blob/master/.github/CONTRIBUTING.rst

.. |pypi| image:: https://img.shields.io/pypi/v/gcloud-rest-kms.svg?style=flat-square
    :alt: Latest PyPI Version (gcloud-rest-kms)
    :target: https://pypi.org/project/gcloud-rest-kms/

.. |pythons-aio| image:: https://img.shields.io/pypi/pyversions/gcloud-rest-kms.svg?style=flat-square&label=python (aio)
    :alt: Python Version Support (gcloud-rest-kms)
    :target: https://pypi.org/project/gcloud-rest-kms/

.. |pythons-rest| image:: https://img.shields.io/pypi/pyversions/gcloud-rest-kms.svg?style=flat-square&label=python (rest)
    :alt: Python Version Support (gcloud-rest-kms)
    :target: https://pypi.org/project/gcloud-rest-kms/
