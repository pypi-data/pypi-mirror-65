"""Library for flattening nested values of container types.

Python library for common functionalities related to flattening
nested values of container types.
"""
import types
import doctest

def _is_container(v):
    return any(isinstance(v, t) for t in [
        types.GeneratorType,
        list,
        set, frozenset,
        tuple
    ])

def flats(value, depth = 1):
    """
    Flatten a value that consists of nested values
    of some built-in container type(s).

    >>> list(flats([[1,2,3],[4,5,6,7]]))
    [1, 2, 3, 4, 5, 6, 7]
    >>> list(flats([[[1,2],3],[4,5,6,7]], depth=2))
    [1, 2, 3, 4, 5, 6, 7]
    >>> list(flats([[[1,2],[3]],[[4,5],[6,7]]], depth=2))
    [1, 2, 3, 4, 5, 6, 7]
    >>> list(flats([[[1,2],3],[4,5,6,7]], depth=1))
    [[1, 2], 3, 4, 5, 6, 7]
    >>> list(flats([[[1,2],3],[4,5,6,7]], depth=0))
    [[[1, 2], 3], [4, 5, 6, 7]]
    >>> list(flats([[[1,2],3],[4,5,6,7]], depth=float('inf')))
    [1, 2, 3, 4, 5, 6, 7]
    """
    if depth == 1: # Most common case is first for efficiency.
        for vs in value:
            if _is_container(vs):
                for v in vs:
                    yield v
            else:
                yield vs
    elif depth == 0:
        for v in value:
            yield v
    else: # General recursive case.

        for vs in value:
            if isinstance(depth, int) and depth >= 1:
                if _is_container(vs):
                    for v in flats(vs, depth=depth-1):
                        yield v
                else:
                    yield vs
            elif depth == float('inf'):
                if _is_container(vs):
                    for v in flats(vs, depth = float('inf')):
                        yield v
                else:
                    yield vs
            elif not isinstance(depth, int) and depth == float('inf'):
                raise TypeError("depth must be an integer or infinity")
            elif isinstance(depth, int) and depth < 0:
                raise ValueError("depth must be a non-negative integer")
            else:
                raise ValueError("invalid depth value")

if __name__ == "__main__": 
    doctest.testmod()
