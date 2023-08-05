# -*- coding: utf-8 -*-
# Author: Orlando Chen
# Created: May 10, 2018
# LastChg: Feb 27, 2020


def intersection(setA: list, setB: list):
    """
    intersection of two lists with basic datatype
    """
    setC = []
    for item in setA:
        if item in setB:
            setC.append(item)
    return setC


def union(setA: list, setB: list):
    """
    union of two lists with basic datatype
    """
    setC = []
    setC.extend(setA)
    for item in setA:
        if item in setB:
            setB.remove(item)
    setC.extend(setB)
    return setC


def remove_sets(bigset: list, subset: list):
    """
    remove items of subset B from big set
    """
    setC = []
    setC.extend(bigset)
    for item in subset:
        if item in bigset:
            setC.remove(item)
    return setC




def split(sets: list, quantity: int):
    """
    splits a list into smaller lists, each of sub list contains 
    the (quantity) of items

    Args:
    * [sets] list to split into smaller lists
    * [quantity] the items in each sub list

    Returns:
    * [list] a new list of sub lists
    """

    output = []

    sublist = None
    max_contains = quantity

    for item in sets:

        if sublist is None:
            sublist = []
        
        if max_contains > 0:
            sublist.append(item)
            max_contains = max_contains - 1
        
        if max_contains == 0:
            output.append(sublist)
            sublist = []
            max_contains = quantity

    # something left
    if len(sublist) > 0:
        output.append(sublist)

    # finished
    return output


def clear(sets: list):
    """
    clear all element from a list
    """
    del sets
    sets = []