import requests


class Package:
    api_url = "https://store.steampowered.com/api/packagedetails?packageids="
    data = {}
    appid = 0

    '''
        DATA
        App ID:
            sucess
            data:
                name
                page_image
                header_image (optional)
                small_logo
                apps
                price
                platforms
                controller
                release_date
    '''

    # returns raw data
    def getRaw(self, appid):
        # caching appid
        self.appid = appid

        # request the data
        json = requests.get(self.api_url + appid).json()

        # if game exists
        if json[appid]['success']:
            self.data = json[appid]['data']
            return self.data
        else:
            return None

    # populate internal data dictionary
    def _populate(self, appid):
        if not self.data or appid != self.appid or self.appid == 0:
            self.getRaw(appid)

    # returns name
    def getName(self, appid):
        self._populate(appid)
        return self.data['name'] if 'name' in self.data else None

    # returns required age
    def getPageImage(self, appid):
        self._populate(appid)
        return self.data['page_image'] if 'page_image' in self.data else None

    # returns is free
    def getHeaderImage(self, appid):
        self._populate(appid)
        return self.data['header_image'] if 'header_image' in self.data else None

    # returns controller support
    def getSmallLogo(self, appid):
        self._populate(appid)
        return self.data['small_logo'] if 'small_logo' in self.data else None

    # returns dlc
    def getApps(self, appid):
        self._populate(appid)
        return self.data['apps'] if 'apps' in self.data else None

    # returns detailed description
    def getPrice(self, appid):
        self._populate(appid)
        return self.data['price'] if 'price' in self.data else None

    # returns short description
    def getPlatforms(self, appid):
        self._populate(appid)
        return self.data['platforms'] if 'platforms' in self.data else None

    # returns fullgame
    def getController(self, appid):
        self._populate(appid)
        return self.data['controller'] if 'controller' in self.data else None

    # returns header image
    def getReleaseDate(self, appid):
        self._populate(appid)
        return self.data['release_date'] if 'release_date' in self.data else None

    # returns price in specific currency
    def getPriceInCurrency(self, appid, currency):
        req = requests.get(self.api_url + appid + "&cc=" + currency).json()

        if req[appid]["data"]:
            return req[appid]["data"]["price"]
        else:
            return None
