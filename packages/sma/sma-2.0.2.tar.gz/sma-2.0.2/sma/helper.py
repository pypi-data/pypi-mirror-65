# -*- coding: utf-8 -*-

import functools
import networkx as nx
import numpy

def binaryArrayHornersMethod(array : list) -> int:
    """
    transforms the binary number encoded in the given array
    to an integer
    
    :example: binaryArrayHornersMethod([1,0,1]) = 5
    """
    return functools.reduce(lambda x, y: x*2 +y, array)

def multiToWeightedGraph(M : nx.MultiGraph, attr = 'weight') -> nx.Graph:
    """
    Helper function for converting a multigraph into a weighted simple graph with
    edge weights corresponding to the multiplicities of the edges in the multigraph.
    
    Nodal attributes are preserved while edge attributes will be lost. Use the 
    second parameter to set the name of the weight attribute.
    
    :param M: a multigraph
    :param attr: name of the weight attribute
    :returns: a simple graph with weighted edges
    """
    R = nx.Graph()
    R.add_nodes_from(M.nodes(data=True))
    for u,v,data in M.edges(data=True):
        if R.has_edge(u,v):
            R[u][v][attr] += 1
        else:
            R.add_edge(u, v, **{attr : 1})
    return R

def maxEdgeCountMatrix(nVertices : numpy.ndarray) -> numpy.ndarray:
    """
    Returns a matrix containing the maximal possible number of edges in the
    subsystems of a multigraph. The entries of this matrix constitute the upper 
    bounds of the entries of the ``nEdges`` parameter of :py:meth:`sma.randomMultiSENs`.
    
    Let :math:`v_1, \dots, v_n` be the entries of ``nVertices``. Then the entries
    of the returned matrix are
    
    .. math:: 
        
        a_{ij} = \\begin{cases} \\frac12 v_i (v_i-1), & i = j \\\\ v_i v_j, & i < j \\end{cases}.
    
    See also :py:meth:`sma.motifClassMatrix`.
    
    :param nVertices: numbers of vertices per subsystem
    """
    N = len(nVertices)
    matrix = numpy.diag([n*(n-1)//2 for n in nVertices])
    for i in range(N):
        for j in range(i+1, N):
            matrix[i][j] = nVertices[i]*nVertices[j]
    return matrix

def randomEdgeCountMatrix(nVertices : numpy.ndarray) -> numpy.ndarray:
    """
    This function takes the result of :py:meth:`sma.maxEdgeCountMatrix` and a matrix
    with random integer entries less or equal this matrix. It can be used to generate
    a random multilevel SEN with :py:meth:`sma.randomMultiSENs`.
    
    :param nVertices: numbers of vertices per subsystem
    """
    matrix = maxEdgeCountMatrix(nVertices)
    random = numpy.random.random_sample(numpy.shape(matrix))
    return numpy.array(numpy.multiply(matrix, random), dtype=int)