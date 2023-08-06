#!/usr/bin/env python

"""Tests for `steamstorefront` package."""

import pytest

from click.testing import CliRunner

from steamstorefront import SteamStoreFront
from steamstorefront import cli

appid = 58375

@pytest.fixture
def app():
    data = SteamStoreFront()
    return data

# returns raw data
def testGetRaw(app):
    data = app.getRaw(appid=appid, category='package')
    assert data['name'] == "Lara Croft and the Temple of Osiris - Season Pass Only"

 # returns name
def testGetName(app):
    data = app.getName(appid=appid, category='package')
    test = (type(data) == type(str()) and data == "Lara Croft and the Temple of Osiris - Season Pass Only")
    assert test == True

# returns required age
def testGetPageImage(app):
    data = app.getPageImage(appid=appid, category='package')
    test = (type(data) == type(str()) and ".jpg" in data)
    assert test == True

# returns is free
def testGetHeaderImage(app):
    data = app.getHeaderImage(appid=appid, category='package')
    test = (type(data) == type(str()) and ".jpg" in data)
    assert test == True

# returns controller support
def testGetSmallLogo(app):
    data = app.getSmallLogo(appid=appid, category='package')
    test = (type(data) == type(str()) and ".jpg" in data)
    assert test == True

# returns dlc
def testGetApps(app):
    data = app.getApps(appid=appid, category='package')
    test = (type(data) == type(list()) and data[0]['id'] == 318874)
    assert test == True

# returns detailed description
def testGetPrice(app):
    data1 = app.getPrice(appid=appid, category='package')
    data2 = app.getPrice(appid=appid, category='package', currency='in')
    test1 = (type(data1) == type(dict()))
    test2 = (type(data2) == type(dict()))
    assert test1 == True
    assert test2 == True

# returns short description
def testGetPlatforms(app):
    data = app.getPlatforms(appid=appid, category='package')
    test = (type(data) == type(dict()) and data['mac'] == False)
    assert test == True

# returns fullgame
def testGetController(app):
    data = app.getControllerSupport(appid=appid, category='package')
    test = (type(data) == type(dict()) and data['full_gamepad'] == True)
    assert test == True

# returns header image
def testGetReleaseDate(app):
    data = app.getReleaseDate(appid=appid, category='package')
    test = (type(data) == type(dict()) and data['coming_soon'] == False)
    assert test == True