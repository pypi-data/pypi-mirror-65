"""
Dictionnary handling convenience functions.
"""

from copy import deepcopy

from boltons import iterutils

strip_none = lambda _p, k, v: k is not None and v is not None


def _deepmerge(src, dest, path=None):
    """
    Take every key, value from src and merge it recursivly into dest.
    Adapted from https://stackoverflow.com/questions/7204805

    :param dest: destination dict
    :param src: source dict
    :returns: merged dict
    """
    if path is None:
        path = []

    for key in src:
        if key not in dest:
            dest[key] = src[key]
        elif isinstance(dest[key], dict) and isinstance(src[key], dict):
            _deepmerge(src[key], dest[key], path + [str(key)])
        elif dest[key] == src[key]:
            pass  # same leaf value
        else:
            dest[key] = src[key]
    return dest


def deepmerge(*args, visit=None):
    """
    Take every key and value from first and merge it recursively into second
    without changing first nor second.

    :param args: sources, left to right
    :returns: A merged dictionnary
    """
    if not args:
        return None

    context = {}
    for i in range(len(args)):
        if args[i] is None:
            source = {}
        else:
            source = deepcopy(args[i])

        if visit:
            source = iterutils.remap(source, visit=visit)

        context = _deepmerge(source, context)

    return context
