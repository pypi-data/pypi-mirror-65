import requests, w3lib.html, math


class App:
    api_url = "https://store.steampowered.com/api/appdetails?appids="
    data = {}
    appid = 0

    def _getNormal(self, text):
        text = text.replace("\"", "").replace("<img src=", "").replace(" >", "")
        return text.replace("<br><br>", "\n")

    def _getNormalLanguage(self, text):
        text = w3lib.html.remove_tags(text)
        return text.replace("*", "").replace("languages with full audio support", "")

    # makes a list from text
    # iterates until text is empty 
    # gets key, value from html patterns
    def _getListReview(self, text):
        reviews = []
        while text != "":
            review = {}
            review['review'] = text[:text.find("<br>")]
            text = text[text.find("<br>") + 4:]
            review['score'] = text[:text.find(" ")]
            text = text[text.find(" ") + 12:]
            review['link'] = text[:text.find("\"")].replace("https://steamcommunity.com/linkfilter/?url=", "")
            text = text[text.find(">") + 1:]
            review['reviewer'] = text[:text.find("<")]
            text = text[text.find("<br>") + 8:]
            reviews.append(review)
        return reviews

    # makes a dict from text
    # iterates until text is empty
    # gets key, value from html patterns
    def _getDict(self, text):
        dict = {}

        text = w3lib.html.remove_tags(text, keep=('strong',))

        while text != "":
            key = text[:text.find("</strong>") - 1].replace("<strong>", "")
            text = text[text.find("</strong>") + 9:]
            requirement = text[:text.find("<strong>")]
            dict[key] = requirement
            if text.find(">") == -1:
                dict[key] = text
                text = ""
            else:
                text = text[text.find(">") + 1:]

        return dict

    def _getDictionaryRequirements(self, list):
        dict = {}
        if 'minimum' in list:
            dict['minimum'] = self._getDict(list['minimum'])
        if 'recommended' in list:
            dict['recommended'] = self._getDict(list['recommended'])

        return dict

    '''
        DATA
        App ID:
            sucess
            data:
                type - ["game", "dlc", "demo", "advertising", "mod", "video"]
                name
                steam_appid
                required_age
                is_free
                controller_support (optional)
                dlc (optional)
                detailed_description
                about_the_game
                short_description
                fullgame (optional)
                supported_languages
                reviews
                header_image
                website
                pc_requirements
                mac_requirements
                linux_requirements
                legal_notice (optional)
                developers (optional)
                publishers
                demos (optional)
                price_overview (optional)
                packages
                package_group
                platforms
                metacritic (optional)
                categories (optional)
                genres (optional)
                screenshots (optional)
                movies (optional)
                recommendations (optional)
                achievements (optional)
                release_date
                support_info
                background
                content_desriptors
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
        if not self.data or appid != self.appid or str(self.data['steam_appid']) != appid:
            self.getRaw(appid)

    # returns name
    def getName(self, appid):
        self._populate(appid)
        return self.data['name'] if 'name' in self.data else None

    # returns required age
    def getRequiredAge(self, appid):
        self._populate(appid)
        return self.data['required_age'] if 'required_age' in self.data else None

    # returns is free
    def getIsFree(self, appid):
        self._populate(appid)
        return self.data['is_free'] if 'is_free' in self.data else None

    # returns controller support
    def getControllerSupport(self, appid):
        self._populate(appid)
        return self.data['controller_support'] if 'controller_support' in self.data else None

    # returns dlc
    def getDLC(self, appid):
        self._populate(appid)
        return self.data['dlc'] if 'dlc' in self.data else None

    # returns detailed description
    # format = raw (default) | normal
    def getDetailedDescription(self, appid, format: str = None):
        self._populate(appid)

        # if normal remove just html tags, retain images link
        if format.lower() == "normal":
            return self._getNormal(self.data['detailed_description']) if 'detailed_description' in self.data else None
        else:
            return self.data['detailed_description'] if 'detailed_description' in self.data else None

    # returns about the game
    # format = raw (default) | normal
    def getAboutTheGame(self, appid, format: str = None):
        self._populate(appid)
        # if normal remove just html tags, retain images link
        if format.lower() == "normal":
            return self._getNormal(self.data['about_the_game']) if 'about_the_game' in self.data else None
        else:
            return self.data['about_the_game'] if 'about_the_game' in self.data else None

    # returns short description
    def getShortDescription(self, appid):
        self._populate(appid)
        return self.data['short_description'] if 'short_description' in self.data else None

    # returns fullgame
    # IDK what this is
    def getFullgame(self, appid):
        self._populate(appid)
        return self.data['fullgame'] if 'fullgame' in self.data else None

    # returns supported languages
    # format = raw (default) | normal | list
    def getSupportedLanguages(self, appid, format: str = None):
        self._populate(appid)
        if format.lower() == "normal":
            return self._getNormalLanguage(
                self.data['supported_languages']) if 'supported_languages' in self.data else None
        elif format.lower() == "list":
            return self._getNormalLanguage(self.data['supported_languages']).split(
                ", ") if 'supported_languages' in self.data else None
        else:
            return self.data['supported_languages'] if 'supported_languages' in self.data else None

    # returns reviews
    # format = raw (default) | list
    '''
        list of dictinaries
        [
            {'review': '', 'score': '', 'link': '', 'reviewer'},
            {'review': '', 'score': '', 'link': '', 'reviewer'}
        ]
    '''

    def getReviews(self, appid, format: str = None):
        self._populate(appid)
        if format.lower() == "list":
            return self._getListReview(self.data['reviews']) if 'reviews' in self.data else None
        else:
            return self.data['reviews'] if 'reviews' in self.data else None

    # returns header image
    def getHeaderImage(self, appid):
        self._populate(appid)
        return self.data['header_image'] if 'header_image' in self.data else None

    # returns website
    def getWebsite(self, appid):
        self._populate(appid)
        return self.data['website'] if 'website' in self.data else None

    # returns pc requirements
    # format = raw (default) | dict
    def getPCRequirements(self, appid, format: str = None):
        self._populate(appid)
        if format.lower() == "dict":
            return self._getDictionaryRequirements(
                self.data['pc_requirements']) if 'pc_requirements' in self.data else None
        else:
            return self.data['pc_requirements'] if 'pc_requirements' in self.data else None

    # returns mac requirements
    # format = raw (default) | dict
    def getMacRequirements(self, appid, format: str = None):
        self._populate(appid)

        if format.lower() == "dict":
            return self._getDictionaryRequirements(
                self.data['mac_requirements']) if 'mac_requirements' in self.data else None
        else:
            return self.data['mac_requirements'] if 'mac_requirements' in self.data else None

    # returns linux requirements
    # format = raw (default) | dict
    def getLinuxRequirements(self, appid, format: str = None):
        self._populate(appid)
        if format.lower() == "dict":
            return self._getDictionaryRequirements(
                self.data['linux_requirements']) if 'linux_requirements' in self.data else None
        else:
            return self.data['linux_requirements'] if 'linux_requirements' in self.data else None

    # returns legal notice
    def getLegalNotice(self, appid):
        self._populate(appid)
        return self.data['legal_notice'] if 'legal_notice' in self.data else None

    # returns developers
    def getDevelopers(self, appid):
        self._populate(appid)
        return self.data['developers'] if 'developers' in self.data else None

    # returns publishers
    def getPublishers(self, appid):
        self._populate(appid)
        return self.data['publishers'] if 'publishers' in self.data else None

    # returns demos
    def getDemos(self, appid):
        self._populate(appid)
        return self.data['demos'] if 'demos' in self.data else None

    # returns price overview
    def getPriceOverview(self, appid):
        self._populate(appid)
        return self.data['price_overview'] if 'price_overview' in self.data else None

    # returns packages
    def getPackages(self, appid):
        self._populate(appid)
        return self.data['packages'] if 'packages' in self.data else None

    # returns package group
    def getPackageGroup(self, appid):
        self._populate(appid)
        return self.data['package_groups'] if 'package_groups' in self.data else None

    # returns platforms
    def getPlatforms(self, appid):
        self._populate(appid)
        return self.data['platforms'] if 'platforms' in self.data else None

    # returns metacritic score
    def getMetacritic(self, appid):
        self._populate(appid)
        return self.data['metacritic'] if 'metacritic' in self.data else None

    # returns categories
    def getCategories(self, appid):
        self._populate(appid)
        return self.data['categories'] if 'categories' in self.data else None

    # returns genres
    def getGenres(self, appid):
        self._populate(appid)
        return self.data['genres'] if 'genres' in self.data else None

    # returns screenshots
    def getScreenshots(self, appid):
        self._populate(appid)
        return self.data['screenshots'] if 'screenshots' in self.data else None

    # returns movies
    def getMovies(self, appid):
        self._populate(appid)
        return self.data['movies'] if 'movies' in self.data else None

    # returns recommendations
    def getRecommendations(self, appid):
        self._populate(appid)
        return self.data['recommendations'] if 'recommendations' in self.data else None

    # returns achievements
    def getAchievements(self, appid):
        self._populate(appid)
        return self.data['achievements'] if 'achievements' in self.data else None

    # returns release date
    def getReleaseDate(self, appid):
        self._populate(appid)
        return self.data['release_date'] if 'release_date' in self.data else None

        # returns release date

    def getSupportInfo(self, appid):
        self._populate(appid)
        return self.data['support_info'] if 'support_info' in self.data else None

        # returns release date

    def getBackground(self, appid):
        self._populate(appid)
        return self.data['background'] if 'background' in self.data else None

        # returns release date

    def getContentDescriptors(self, appid):
        self._populate(appid)
        return self.data['content_descriptors'] if 'content_descriptors' in self.data else None

        # returns ratings

    def getRatings(self, appid):
        req = requests.get("https://store.steampowered.com/appreviews/" + appid + "?json=1").json()

        if req["query_summary"]:
            # Review Score = frac{Positive Reviews}{Total Reviews}
            try:
                review_score = req["query_summary"]["total_positive"] / req["query_summary"]["total_reviews"]
                # Rating = Review Score - (Review Score - 0.5)*2^{-log_{10}(Total Reviews + 1)})
                rating = review_score - (review_score - 0.5) * (
                            2 ** (-1 * math.log10(req["query_summary"]["total_reviews"] + 1)))
                return review_score * 100, rating * 100, req["query_summary"]
            except:
                return 0, 0, req["query_summary"]
        else:
            return 0, 0, req["query_summary"]

    # returns price in specific currency
    def getPriceInCurrency(self, appid, currency):
        req = requests.get(self.api_url + appid + "&cc=" + currency + "&filters=price_overview").json()

        if req[appid]["data"]:
            return req[appid]["data"]["price_overview"]
        else:
            return None
