from fuzzywuzzy import process
import requests


class FuzzySearch:
    json = None
    indexed = None

    def _populate(self, name):
        if not self.json and not self.indexed:
            self.json = requests.get('http://api.steampowered.com/ISteamApps/GetAppList/v0001/').json()
        if not self.indexed:
            self.indexed = {idx: k["name"] for idx, k in enumerate(json["applist"]["apps"]["app"])}

    def getAppID(self, name):
        # populate it
        self._populate(name)

        # extract the one with best match
        tup = process.extractOne(name, dict)

        # return if found else return None
        if tup:
            return self.json["applist"]["apps"]["app"][a[2]]["appid"]
        else:
            return None
