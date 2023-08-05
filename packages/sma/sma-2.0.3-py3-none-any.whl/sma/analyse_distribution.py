#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sma
import networkx as nx
from scipy.special import binom
import numpy
import functools, itertools

def _probability(edges, sym, maxedges, probs):
    prob = sym
    for e, p, m in zip(edges, probs, maxedges):
        prob *= p**e * (1-p)**(m-e)
    return prob

def expectedMultiMotifs(G : nx.Graph,
                        *arities, 
                        roles = [],
                        **kwargs):
    """
    Front-end function for several functions for computing motif expectations. It supports
    the same parameters for defining the motifs (arities, roles) as other multi-level
    (counting) functions. Check the documentations of the respective functions.
    The supported functions are:
        
        - :py:meth:`sma.expected3Motifs`
        - :py:meth:`sma.expected4Motifs`
        - :py:meth:`sma.expected121Motifs`
        - :py:meth:`sma.expected221Motifs`
        - :py:meth:`sma.expected222Motifs`
    
    See the documentation for an exposition of the mathematical background.
    
    :param G: the SEN
    :param arities: arities of the motifs, cf. :py:class:`sma.MultiMotifClassificator`.
    :param roles: roles of the levels, cf. :py:class:`sma.MultiMotifClassificator`.
    :param kwargs: additional parameters for the functions, see above.
    """
    signature = sma.classify._multiSignature(arities)
    multis = [
                # signature, ordered,  function
                ([1, 2],    [1, 2],    sma.expected3Motifs),
                ([2, 2],    [2, 2],    sma.expected4Motifs),
                ([1, 1, 2], [1, 2, 1], sma.expected121Motifs),
                ([1, 2, 2], [2, 2, 1], sma.expected221Motifs),
                ([2, 2, 2,],[2, 2, 2], sma.expected222Motifs)
            ]
    for sig, sig_ordered, counter in multis:
        if signature == sig:
            positions = sma.classify._matchPositions(sig_ordered, arities, roles)
            return counter(G, *positions, **kwargs)
            
    raise TypeError('No suitable function for computing expectations found')

def expected3Motifs(G : nx.Graph, 
                    level0, 
                    level1, 
                    array = False, 
                    densities : bool = False):
    """
    Computes the expected number of 3-motifs in a SEN. See the documentation for an
    exposition of the mathematical background.
    
    Use functions :py:meth:`sma.expected3EMotifs` and :py:meth:`sma.expected3SMotifs`
    for regular two level graphs.
    
    If ``densities = True``, the returned values sum up to one. Otherwise their
    sum is total number of 3-motifs, see :py:meth:`sma.total3EMotifs` etc.
    
    :param G: the SEN
    :param level0: ``sesType`` of the distinct node, e.g. in 3E-motifs :py:const:`sma.NODE_TYPE_ECO`
    :param level1: ``sesType`` of the other nodes, e.g. in 3E-motifs :py:const:`sma.NODE_TYPE_SOC`
    :param array: whether the result shall be an array or a dict
    :param densities: whether densities or absolute numbers of motifs shall be returned
    """
    v = sma.nodesCount(G)
    m = sma.maxEdgeCountMatrix(list(v.values()))
    d = sma.edgesCountMatrix(G)
    
    total = 1 if densities else binom(v[level1], 2) * v[level0]
    p0 = d[level0, level1] / m[level0, level1] if level0 <= level1 else d[level1,level0] / m[level1,level0]
    p1 = d[level1, level1] / m[level1, level1]
    
    maxedges = numpy.max(sma.MOTIF3_EDGES, axis = 0)
    res = list(itertools.starmap(functools.partial(_probability, maxedges = maxedges, probs = [p1, p0]),
                  zip(sma.MOTIF3_EDGES, sma.MOTIF3_AUT)))
    results = total * numpy.array(res)
    if not array:
        return {k : v for k,v in zip(sma.MOTIF3_NAMES, results)}
    return results

