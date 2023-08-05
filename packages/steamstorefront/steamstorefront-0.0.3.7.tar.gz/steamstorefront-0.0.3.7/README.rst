=================
Steam Store Front
=================

.. image:: https://img.shields.io/pypi/v/steamstorefront.svg?style=flat-square
        :target: https://pypi.python.org/pypi/steamstorefront

.. image:: https://img.shields.io/travis/com/santoshpanna/steamstorefront?style=flat-square
        :target: https://travis-ci.com/santoshpanna/SteamStoreFront

.. image:: https://img.shields.io/readthedocs/steamstorefront?style=flat-square
        :target: https://steamstorefront.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

Steam Store Front is an easy to use package to get game or app details from steam store.

.. note:: It is not a client. You cannot interact with steam to make purchase or do actions which requires login.*

* Free software: MIT license
* Documentation: https://steamstorefront.readthedocs.io

Features
********
- Supports apps
- Supports packages
- Supports bundles

Todo
****
- more details about app from other souces
- support for pages like developers, publishers, sales etc

Installation
************
.. code-block:: console

    pip install steamstorefront

Usage
*****
Constructor:

.. code-block:: python

    import steamstorefront
    
    ssf = steamstorefront.SteamStoreFront(appid=203160, category="app")

    ssf.getName()
    ssf.getPrice()

Function:

.. code-block:: python
    
    from steamstorefront import SteamStoreFront
    
    ssf = SteamStoreFront()

    ssf.getName(appid=203160, category="app")
    ssf.getPrice(appid=203160, category="app")

When quering data for same app:

.. code-block:: python

    from steamstorefront import SteamStoreFront
    
    ssf = SteamStoreFront()

    ssf.getName(appid=203160, category="app")
    # it stores the appid and category so no need to pass it twice
    ssf.getPrice()

When quering for different app:

.. code-block:: python

    from steamstorefront import SteamStoreFront
    
    ssf = SteamStoreFront()

    ssf.getName(appid=203160, category="app")
    ssf.getName(appid=730, category="app")

Credits
*******
 - `Cookiecutter <https://github.com/audreyr/cookiecutter>`_
