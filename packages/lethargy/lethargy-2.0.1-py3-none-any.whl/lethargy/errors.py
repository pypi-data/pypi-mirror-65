"""Module specifically to contain exception subclasses."""


class OptionError(Exception):
    """Superclass of ArgsError and MissingOption."""


class ArgsError(OptionError):
    """Too few arguments provided to an option."""


class MissingOption(OptionError):
    """Expecting an option, but unable to find it."""