def expected4Motifs(G : nx.Graph, 
                    level0 = sma.NODE_TYPE_SOC, 
                    level1 = sma.NODE_TYPE_ECO, 
                    array = False, 
                    densities = False):
    """
    Computes the expected number of 4-motifs in a SEN. See the documentation for an
    exposition of the mathematical background.
    
    If ``densities = True``, the returned values sum up to one. Otherwise their
    sum is total number of 4-motifs, see :py:meth:`sma.total4Motifs` etc.
    
    :param G: the SEN
    :param level0: ``sesType`` of the upper nodes, standard :py:const:`sma.NODE_TYPE_SOC`
    :param level1: ``sesType`` of the lower nodes, e.g. in 3E-motifs :py:const:`sma.NODE_TYPE_ECO`
    :param array: whether the result shall be an array or a dict
    :param densities: whether densities or absolute numbers of motifs shall be returned
    """
    v = sma.nodesCount(G)
    m = sma.maxEdgeCountMatrix(list(v.values()))
    d = sma.edgesCountMatrix(G)
    
    total = 1 if densities else binom(v[level1], 2) * binom(v[level0], 2)
    p0 = d[level0, level0] / m[level0, level0]
    p1 = d[level0, level1] / m[level0, level1] if level0 <= level1 else d[level1,level0] / m[level1,level0]
    p2 = d[level1, level1] / m[level1, level1]
    maxedges = numpy.max(sma.MOTIF4_EDGES, axis = 0)

    res = list(itertools.starmap(functools.partial(_probability, maxedges = maxedges, probs = [p0, p1, p2]),
                  zip(sma.MOTIF4_EDGES, sma.MOTIF4_AUT)))
    results = total * numpy.array(res)
    if not array:
        return {k : v for k,v in zip(sma.MOTIF4_NAMES, results)}
    return results

def expected3EMotifs(G : nx.Graph, **kwargs):
    """
    Computes the expected number of 3E-motifs in a SEN. See the documentation for an
    exposition of the mathematical background. See also :py:meth:`sma.expected3Motifs`.
    
    :param G: the SEN
    :param kwargs: additional parameters for :py:meth:`sma.expected3Motifs`.
    """
    return expected3Motifs(G, sma.NODE_TYPE_ECO, sma.NODE_TYPE_SOC, **kwargs)
def expected3SMotifs(G : nx.Graph, **kwargs):
    """
    Computes the expected number of 3S-motifs in a SEN. See the documentation for an
    exposition of the mathematical background. See also :py:meth:`sma.expected3Motifs`.
    
    :param G: the SEN
    :param kwargs: additional parameters for :py:meth:`sma.expected3Motifs`.
    """
    return expected3Motifs(G, sma.NODE_TYPE_SOC, sma.NODE_TYPE_ECO, **kwargs)

def expected121Motifs(G : nx.Graph, 
                      level0, 
                      level1, 
                      level2, 
                      array = False,
                      density = False):
    """
    Computes the expected number of multi level motifs with arities 1, 2, 1. 
    See the documentation for an exposition of the mathematical background.
    
    :param G: the SEN
    :param level0: ``sesType`` of the upper node
    :param level1: ``sesType`` of the middle nodes
    :param level2: ``sesType`` of the lower node
    :param array: whether the result shall be an array or a dict
    :param densities: whether densities or absolute numbers of motifs shall be returned
    """
    v = sma.nodesCount(G)
    m = sma.maxEdgeCountMatrix(list(v.values()))
    d = sma.edgesCountMatrix(G)
    total = 1 if density else v[level0] * binom(v[level1], 2) * v[level2]
    p01 = d[level0, level1] / m[level0, level1] if level0 <= level1 else d[level1,level0] / m[level1,level0]
    p02 = d[level0, level2] / m[level0, level2] if level0 <= level2 else d[level2,level0] / m[level2,level0]
    p11 = d[level1, level1] / m[level1, level1]
    p12 = d[level1, level2] / m[level1, level2] if level1 <= level2 else d[level2,level1] / m[level2,level1]
    results = numpy.array([
            0,
            2 * p01 * (1-p01) * (1-p11) * p12**2 * (1-p02),
            p01**2 * (1-p11) * p12**2 * (1-p02),
            p01**2 * (1-p11) * p12**2 * p02,
            p01**2 * p11 * p12**2 * p02,
        ])
    results[0] = 1 - sum(results)
    results = total * results
    if array:
        return results
    return {k : r for k, r in zip([-1,1,2,3,4], results)}

