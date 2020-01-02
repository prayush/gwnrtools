#!/usr/bin/env python

########################################
## IMPORTS
########################################
import os, sys
from collections import Mapping, Container
from sys import getsizeof
import glob, commands as cmd
from numbers import Number
from collections import Set, Mapping, deque


########################################
## Other FUNCTIONS
########################################


########################################
## USER-FACING FUNCTIONS
########################################
def MemoryUsage(o):
    """Find the memory footprint of a Python object

    This is a recursive function that drills down a Python object graph
    like a dictionary holding nested dictionaries with lists of lists
    and tuples and sets.

    The sys.getsizeof function does a shallow sizeof. It counts each
    object inside a container as pointer only regardless of how big it
    really is.

    :param o: the object
    :param ids:
    :return:
    """
    #{{{
    try: # Python 2
        zero_depth_bases = (basestring, Number, xrange, bytearray)
        iteritems = 'iteritems'
    except NameError: # Python 3
        zero_depth_bases = (str, bytes, Number, range, bytearray)
        iteritems = 'items'

    _seen_ids = set()

    def inner(obj):
        obj_id = id(obj)
        if obj_id in _seen_ids:
            return 0
        _seen_ids.add(obj_id)

        size = sys.getsizeof(obj)

        if isinstance(obj, zero_depth_bases):
            pass # bypass remaining control flow and return
        elif isinstance(obj, (tuple, list, Set, deque)):
            size += sum(inner(i) for i in obj)
        elif isinstance(obj, Mapping) or hasattr(obj, iteritems):
            size += sum(inner(k) + inner(v) for k, v in getattr(obj, iteritems)())

        # Check for custom object instances - may subclass above too
        if hasattr(obj, '__dict__'):
            size += inner(vars(obj))
        if hasattr(obj, '__slots__'): # can have __slots__ with __dict__
            size += sum(inner(getattr(obj, s)) for s in obj.__slots__ if hasattr(obj, s))
        return size

    return inner(o)
    #}}}

def ShowMemoryUsage(objs=[], prefac=1e-6, prefac_name='Mb'):
    """
This is a wrapper around MemoryUsage that takes in a list
of arbitrary objects, and prints their total size
    """
    #{{{
    if type(objs) is not list: objs = [objs]

    mem = 0.0
    for obj in objs: mem += MemoryUsage(obj)

    print("Memory used: %.3f %s" % (mem * prefac, prefac_name))

    sys.stdout.flush()
    return
    #}}}

show_memory_increase = ShowMemoryUsage
