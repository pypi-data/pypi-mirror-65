"""Main module."""
from .errors import InvalidArgument
from .errors import Errors
from .misc import FuzzySearch
from .app import App
from .package import Package
from .bundle import Bundle


class SteamStoreFront:
    """
    :param appid: application id
    :param category: application category
    :param name: application name
    :param url: store url
    :type appid: integer or numeric string
    :type category: string
    :type name: string
    :type url: string

    .. note::

        one of the 3 parameters is required

        - appid
        - name
        - url

        category defaults to "app"

    :raise InvalidArgument: See error message for explanation. Additionally error can be looked up for argument and type for error code.

    :rtype: None if key not found.
    """

    appid = None
    category = "app"
    publisher = None
    app = None
    bundle = None
    package = None
    Errors = Errors

    # populate
    def _populate(self, **kwargs):
        # check if arguments were passed
        if kwargs:
            # check which arguments were passed
            # check if appid was passed
            if "appid" in kwargs:
                # check if appid is int
                if isinstance(kwargs["appid"], int):
                    self.appid = str(kwargs["appid"])

                # check if appid is numeric string
                elif isinstance(kwargs["appid"], str) and kwargs["appid"].isnumeric():
                    self.appid = kwargs["appid"]

                # appid is not integer, throw error
                else:
                    raise InvalidArgument("Appid must be integer or numeric string.", kwargs, Errors.InvalidAppId)

                # appid is valid, now assign category
                # default category is app
                if self.appid:
                    self.category = 'app'

                    # valid categories
                    accepted = ('sub', 'package', 'app', 'bundle')

                    # check if passed category is valid
                    if "category" in kwargs:
                        if kwargs["category"] in accepted:
                            self.category = kwargs["category"]
                        else:
                            raise InvalidArgument("Invalid category, {}.".format(kwargs['category']), kwargs, Errors.InvalidCategory)

            # name was passed
            if "name" in kwargs:
                # query for appid
                obj = FuzzySearch()
                self.appid = obj.getAppID(kwargs["name"])
                self.category = 'app'
                if not self.appid:
                    raise InvalidArgument("App not found for this game {}".format(kwargs['name']), kwargs, Errors.InvalidName)

            # url was passed
            if "url" in kwargs:
                url = ''

                # check if url is valid
                valid = ('https://store.steampowered.com', 'store.steampowered.com')
                if kwargs["url"].startswith(valid):
                    if kwargs["url"].startswith(valid[1]):
                        url = "https://" + kwargs["url"]
                    else:
                        url = kwargs["url"]

                    # if url is valid get category and appid
                    self.category = kwargs["url"].split("/")[3]
                    if self.category == "publisher":
                        self.publisher = kwargs["url"].split("/")[4]
                    else:
                        self.appid = kwargs["url"].split("/")[4]

        if "init" not in kwargs:
            # no arugments were passed or details are not filled
            if not self.appid:
                raise InvalidArgument("No identifier was passed, atleast one of appid, url, name is required.", kwargs, Errors.NoArgumentPassed)

        else:
            self.app = App()
            self.bundle = Bundle()
            self.package = Package()

    def __init__(self, **kwargs):
        # populate
        kwargs["init"] = True
        self._populate(**kwargs)
        app = App()
        bundle = Bundle()
        package = Package()

    def getRaw(self, **kwargs):
        """
            getRaw(appid=appid, category=category, name=name, url=url)

            .. code-block:: python

                getRaw(appid=appid, category=category, name=name, url=url)

            - supported categories = [app, sub, bundle]            

            :return: returns raw json data
            :rtype: dictionary
        """

        # store data
        self._populate(**kwargs)

        # get data for app
        if self.category == "app":
            return self.app.getRaw(self.appid)

        # get data for packages
        elif self.category == "sub" or self.category == "package":
            return self.package.getRaw(self.appid)

        # get data for bundles
        elif self.category == "bundle":
            return self.bundle.getRaw(self.appid)

        else:
            raise InvalidArgument("No app with {} appid.".format(self.appid), kwargs, Errors.InvalidAppId)

    # returns store url
    def getLink(self, **kwargs):
        """
            getLink(appid=appid, category=category, name=name, url=url)

            .. code-block:: python
                getLink(appid=appid, category=category, name=name, url=url)
            
            - supported categories = [app, sub, bundle]
            
            :return: returns store url
            :rtype: string
        """

        if self.category == 'app':
            return 'https://store.steampowered.com/app/' + self.appid
        elif self.category == 'sub' or self.category == 'package':
            return 'https://store.steampowered.com/sub/' + self.appid
        elif self.category == 'bundle':
            return 'https://store.steampowered.com/bundle/' + self.appid

    # function to return price
    # currency only works with app and sub|package
    def getPrice(self, **kwargs):
        """
            getPrice(appid=appid, category=category, name=name, url=url, currency=currency)

            .. code-block:: python

                getPrice(appid=appid, category=category, name=name, url=url, currency=currency)
            
            - supported categories = [app, sub, bundle]
            - supported categories with currency = [app, sub]
            - currency should be in 2 letters, eg:- USD : us, INR : in, etc
            
            :return: returns price
            :rtype: dictionary
        """

        # store data
        self._populate(**kwargs)

        # get data for app
        if self.category == "app":
            if "currency" in kwargs:
                return self.app.getPriceInCurrency(self.appid, kwargs["currency"])
            return self.app.getPriceOverview(self.appid)

        # get data for packages
        elif self.category == "sub" or self.category == "package":
            if "currency" in kwargs:
                return self.package.getPriceInCurrency(self.appid, kwargs["currency"])
            return self.package.getPrice(self.appid)

        # get data for bundles
        elif self.category == "bundle":
            return self.bundle.getPrice(self.appid)

    # returns name
    def getName(self, **kwargs):
        """
            getName(appid=appid, category=category, name=name, url=url)

            .. code-block:: python

                getName(appid=appid, category=category, name=name, url=url)
            
            - supported categories = [app, sub, bundle]
            
            :return: returns name
            :rtype: str
        """

        # store data
        self._populate(**kwargs)

        # get data for app
        if self.category == "app":
            return self.app.getName(self.appid)

        # get data for packages
        elif self.category == "sub" or self.category == "package":
            return self.package.getName(self.appid)

        # get data for bundles
        elif self.category == "bundle":
            return self.bundle.getName(self.appid)

    # returns required age
    def getRequiredAge(self, **kwargs):
        """
            getRequiredAge(appid=appid, category=category, name=name, url=url)

            .. code-block:: python

                getRequiredAge(appid=appid, category=category, name=name, url=url)
            
            - supported categories = [app]
            
            :return: returns required age
            :rtype: int
        """

        # store data
        self._populate(**kwargs)

        # get data for app
        if self.category == "app":
            return self.app.getRequiredAge(self.appid)

        else:
            return None

    # returns is free
    def getIsFree(self, **kwargs):
        """
            getIsFree(appid=appid, category=category, name=name, url=url)

            .. code-block:: python

                getIsFree(appid=appid, category=category, name=name, url=url)
            
            - supported categories = [app]
            
            :return: returns is game free
            :rtype: boolean
        """

        # store data
        self._populate(**kwargs)

        # get data for app
        if self.category == "app":
            return self.app.getIsFree(self.appid)

        # get data for bundles
        else:
            return None

    # returns controller support
    def getControllerSupport(self, **kwargs):
        """
            getControllerSupport(appid=appid, category=category, name=name, url=url)

            .. code-block:: python

                getControllerSupport(appid=appid, category=category, name=name, url=url)
            
            - supported categories = [app, sub]
            
            :return: returns controller support
            :rtype: str
        """

        # store data
        self._populate(**kwargs)

        # get data for app
        if self.category == "app":
            return self.app.getControllerSupport(self.appid)

        # get data for packages
        elif self.category == "sub" or self.category == "package":
            return self.package.getController(self.appid)

        else:
            return None

    # returns dlc
    def getDLC(self, **kwargs):
        """
            getDLC(appid=appid, category=category, name=name, url=url)

            .. code-block:: python

                getDLC(appid=appid, category=category, name=name, url=url)
            
            - supported categories = [app]
            
            :return: returns dlc list
            :rtype: list
        """

        # store data
        self._populate(**kwargs)

        # get data for app
        if self.category == "app":
            return self.app.getDLC(self.appid)

        else:
            return None

    # returns detailed description
    # format = raw (default) | normal
    def getDescription(self, **kwargs):
        """
            getDescription(appid=appid, category=category, name=name, url=url, format=format)

            .. code-block:: python

                getDescription(appid=appid, category=category, name=name, url=url, format=format)
            
            - supported categories = [app, bundle]
            - supported categories with format = [app]
            - supported format = [raw(default), normal]

            - normal removes all html tags
            
            :return: returns description
            :rtype: str
        """

        # store data
        self._populate(**kwargs)

        # get data for app
        if self.category == "app":
            if "short" in kwargs:
                return self.app.getShortDescription(self.appid)
            if "format" in kwargs:
                return self.app.getDetailedDescription(self.appid, kwargs["format"])
            return self.app.getDetailedDescription(self.appid, "raw")

        # get data for bundles
        elif self.category == "bundle":
            return self.bundle.getBundleDescription(self.appid)

        else:
            return None

    # returns about the game
    # format = raw (default) | normal
    def getAboutTheGame(self, **kwargs):
        """
            getAboutTheGame(appid=appid, category=category, name=name, url=url, format=format)

            .. code-block:: python

                getAboutTheGame(appid=appid, category=category, name=name, url=url, format=format)
            
            - supported categories = [app]
            - supported categories with format = [app]
            - supported format = [raw(default), normal]

            - normal removes all html tags
            
            :return: returns about the game
            :rtype: str
        """

        # store data
        self._populate(**kwargs)

        # get data for app
        if self.category == "app":
            if "format" in kwargs:
                return self.app.getAboutTheGame(self.appid, kwargs["format"])
            return self.app.getAboutTheGame(self.appid, "raw")

        else:
            return None

    # returns short description
    def getShortDescription(self, **kwargs):
        """
            getShortDescription(appid=appid, category=category, name=name, url=url)

            .. code-block:: python

                getShortDescription(appid=appid, category=category, name=name, url=url)
            
            - supported categories = [app]
            
            :return: returns short description
            :rtype: str
        """

        # store data
        self._populate(**kwargs)

        # get data for app
        if self.category == "app":
            return self.app.getShortDescription(self.appid)

        else:
            return None

    # returns fullgame
    # IDK what this is
    def getFullgame(self, **kwargs):
        """
            getFullgame(appid=appid, category=category, name=name, url=url)

            .. code-block:: python

                getFullgame(appid=appid, category=category, name=name, url=url)
            
            - supported categories = [app]
            
            :return: returns ?
            :rtype: ?
        """

        # store data
        self._populate(**kwargs)

        # get data for app
        if self.category == "app":
            return self.app.getFullgame(self.appid)

        else:
            return None

    # returns supported languages
    # format = raw (default) | normal | list
    # format is only for app category
    def getSupportedLanguages(self, **kwargs):
        """
            getSupportedLanguages(appid=appid, category=category, name=name, url=url, format=format)

            .. code-block:: python

                getSupportedLanguages(appid=appid, category=category, name=name, url=url, format=format)
            
            - supported categories = [app, bundle]
            - supported categories with format = [app]
            - supported format = [raw(default), normal, list]

            - normal removes all html tags
            - list returns a list
            
            :return: returns supported language
            :rtype: str or list
        """

        # store data
        self._populate(**kwargs)

        # get data for app
        if self.category == "app":
            if "format" in kwargs:
                return self.app.getSupportedLanguages(self.appid, kwargs["format"])
            else:
                return self.app.getSupportedLanguages(self.appid, "raw")

        # get data for bundles
        elif self.category == "bundle":
            return self.bundle.getLanguages(self.appid)

        else:
            return None

    # returns reviews
    # format = raw (default) | list
    '''
        list of dictinaries
        [
            {'review': '', 'score': '', 'link': '', 'reviewer'},
            {'review': '', 'score': '', 'link': '', 'reviewer'}
        ]
    '''

    def getReviews(self, **kwargs):
        """
            getReviews(appid=appid, category=category, name=name, url=url, format=format)

            .. code-block:: python

                getReviews(appid=appid, category=category, name=name, url=url, format=format)
            
            - supported categories = [app]
            - supported categories with format = [app]
            - supported format = [raw(default), list]
            
            :return: returns reviews
            :rtype: str or list
        """

        # store data
        self._populate(**kwargs)

        # get data for app
        if self.category == "app":
            if "format" in kwargs:
                return self.app.getReviews(self.appid, kwargs["format"])
            else:
                return self.app.getReviews(self.appid, "raw")

        else:
            return None

    # returns header image
    def getHeaderImage(self, **kwargs):
        """
            getHeaderImage(appid=appid, category=category, name=name, url=url)

            .. code-block:: python

                getHeaderImage(appid=appid, category=category, name=name, url=url)
            
            - supported categories = [app, sub, bundle]
            
            :return: returns header image
            :rtype: str
        """

        # store data
        self._populate(**kwargs)

        # get data for app
        if self.category == "app":
            return self.app.getHeaderImage(self.appid)

        # get data for packages
        elif self.category == "sub" or self.category == "package":
            return self.package.getHeaderImage(self.appid)

        # get data for bundles
        elif self.category == "bundle":
            return self.bundle.getHeaderImage(self.appid)

        else:
            return None

    # returns website
    def getWebsite(self, **kwargs):
        """
            getWebsite(appid=appid, category=category, name=name, url=url)

            .. code-block:: python

                getWebsite(appid=appid, category=category, name=name, url=url)
            
            - supported categories = [app]
            
            :return: returns 
            :rtype: 
        """

        # store data
        self._populate(**kwargs)

        # get data for app
        if self.category == "app":
            return self.app.getWebsite(self.appid)

        else:
            return None

    # returns pc requirements
    # format = raw (default) | dict
    def getPCRequirements(self, **kwargs):
        """
            getPCRequirements(appid=appid, category=category, name=name, url=url, format=format)

            .. code-block:: python

                getPCRequirements(appid=appid, category=category, name=name, url=url, format=format)
            
            - supported categories = [app]
            - supported categories with format = [app]
            - supported format = [raw(default), dict]
            
            :return: returns pc requirements
            :rtype: str or dict
        """

        # store data
        self._populate(**kwargs)

        # get data for app
        if self.category == "app":
            if "format" in kwargs:
                return self.app.getPCRequirements(self.appid, kwargs["format"])
            else:
                return self.app.getPCRequirements(self.appid, "raw", "raw")
        else:
            return None

    # returns mac requirements
    # format = raw (default) | dict
    def getMacRequirements(self, **kwargs):
        """
            getMacRequirements(appid=appid, category=category, name=name, url=url, format=format)

            .. code-block:: python

                getMacRequirements(appid=appid, category=category, name=name, url=url, format=format)
            
            - supported categories = [app]
            - supported categories with format = [app]
            - supported format = [raw(default), dict]
            
            :return: returns mac requirements
            :rtype: str or dict
        """

        # store data
        self._populate(**kwargs)

        # get data for app
        if self.category == "app":
            if "format" in kwargs:
                return self.app.getMacRequirements(self.appid, kwargs["format"])
            else:
                return self.app.getMacRequirements(self.appid, "raw")
        else:
            return None

    # returns linux requirements
    # format = raw (default) | dict
    def getLinuxRequirements(self, **kwargs):
        """
            getLinuxRequirements(appid=appid, category=category, name=name, url=url, format=format)

            .. code-block:: python

                getLinuxRequirements(appid=appid, category=category, name=name, url=url, format=format)
            
            - supported categories = [app]
            - supported categories with format = [app]
            - supported format = [raw(default), dict]
            
            :return: returns linux requirements
            :rtype: str or dict
        """

        # store data
        self._populate(**kwargs)

        # get data for app
        if self.category == "app":
            if "format" in kwargs:
                return self.app.getMacRequirements(self.appid, kwargs["format"])
            else:
                return self.app.getMacRequirements(self.appid, "raw")
        else:
            return None

    # returns legal notice
    def getLegalNotice(self, **kwargs):
        """
            getLegalNotice(appid=appid, category=category, name=name, url=url)

            .. code-block:: python

                getLegalNotice(appid=appid, category=category, name=name, url=url)
            
            - supported categories = [app]
            
            :return: returns legal notice
            :rtype: str
        """

        # store data
        self._populate(**kwargs)

        # get data for app
        if self.category == "app":
            return self.app.getLegalNotice(self.appid)

        else:
            return None

    # returns developers
    def getDevelopers(self, **kwargs):
        """
            getDevelopers(appid=appid, category=category, name=name, url=url)

            .. code-block:: python

                getDevelopers(appid=appid, category=category, name=name, url=url)
            
            - supported categories = [app, bundle]
            
            :return: returns developers
            :rtype: list
        """

        # store data
        self._populate(**kwargs)

        # get data for app
        if self.category == "app":
            return self.app.getDevelopers(self.appid)

        # get data for bundles
        elif self.category == "bundle":
            return self.bundle.getDevelopers(self.appid)

        else:
            return None

    # returns publishers
    def getPublishers(self, **kwargs):
        """
            getPublishers(appid=appid, category=category, name=name, url=url)

            .. code-block:: python

                getPublishers(appid=appid, category=category, name=name, url=url)
            
            - supported categories = [app, bundle]
            
            :return: returns publishers
            :rtype: list
        """

        # store data
        self._populate(**kwargs)

        # get data for app
        if self.category == "app":
            return self.app.getPublishers(self.appid)

        # get data for bundles
        elif self.category == "bundle":
            return self.bundle.getPublishers(self.appid)

        else:
            return None

    # returns demos
    def getDemos(self, **kwargs):
        """
            getDemos(appid=appid, category=category, name=name, url=url)

            .. code-block:: python

                getDemos(appid=appid, category=category, name=name, url=url)
            
            - supported categories = [app]
            
            :return: returns demos
            :rtype: ?
        """

        # store data
        self._populate(**kwargs)

        # get data for app
        if self.category == "app":
            return self.app.getDemos(self.appid)

        else:
            return None

    # returns packages
    def getPackages(self, **kwargs):
        """
            getPackages(appid=appid, category=category, name=name, url=url)

            .. code-block:: python

                getPackages(appid=appid, category=category, name=name, url=url)
            
            - supported categories = [app]
            
            :return: returns packages
            :rtype: list
        """

        # store data
        self._populate(**kwargs)

        # get data for app
        if self.category == "app":
            return self.app.getPackages(self.appid)

        else:
            return None

    # returns package group
    def getPackageGroup(self, **kwargs):
        """
            getPackageGroup(appid=appid, category=category, name=name, url=url)

            .. code-block:: python

                getPackageGroup(appid=appid, category=category, name=name, url=url)
            
            - supported categories = [app]
            
            :return: returns package groups
            :rtype: list
        """

        # store data
        self._populate(**kwargs)

        # get data for app
        if self.category == "app":
            return self.app.getPackageGroup(self.appid)

        else:
            return None

    # returns platforms
    def getPlatforms(self, **kwargs):
        """
            getPlatforms(appid=appid, category=category, name=name, url=url)

            .. code-block:: python

                getPlatforms(appid=appid, category=category, name=name, url=url)
            
            - supported categories = [app, sub]
            
            :return: returns platforms
            :rtype: dict
        """

        # store data
        self._populate(**kwargs)

        # get data for app
        if self.category == "app":
            return self.app.getPlatforms(self.appid)

        # get data for packages
        elif self.category == "sub" or self.category == "package":
            return self.package.getPlatforms(self.appid)

        else:
            return None

    # returns metacritic score
    def getMetacritic(self, **kwargs):
        """
            getMetacritic(appid=appid, category=category, name=name, url=url)

            .. code-block:: python

                getMetacritic(appid=appid, category=category, name=name, url=url)
            
            - supported categories = [app]
            
            :return: returns metacritc score
            :rtype: dict
        """

        # store data
        self._populate(**kwargs)

        # get data for app
        if self.category == "app":
            return self.app.getMetacritic(self.appid)

        else:
            return None

    # returns categories
    def getCategories(self, **kwargs):
        """
            getCategories(appid=appid, category=category, name=name, url=url)

            .. code-block:: python

                getCategories(appid=appid, category=category, name=name, url=url)
            
            - supported categories = [app, bundle]
            
            :return: returns categories
            :rtype: list
        """

        # store data
        self._populate(**kwargs)

        # get data for app
        if self.category == "app":
            return self.app.getCategories(self.appid)

        # get data for bundles
        elif self.category == "bundle":
            return self.bundle.getCategories(self.appid)

        else:
            return None

    # returns genres
    def getGenres(self, **kwargs):
        """
            getGenres(appid=appid, category=category, name=name, url=url)

            .. code-block:: python

                getGenres(appid=appid, category=category, name=name, url=url)
            
            - supported categories = [app, bundle]
            
            :return: returns genres
            :rtype: list
        """

        # store data
        self._populate(**kwargs)

        # get data for app
        if self.category == "app":
            return self.app.getGenres(self.appid)

        # get data for bundles
        elif self.category == "bundle":
            return self.bundle.getGenres(self.appid)

        else:
            return None

    # returns screenshots
    def getScreenshots(self, **kwargs):
        """
            getScreenshots(appid=appid, category=category, name=name, url=url)

            .. code-block:: python

                getScreenshots(appid=appid, category=category, name=name, url=url)
            
            - supported categories = [app]
            
            :return: returns screenshots
            :rtype: list
        """

        # store data
        self._populate(**kwargs)

        # get data for app
        if self.category == "app":
            return self.app.getScreenshots(self.appid)

        else:
            return None

    # returns movies
    def getMovies(self, **kwargs):
        """
            getMovies(appid=appid, category=category, name=name, url=url)

            .. code-block:: python

                getMovies(appid=appid, category=category, name=name, url=url)
            
            - supported categories = [app]
            
            :return: returns movies
            :rtype: list
        """

        # store data
        self._populate(**kwargs)

        # get data for app
        if self.category == "app":
            return self.app.getMovies(self.appid)

        else:
            return None

    # returns recommendations
    def getRecommendations(self, **kwargs):
        """
            getRecommendations(appid=appid, category=category, name=name, url=url)

            .. code-block:: python

                getRecommendations(appid=appid, category=category, name=name, url=url)
            
            - supported categories = [app]
            
            :return: returns recommendations
            :rtype: dict
        """

        # store data
        self._populate(**kwargs)

        # get data for app
        if self.category == "app":
            return self.app.getRecommendations(self.appid)

        else:
            return None

    # returns achievements
    def getAchievements(self, **kwargs):
        """
            getAchievements(appid=appid, category=category, name=name, url=url)

            .. code-block:: python

                getAchievements(appid=appid, category=category, name=name, url=url)
            
            - supported categories = [app]
            
            :return: returns achievements list
            :rtype: list
        """

        # store data
        self._populate(**kwargs)

        # get data for app
        if self.category == "app":
            return self.app.getAchievements(self.appid)

        else:
            return None

    # returns release date
    def getReleaseDate(self, **kwargs):
        """
            getReleaseDate(appid=appid, category=category, name=name, url=url)

            .. code-block:: python

                getReleaseDate(appid=appid, category=category, name=name, url=url)
            
            - supported categories = [app, sub]
            
            :return: returns release date
            :rtype: dict
        """

        # store data
        self._populate(**kwargs)

        # get data for app
        if self.category == "app":
            return self.app.getReleaseDate(self.appid)

        # get data for packages
        elif self.category == "sub" or self.category == "package":
            return self.package.getReleaseDate(self.appid)

        else:
            return None

            # returns ratings

    def getRatings(self, **kwargs):
        """
            getRatings(appid=appid, category=category, name=name, url=url)

            .. code-block:: python

                getRatings(appid=appid, category=category, name=name, url=url)
            
            - supported categories = [app]
            
            :return: returns (review_score, rating, review_summary)
            :rtype: tuple
        """

        # store data
        self._populate(**kwargs)

        # get data for app
        if self.category == "app":
            return self.app.getRatings(self.appid)

        else:
            return None

    # returns release date
    def getSupportInfo(self, **kwargs):
        """
            getSupportInfo(appid=appid, category=category, name=name, url=url)

            .. code-block:: python

                getSupportInfo(appid=appid, category=category, name=name, url=url)
            
            - supported categories = [app]
            
            :return: returns suport info
            :rtype: dict
        """

        # store data
        self._populate(**kwargs)

        # get data for app
        if self.category == "app":
            return self.app.getSupportInfo(self.appid)

        else:
            return None

    # returns release date
    def getBackground(self, **kwargs):
        """
            getBackground(appid=appid, category=category, name=name, url=url)

            .. code-block:: python

                getBackground(appid=appid, category=category, name=name, url=url)
            
            - supported categories = [app]
            
            :return: returns background image
            :rtype: str
        """

        # store data
        self._populate(**kwargs)

        # get data for app
        if self.category == "app":
            return self.app.getBackground(self.appid)

        else:
            return None

    # returns release date
    def getContentDescriptors(self, **kwargs):
        """
            getContentDescriptors(appid=appid, category=category, name=name, url=url)

            .. code-block:: python

                getContentDescriptors(appid=appid, category=category, name=name, url=url)
            
            - supported categories = [app]
            
            :return: returns content descriptors
            :rtype: dict
        """

        # store data
        self._populate(**kwargs)

        # get data for app
        if self.category == "app":
            return self.app.getContentDescriptors(self.appid)

        else:
            return None

    '''
        Bundle only functions
    '''

    # returns franchise
    def getFranchise(self, **kwargs):
        """
            getFranchise(appid=appid, category=category, name=name, url=url)

            .. code-block:: python

                getFranchise(appid=appid, category=category, name=name, url=url)
            
            - supported categories = [bundle]
            
            :return: returns franchise
            :rtype: list
        """

        # store data
        self._populate(**kwargs)

        if self.category == "bundle":
            return self.bundle.getFranchise(self.appid)

        else:
            return None

    # returns drm
    def getDRM(self, **kwargs):
        """
            getDRM(appid=appid, category=category, name=name, url=url)

            .. code-block:: python

                getDRM(appid=appid, category=category, name=name, url=url)
            
            - supported categories = [bundle]
            
            :return: returns drm
            :rtype: list
        """

        # store data
        self._populate(**kwargs)

        if self.category == "bundle":
            return self.bundle.getDRM(self.appid)

        else:
            return None

    # returns package items
    def getPackageItem(self, **kwargs):
        """
            getPackageItem(appid=appid, category=category, name=name, url=url)

            .. code-block:: python

                getPackageItem(appid=appid, category=category, name=name, url=url)
            
            - supported categories = [bundle]
            
            :return: returns package item (apps and packages)
            :rtype: list
        """

        # store data
        self._populate(**kwargs)

        if self.category == "bundle":
            return self.bundle.getPackageItem(self.appid)

        else:
            return None

    '''
        Package only functions
    '''

    # returns required age
    def getPageImage(self, **kwargs):
        """
            getPageImage(appid=appid, category=category, name=name, url=url)

            .. code-block:: python

                getPageImage(appid=appid, category=category, name=name, url=url)
            
            - supported categories = [sub]
            
            :return: returns page image
            :rtype: str
        """

        # store data
        self._populate(**kwargs)

        if self.category == "sub" or self.category == "package":
            return self.package.getPageImage(self.appid)

        else:
            return None

    # returns small logo
    def getSmallLogo(self, **kwargs):
        """
            getSmallLogo(appid=appid, category=category, name=name, url=url)

            .. code-block:: python

                getSmallLogo(appid=appid, category=category, name=name, url=url)
            
            - supported categories = [sub]
            
            :return: returns small logo
            :rtype: str
        """

        # store data
        self._populate(**kwargs)

        if self.category == "sub" or self.category == "package":
            return self.package.getSmallLogo(self.appid)

        else:
            return None

    # returns apps
    def getApps(self, **kwargs):
        """
            getApps(appid=appid, category=category, name=name, url=url)

            .. code-block:: python

                getApps(appid=appid, category=category, name=name, url=url)
            
            - supported categories = [sub]
            
            :return: returns apps
            :rtype: list
        """

        # store data
        self._populate(**kwargs)

        if self.category == "sub" or self.category == "package":
            return self.package.getApps(self.appid)

        else:
            return None