def expected221Motifs(G : nx.Graph, 
                      level0, 
                      level1, 
                      level2, 
                      array = False,
                      density = False):
    """
    Computes the expected number of multi level motifs with arities 2, 2, 1. 
    See the documentation for an exposition of the mathematical background.
    
    Uses :py:meth:`sma.expected4Motifs` for computing the expectations of the upper
    part.
    
    :param G: the SEN
    :param level0: ``sesType`` of the upper node
    :param level1: ``sesType`` of the middle nodes
    :param level2: ``sesType`` of the lower node
    :param array: whether the result shall be an array or a dict
    :param densities: whether densities or absolute numbers of motifs shall be returned
    """
    v = sma.nodesCount(G)
    m = sma.maxEdgeCountMatrix(list(v.values()))
    d = sma.edgesCountMatrix(G)
    total = 1 if density else binom(v[level0], 2) * binom(v[level1], 2) * v[level2]
    p02 = d[level0, level2] / m[level0, level2] if level0 <= level2 else d[level2,level0] / m[level2,level0]
    p12 = d[level1, level2] / m[level1, level2] if level1 <= level2 else d[level2,level1] / m[level2,level1]
    
    values4 = sma.expected4Motifs(G, level0, level1, array = True, densities = True)
    
    factors = [
            (1-p02)**2 * (1-p12)**2,
            p02**2 * (1-p12)**2,
            (1-p02)**2 * p12**2,
            p02**2 * p12**2,
        ]
    result = {'Unclassified' : 0, **{
            '%s.%d' % (m, i) : total * f * v
            for (m, v), (i, f) in itertools.product(zip(sma.MOTIF4_NAMES, values4), zip([0, 1, 2, 3], factors))
        }}
    result['Unclassified'] = total - sum(result.values())
    if array:
        return numpy.array(list(result.values()))
    return result

def expected222Motifs(G : nx.Graph, 
                      level0, 
                      level1, 
                      level2, 
                      array = False,
                      density = False):
    """
    Computes the expected number of multi level motifs with arities 2, 2, 2. 
    See the documentation for an exposition of the mathematical background.
    
    :param G: the SEN
    :param level0: ``sesType`` of the upper node
    :param level1: ``sesType`` of the middle nodes
    :param level2: ``sesType`` of the lower node
    :param array: whether the result shall be an array or a dict
    :param densities: whether densities or absolute numbers of motifs shall be returned
    """
    v = sma.nodesCount(G)
    m = sma.maxEdgeCountMatrix(list(v.values()))
    d = sma.edgesCountMatrix(G)
    total = 1 if density else binom(v[level0], 2) * binom(v[level1], 2) * binom(v[level2], 2)
    p00 = d[level0, level0] / m[level0, level0]
    p01 = d[level0, level1] / m[level0, level1] if level0 <= level1 else d[level1,level0] / m[level1,level0]
    p02 = d[level0, level2] / m[level0, level2] if level0 <= level2 else d[level2,level0] / m[level2,level0]
    p11 = d[level1, level1] / m[level1, level1]
    p12 = d[level1, level2] / m[level1, level2] if level1 <= level2 else d[level2,level1] / m[level2,level1]
    p22 = d[level2, level2] / m[level2, level2]

    results = numpy.array([
            0,
            2 * (1-p00) * (1-p01)**2 * p01**2 * (1-p12)**2 * (1-p11) * p12**2 * p22 * (1-p02)**4,
            2 * p00 * (1-p01)**2 * p01**2 * (1-p12)**2 * (1-p11) * p12**2 * p22 * (1-p02)**4,
            (1-p00) * p01**4 * p02**4 * (1-p11) * p12**4 * p22,
            p00 * p01**4 * p02**4 * (1-p11) * p12**4 * p22
        ])
    results[0] = 1 - sum(results)
    results = total * results
    if array:
        return results
    return {k : r for k, r in zip([-1,1,2,3,4], results)}

