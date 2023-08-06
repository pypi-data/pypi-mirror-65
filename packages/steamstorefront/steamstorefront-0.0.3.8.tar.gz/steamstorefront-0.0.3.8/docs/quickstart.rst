.. _quickstart:

Quickstart
==========
Arguments::

It supports 3 types of app detection

 - Appid

    `appid=203160`

 - Name

    `name="Tomb Raider"`

 - Url

     `url="https://store.steampowered.com/app/1085660/Destiny_2/"`

- If only appid is given

 - Category can be 

        `category="app"`

        `category="sub"`

        `category="package"`
 - Default category is `app`

- If name is given

 - The appid is extracted from `http://api.steampowered.com/ISteamApps/GetAppList/v0001/` with the best match with name

- If url is given

 - appid and category is extracted from url itself

See :ref:`functions` for functions and their purpose

Initializing from constructor
-----------------------------

.. code-block:: python

    import steamstorefront
    
    ssf = steamstorefront.SteamStoreFront(appid=203160, category="app")

    ssf.getName()
    ssf.getPrice()

Initializing from function
--------------------------

.. code-block:: python
    
    from steamstorefront import SteamStoreFront
    
    ssf = SteamStoreFront()

    ssf.getName(appid=203160, category="app")
    ssf.getPrice(appid=203160, category="app")

Quering data for same app
-------------------------

.. code-block:: python

    from steamstorefront import SteamStoreFront
    
    ssf = SteamStoreFront()

    ssf.getName(appid=203160, category="app")
    # it stores the appid and category so no need to pass it twice
    ssf.getPrice()

Quering for different app
-------------------------

.. code-block:: python

    from steamstorefront import SteamStoreFront
    
    ssf = SteamStoreFront()

    ssf.getName(appid=203160, category="app")
    ssf.getName(appid=730, category="app")