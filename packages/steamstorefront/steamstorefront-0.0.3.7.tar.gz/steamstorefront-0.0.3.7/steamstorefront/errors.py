import enum


class SteamStoreFront(Exception):
    pass


class Errors(enum.Enum):
    NoArgumentPassed = 0
    InvalidCategory = 1
    InvalidUrl = 2
    InvalidName = 3
    InvalidAppId = 4


class InvalidArgument(SteamStoreFront):
    def __init__(self, message, error, type_e):
        super().__init__(message)
        self.error = error
        self.type = type_e
