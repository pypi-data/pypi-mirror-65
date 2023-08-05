"""
Functions for working with filesystem paths.

The :func:`expandpath` does recursive shell-like expansion of paths from lists.
"""
import os

import boltons.pathutils

from torxtools import xdgtools

__all__ = [
    "expandpath",
]


def expandpath(path):
    """
    Recursive shell-like expansion of environment variables and tilde home directory.

    Parameters
    ----------
    path: str, [str], None
        a single path, a list of paths, or none.

    Returns
    -------
    str, [str], None:
        a single expanded path, a list of expanded path, or none

    Example
    -------

    .. code-block:: python

        import os
        from torxtools import pathtools
        os.environ['SPAM'] = 'eggs'
        assert pathtools.expandpath(['~/$SPAM/one', '~/$SPAM/two']) == [os.path.expanduser('~/eggs/one'), os.path.expanduser('~/eggs/two')]

    See Also
    --------
    :py:func:`boltons:boltons.pathutils.expandpath`
    """

    def _expandpath(path):
        if path is None:
            return None
        if isinstance(path, list):
            return [_expandpath(p) for p in path]
        return boltons.pathutils.expandpath(path)

    return _expandpath(path)