def var3Motifs(G : nx.Graph, 
               level0, 
               level1, 
               array : bool = False,
               second_moment : bool = False):
    """
    Computes variances of the number for 3-motifs in a SEN. See documentation for
    the mathematical background.
    
    This function uses the following formula where :math:`X` denotes the random
    variable number of 3-motifs
    
    .. math::
        
        \mathbb{V}[X] = \mathbb{E}[X^2] - (\mathbb{E}[X])^2
        
    
    and computes the expectation using :py:meth:`sma.expected3Motifs`. Set
    ``second_moment = True`` to compute :math:`\mathbb{E}[X^2]` instead of the variance.
    In this case :py:meth:`sma.expected3Motifs` is not called.
    
    :param G: the SEN
    :param level0: ``sesType`` of the distinct node, e.g. in 3E-motifs :py:const:`sma.NODE_TYPE_ECO`
    :param level1: ``sesType`` of the other nodes, e.g. in 3E-motifs :py:const:`sma.NODE_TYPE_SOC`
    :param array: whether the result should be an array instead of a dict
    :param second_moment: switch on for computing the second moment instead of the
        variance
    """
    m = sma.maxEdgeCountMatrix(sma.nodesCount(G, array = True))
    d = sma.edgesCountMatrix(G)
    v = sma.nodesCount(G)
    p0 = d[level0, level1] / m[level0, level1] if level0 <= level1 else d[level1,level0] / m[level1,level0]
    p1 = d[level1, level1] / m[level1, level1]
    v0 = v[level0]
    v1 = v[level1]     
    partition = numpy.array([
                 v0 * binom(v1,2),                           # all nodes shared
                 v0 * v1 * (v1-1) * (v1-2),                  # one from each level shared
                 binom(v1, 2) * v0 * (v0-1),                 # two from non-distinct level shared
                 v0 * v1 * (v0-1) * (v1-1) * (v1-2),         # one non-distinct node shared
                 v0 * binom(v1,2) * binom(v1-2,2),           # distinct node shared
                 v0 * (v0-1) * binom(v1,2) * binom(v1-2,2)   # no nodes shared
            ])
    # one column for each partion, see above
    # one row for each motif I.A-II.C
    motifprops = numpy.array([
                [(1-p0)**2 * (1-p1), (1-p0)**3*(1-p1)**2,                   (1-p0)**4 * (1-p1),        (1-p0)**4 * (1-p1)**2,       (1-p0)**4 * (1-p1)**2,       (1-p0)**4 * (1-p1)**2],
                [2*(1-p0)*(1-p1)*p0, (1-p1)**2*((1-p0)**2*p0+p0**2*(1-p0)), 4*(1-p0)**2*p0**2 *(1-p1), 4*(1-p0)**2*p0**2*(1-p1)**2, 4*(1-p0)**2*p0**2*(1-p1)**2, 4*(1-p0)**2*p0**2*(1-p1)**2],
                [p0**2*(1-p1),       p0**3*(1-p1)**2,                       p0**4*(1-p1),              p0**4*(1-p1)**2,             p0**4*(1-p1)**2,             p0**4*(1-p1)**2],
                [(1-p0)**2 *p1,      (1-p0)**3*p1**2,                       (1-p0)**4*p1,              (1-p0)**4 * p1**2,           (1-p0)**4 * p1**2,           (1-p0)**4 * p1**2],
                [2*(1-p0)*p1*p0,     p1**2*((1-p0)**2*p0+p0**2*(1-p0)),     4*(1-p0)**2*p0**2 * p1,    4*(1-p0)**2*p0**2*p1**2,     4*(1-p0)**2*p0**2*p1**2,     4*(1-p0)**2*p0**2*p1**2],
                [p0**2*p1,           p0**3*p1**2,                           p0**4*p1,                  p0**4*p1**2,                 p0**4*p1**2,                 p0**4*p1**2]
            ])
    if second_moment:
        result = motifprops @ partition
    else:
        expectations = expected3Motifs(G, level0, level1, array=True)
        result = motifprops @ partition - expectations**2
    if array:
        return result
    else:
        return {k : v for k, v in zip(sma.MOTIF3_NAMES, result)}
    
