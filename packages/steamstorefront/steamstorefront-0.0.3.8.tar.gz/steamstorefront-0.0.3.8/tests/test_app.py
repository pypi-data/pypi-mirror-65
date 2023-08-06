#!/usr/bin/env python

"""Tests for `steamstorefront` package."""

import pytest

from click.testing import CliRunner

from steamstorefront import SteamStoreFront
from steamstorefront import cli

# Tomb Raider Reboot
appid = 203160

@pytest.fixture
def app():
    data = SteamStoreFront()
    return data


# returns raw data
def testGetRaw(app):
    data = app.getRaw(appid=appid, category='app')
    assert data['steam_appid'] == 203160

# returns name
def testGetName(app):
    assert app.getName(appid=appid, category='app') == "Tomb Raider"

# returns required age
def testGetRequiredAge(app):
    assert type(app.getRequiredAge(appid=appid, category='app')) == type(str())

# returns is free
def testGetIsFree(app):
    assert app.getIsFree(appid=appid, category='app') == False

# returns controller support
def testGetControllerSupport(app):
    assert app.getControllerSupport(appid=appid, category='app') == "full"

# returns dlc
def testGetDLC(app):
    data = app.getDLC(appid=appid, category='app')
    test = (type(data) == type(list()) and 208791 in data)
    assert test == True

# returns detailed description
# format = raw (default) | normal
def testGetDescription(app):
    assert type(app.getDescription(appid=appid, category='app', format='raw')) == type(str())
    assert type(app.getDescription(appid=appid, category='app', format='normal')) == type(str())

    assert type(app.getDescription(appid=appid, category='app', short=True, format='raw')) == type(str())
    assert type(app.getDescription(appid=appid, category='app', short=True, format='normal')) == type(str())

# returns about the game
# format = raw (default) | normal
def testGetAboutTheGame(app):
    assert type(app.getControllerSupport(appid=appid, category='app', format='raw')) == type(str())
    assert type(app.getControllerSupport(appid=appid, category='app', format='normal')) == type(str())

# returns fullgame
# IDK what this is
def testGetFullgame(app):
    assert app.getFullgame(appid=appid, category='app') == None

# returns supported languages
# format = raw (default) | normal | list
def testGetSupportedLanguages(app):
    data1 = app.getSupportedLanguages(appid=appid, category='app')
    data2 = app.getSupportedLanguages(appid=appid, category='app', format="normal")
    data3 = app.getSupportedLanguages(appid=appid, category='app', format="list")
    langtest1 = ("English" in data1 and type(str()) == type(data1) and "<strong>" in data1)
    langtest2 = ("English" in data2 and type(str()) == type(data2) and "<strong>" not in data2)
    langtest3 = ("English" in data3 and type(list()) == type(data3))

    assert langtest1 == True
    assert langtest2 == True
    assert langtest3 == True

# returns reviews
def testGetReviews(app):
    assert type(app.getReviews(appid=appid, category='app', format='raw')) == type(str())
    assert type(app.getReviews(appid=appid, category='app', format='list')) == type(list())

# returns header image
def testGetHeaderImage(app):
    test = ".jpg" in app.getHeaderImage(appid=appid, category='app')
    assert test == True

# returns website
def testGetWebsite(app):
    assert app.getWebsite(appid=appid, category='app') == "http://www.tombraider.com"

# returns pc requirements
# format = raw (default) | dict
def testGetPCRequirements(app):
    data1 = app.getPCRequirements(appid=appid, category='app', format='raw')
    data2 = app.getPCRequirements(appid=appid, category='app', format='dict')
    test1 = (data1["minimum"].startswith("<strong>") and type(data1["minimum"]) == type(str()))
    test2 = ("OS" in data2["minimum"] and type(data2["minimum"]) == type(dict()))
    assert test1 == True
    assert test2 == True

# returns mac requirements
# format = raw (default) | dict
def testGetMacRequirements(app):
    data1 = app.getMacRequirements(appid=appid, category='app', format='raw')
    data2 = app.getMacRequirements(appid=appid, category='app', format='dict')
    test1 = (data1["minimum"].startswith("<strong>") and type(data1["minimum"]) == type(str()))
    test2 = ("OS" in data2["minimum"] and type(data2["minimum"]) == type(dict()))
    assert test1 == True
    assert test2 == True

