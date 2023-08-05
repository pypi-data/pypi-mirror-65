

class XivDbReader(Exception):
    """
    About:
        This is the base class for all XivDbReader errors.
    """
    pass

class UnableToReadWeaponType(XivDbReader):
    pass

class UnableToFindValue(XivDbReader):
    """
    About:
        Used when unable to find a value in an expected place.
        Report where the error happened to resolve the issue.
    """
    pass