def var3EMotifs(G : nx.Graph, **kwargs):
    """
    Computes the variance of the number of 3E-motifs in a SEN. See the documentation for a
    exposition of the mathematical background. See also :py:meth:`sma.expected3Motifs`.
    
    :param G: the SEN
    :param kwargs: additional parameters for :py:meth:`sma.var3Motifs`.
    """
    return var3Motifs(G, sma.NODE_TYPE_ECO, sma.NODE_TYPE_SOC, **kwargs)

def var3SMotifs(G : nx.Graph, **kwargs):
    """
    Computes the variance of the number of 3S-motifs in a SEN. See the documentation for a
    exposition of the mathematical background. See also :py:meth:`sma.expected3Motifs`.
    
    :param G: the SEN
    :param kwargs: additional parameters for :py:meth:`sma.var3Motifs`.
    """
    return var3Motifs(G, sma.NODE_TYPE_SOC, sma.NODE_TYPE_ECO, **kwargs)

def markovBound(value : numpy.ndarray, expectation : numpy.ndarray) -> numpy.ndarray:
    """
    Uses Markov's inequality to compute bounds for the probability that a random
    variable with given expectation takes values higher than the given values.
    
    .. math::
        
        \mathbb{P}[X \geq a] \leq \\frac{\mathbb{E}[X]}{a} 
        
    where :math:`a` is given by ``values`` and :math:`\mathbb{E}[X]` is given
    by ``expectation``.
    
    See `Markov's inequality on Wikipedia <https://en.wikipedia.org/wiki/Markov%27s_inequality>`_.
    
    :param value: the value
    :param expectation: the expectation
    :returns: bounds on the probabilities
    """
    return expectation / value

def cantelliBound(value : numpy.ndarray, 
                  expectation : numpy.ndarray, 
                  variance : numpy.ndarray) -> numpy.ndarray:
    """
    Uses Cantelli's inequality to compute bounds for the probability that a random
    variable with given expectation takes values higher/lower than the given values.
    
    .. math::
        :nowrap:
        
        \[
        \mathbb{P}[X - \mathbb{E}[X]\geq a] \leq 
        \\begin{cases}
        \\frac{\sigma^2}{\sigma^2 + a^2}, & a > 0 \\\\
        1 - \\frac{\sigma^2}{\sigma^2 + a^2}, & a < 0 \\\\ \end{cases}.
        \]
    
    where :math:`a` is given by ``value`` minus ``expectation`` and 
    :math:`\sigma^2` is given by ``variance``.
    
    See `Cantelli's inequality on Wikipedia <https://en.wikipedia.org/wiki/Cantelli%27s_inequality>`_.
    
    :param value: the value
    :param expectation: the expectation
    :returns: bounds on the probabilities
    """
    l = value - expectation
    bound = variance / (variance + l**2)
    signs = l < 0
    return signs * 1 + ((signs * -2)+1) * bound