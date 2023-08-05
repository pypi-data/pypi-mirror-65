"""
Functions for working with configuration file selection and reading.

The :func:`which` convenience function returns the first file that should be used as configuration file from a list.
"""

import os

from boltons.iterutils import first

__all__ = [
    "which",
]


def which(cfgfile=None, candidates=None, default="/dev/null", verify=os.path.exists):
    """
    Convenience function to return the configuration file to read.

    Parameters
    ----------
    cfgfile: str, None
        a single path. If not None, then it will be returned without calling the verify function.

    candidates: list[str], None
        a list of paths. If cfgfile is None, then the verify function will be
        called for each of these paths and the first one for which verify
        returns True will be returned.

        If no file is matched, then :file:`/dev/null` will be returned. 

    verify: callable
        callable that will be called for every file in candidate. Defaults to os.path.exists.

    default: str
        value to be returned if cfgfile is None and no match from candidates was found

    Returns
    -------
    str:
        cfgfile, a value from candidates, or default

    Example
    -------

    .. code-block:: python

        import argparse, sys
        from torxtools import cfgtools, pathtools
        
        defaults = pathtools.expandpath(["~/.my-cfgfile"])
        parser = argparse.ArgumentParser()
        parser.add_argument('--cfgfile')
        
        args = parser.parse_args(sys.argv[:1])
        print(cfgtools.which(args.cfgfile, defaults))

    """
    if not callable(verify):
        raise TypeError("expected verify to be a callable, not: %r" % verify)

    if cfgfile:
        return cfgfile
    return first(candidates or [], default=default, key=verify)
