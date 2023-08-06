"""Functions and values, independent of other modules."""

import functools
import sys

# Lethargy provides its own argv so you don't have to import sys or worry
# about mutating the original.
argv = sys.argv.copy()


def stab(text):
    """Stab a string, with a skewer of appropriate length.

        >>> stab('x')
        '-x'
        >>> stab('xyz')
        '--xyz'
        >>> stab('abc xyz')
        '--abc-xyz'
        >>> stab('  lm no p ')
        '--lm-no-p'

    Unless the string starts with something that isn't a letter or number.

        >>> stab('  -x')
        '-x'
        >>> stab('/FLAG ')
        '/FLAG'
    """
    stripped = str(text).strip()

    # Assume it's been pre-formatted if it starts with something that's not
    # a letter or number.
    if not stripped[:1].isalnum():
        return stripped

    name = "-".join(stripped.split())

    chars = len(name)

    if chars > 1:
        return f"--{name}"
    if chars == 1:
        return f"-{name}"

    raise ValueError("Cannot stab an empty string.")


def is_greedy(value):
    """Return a boolean representing whether a given value is "greedy"."""
    return value is ...


def identity(a):
    """Get the same output as the input."""
    return a


def print_if(condition):
    """Return either ``print`` or a dummy function, depending on ``condition``."""
    return print if condition else lambda *__, **_: None


eprint = functools.partial(print, file=sys.stderr)
