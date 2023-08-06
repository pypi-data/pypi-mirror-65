"""Declarative, dynamic option parsing."""

__version__ = "2.0.1"
__all__ = (
    "ArgsError",
    "MissingOption",
    "Opt",
    "OptionError",
    "argv",
    "eprint",
    "print_if",
    "take_debug",
    "take_verbose",
)

from lethargy.errors import ArgsError, MissingOption, OptionError
from lethargy.option import Opt
from lethargy.util import argv, eprint, print_if

# The following options are such a frequent usage of this library that it's
# reasonable to provide them automatically, and remove even more boilerplate.

take_debug = Opt("debug").take_flag
take_verbose = Opt("v", "verbose").take_flag
