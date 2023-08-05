#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import networkx as nx
import sma

def translateGraph(adjacency, attributeNames, attributeValues, typeAttr : str = None) -> nx.Graph:
    """
    Returns a :py:class:`networkx.Graph` from a adjacency matrix, a list of nodal attribute names
    and a matrix of nodal attribute values. This function is designed to make networkx objects
    compatible with R's statnet network objects.
    
    :param adjacency: adjacency matrix provided as a numerical matrix
    :param attributeNames: list of attribute names
    :param attributeValues: matrix of attribute values in accordance to `attributeNames`.
    :param typeAttr: name of an attribute with specifies whether a node is social or ecological.
        The values must match :py:const:`sma.NODE_TYPE_SOC` and :py:const:`sma.NODE_TYPE_ECO`.
        If None, attributeNames must contain 'sesType'.
    
    :returns: networkx graph with the given properties
    """
    G = nx.from_numpy_matrix(adjacency, create_using=nx.Graph())
    
    assert ((typeAttr is not None and typeAttr in attributeNames) or 
           (typeAttr is None and 'sesType' in attributeNames)), 'sesType attribute must be provided'
    
    for attr, values in zip(attributeNames,attributeValues):
        nx.set_node_attributes(G, name=attr, values=dict(enumerate(values)))
        if typeAttr == attr:
            nx.set_node_attributes(G, name='sesType', values=dict(enumerate(values)))
    
    return G

def countAnyMotifs(it : sma.ComplexMotifIterator) -> int:
    """
    Counts the number of elements in the given iterator.
    
    Function for compatability with R.
    """
    try:
        return len(it)
    except TypeError:
        return sum(1 for _ in it)

def motifSet(source : sma.SourceMotifIterator, 
             *conditions : sma.ConditionMotifIterator) -> sma.ComplexMotifIterator:
    """
    Returns an motif interator representing a set of motifs with 
    certain properties.
    
    Function for compatability with R.
    
    :param source: :py:class:`sma.SourceMotifIterator`, the basal set to take the
        motifs from
    :param conditions: one or several :py:class:`sma.ConditionMotifIterator` 
        representing conditions which the motifs must fulfill to be part of the set
    """
    it = source
    for cond in conditions:
        it = it & cond
    return it

def listMotifs(iterator : sma.ComplexMotifIterator) -> list:
    """
    Returns a list of all motifs in a motif iterator.
    
    Function for compatability with R.
    
    :param iterator: motif iterator
    """
    return list(iterator)