# returns linux requirements
# format = raw (default) | dict
def testGetLinuxRequirements(app):
    data1 = app.getLinuxRequirements(appid=appid, category='app', format='raw')
    data2 = app.getLinuxRequirements(appid=appid, category='app', format='dict')
    test1 = (data1["minimum"].startswith("<strong>") and type(data1["minimum"]) == type(str()))
    test2 = ("OS" in data2["minimum"] and type(data2["minimum"]) == type(dict()))
    assert test1 == True
    assert test2 == True

# returns legal notice
def testGetLegalNotice(app):
    assert type(app.getLegalNotice(appid=appid, category='app')) == type(str())

# returns developers
def testGetDevelopers(app):
    data = app.getDevelopers(appid=appid, category='app') 
    test1 = ("Crystal Dynamics" in data and type(data) == type(list()))
    assert test1 == True

# returns publishers
def testGetPublishers(app):
    data = app.getPublishers(appid=appid, category='app') 
    test1 = ("Square Enix" in data and type(data) == type(list()))
    assert test1 == True

# returns demos
def testGetDemos(app):
    assert app.getDemos(appid=appid, category='app') == None

# returns price overview
def testGetPrice(app):
    data1 = app.getPrice(appid=appid, category='app')
    data2 = app.getPrice(appid=appid, category='app', currency='in')
    test1 = (type(data1) == type(dict()) and type(data1["initial"]) == type(int()))
    test2 = (type(data2) == type(dict()) and data2["initial"] == 56500)
    assert test1 == True
    assert test2 == True

# returns packages
def testGetPackages(app):
    data = app.getPackages(appid=appid, category='app')
    test = (type(data) == type(list()) and 26016 in data)
    assert test == True

# returns package group
def testGetPackageGroup(app):
    data = app.getPackageGroup(appid=appid, category='app')
    test = (type(data) == type(list()) and data[0]["title"] == "Buy Tomb Raider")
    assert test == True

# returns platforms
def testGetPlatforms(app):
    data = app.getPlatforms(appid=appid, category='app')
    test = (type(data) == type(dict()) and data["windows"] == True)
    assert test == True

# returns metacritic score
def testGetMetacritic(app):
    data = app.getMetacritic(appid=appid, category='app')
    test = (type(data) == type(dict()) and type(data["score"]) == type(int()))
    assert test == True

# returns categories
def testGetCategories(app):
    data = app.getCategories(appid=appid, category='app')
    test = (type(data) == type(list()) and data[0]["id"] == 2)
    assert test == True

# returns genres
def testGetGenres(app):
    data = app.getGenres(appid=appid, category='app')
    test = (type(data) == type(list()) and data[0]["id"] == "1")
    assert test == True

# returns screenshots
def testGetScreenshots(app):
    data = app.getScreenshots(appid=appid, category='app')
    test = (type(data) == type(list()) and data[0]["id"] == 0)
    assert test == True

# returns movies
def testGetMovies(app):
    data = app.getMovies(appid=appid, category='app')
    test = (type(data) == type(list()))
    assert test == True

# returns recommendations
def testGetRecommendations(app):
    data = app.getRecommendations(appid=appid, category='app')
    test = (type(data) == type(dict()) and type(data["total"]) == type(int()))
    assert test == True

# returns achievements
def testGetAchievements(app):
    data = app.getAchievements(appid=appid, category='app')
    test = (type(data) == type(dict()) and data["total"] == 50)
    assert test == True

# returns release date
def testGetReleaseDate(app):
    data = app.getReleaseDate(appid=appid, category='app')
    test = (type(data) == type(dict()) and data["coming_soon"] == False)
    assert test == True

# returns ratings
def testGetRatings(app):
    data = app.getRatings(appid=appid, category='app')
    test = (type(data) == type(tuple()) and data[0] != 0)
    assert test == True

# returns release date
def testGetSupportInfo(app):
    data = app.getSupportInfo(appid=appid, category='app')
    test = (type(data) == type(dict()) and data["url"] == "http://support.na.square-enix.com/")
    assert test == True

# returns release date
def testGetBackground(app):
    data = app.getBackground(appid=appid, category='app')
    test = (type(data) == type(str()) and '.jpg' in data)
    assert test == True

# returns release date
def testGetContentDescriptors(app):
    data = app.getContentDescriptors(appid=appid, category='app')
    test = (type(data) == type(dict()) and type(data["ids"]) == type(list()))
    assert test == True

def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    assert 'steamstorefront.cli.main' in result.output
    help_result = runner.invoke(cli.main, ['--help'])
    assert help_result.exit_code == 0
    assert '--help  Show this message and exit.' in help_result.output