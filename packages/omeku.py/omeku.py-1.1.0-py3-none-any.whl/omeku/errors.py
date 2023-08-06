class OmekuException(Exception):
    """ Base exception class for omeku.py """

    pass


class NothingFound(OmekuException):
    """ The API didn't return anything """

    pass


class EmptyArgument(OmekuException):
    """ When no target is defined """

    pass


class InvalidArgument(OmekuException):
    """ Invalid argument within the category """

    pass
