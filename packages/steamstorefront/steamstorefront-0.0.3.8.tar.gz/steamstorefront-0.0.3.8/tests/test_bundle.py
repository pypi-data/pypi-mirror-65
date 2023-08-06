#!/usr/bin/env python

"""Tests for `steamstorefront` package."""

import pytest

from click.testing import CliRunner

from steamstorefront import SteamStoreFront
from steamstorefront import cli

# Shadow of the Tomb Raider: Definitive Edition
appid = 12231

@pytest.fixture
def app():
    data = SteamStoreFront()
    return data

# returns raw data
def testGetRaw(app):
    data = app.getRaw(appid=appid, category='bundle')
    assert data['bundle_id'] == str(appid)

# returns name
def testGetName(app):
    data = app.getName(appid=appid, category='bundle')
    test = (data == "Shadow of the Tomb Raider: Definitive Edition")
    assert test == True

# returns header image
def testGetHeaderImage(app):
    data = app.getHeaderImage(appid=appid, category='bundle')
    test = (".jpg" in data)
    assert test == True

# returns bundle description
def testGetBundleDescription(app):
    data = app.getDescription(appid=appid, category='bundle')
    test = (type(data) == type(str()))
    assert test == True

# returns genre
def testGetGenres(app):
    data = app.getGenres(appid=appid, category='bundle')
    test = (type(data) == type(list()) and "Action" in data)
    assert test == True

# returns developer
def testGetDevelopers(app):
    data = app.getDevelopers(appid=appid, category='bundle')
    test = (type(data) == type(list()) and "Crystal Dynamics" in data)
    assert test == True

# returns publisher
def testGetPublishers(app):
    data = app.getPublishers(appid=appid, category='bundle')
    test = (type(data) == type(list()) and "Square Enix" in data)
    assert test == True

# returns franchise
def testGetFranchise(app):
    data = app.getFranchise(appid=appid, category='bundle')
    test = (type(data) == type(list()) and "Tomb Raider" in data)
    assert test == True

# returns languages
def testGetLanguages(app):
    data = app.getSupportedLanguages(appid=appid, category='bundle')
    test = (type(data) == type(list()) and "English" in data)
    assert test == True

# returns drm
def testGetDRM(app):
    data = app.getDRM(appid=appid, category='bundle')
    test = (type(data) == type(str()))
    assert test == True

# returns categories
def testGetCategories(app):
    data = app.getCategories(appid=appid, category='bundle')
    test = (type(data) == type(list()) and data[0][2] == "Single-player")
    assert test == True

# returns price
def testGetPrice(app):
    data = app.getPrice(appid=appid, category='bundle')
    test = (type(data) == type(dict()))
    assert test == True

# returns package items
def testGetPackageItem(app):
    data = app.getPackageItem(appid=appid, category='bundle')
    test = (type(data) == type(list()) and data[0]['name'] == "Shadow of the Tomb Raider - Deluxe Extras")
    assert test == True