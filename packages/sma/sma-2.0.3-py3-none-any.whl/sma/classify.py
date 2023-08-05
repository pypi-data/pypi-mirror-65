#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sma
import networkx as nx
import itertools

class MotifClassificator:
    """
    Abstract super class of all motif classificators. Roughly speaking, a classificator
    maps a motif to its motif class, e.g. (Peter, Lake, Forrest) to 'I.C'.
    
    This class cannot be used as classificator as it is abstract. Use one of its
    inheritors, e.g. :py:class:`sma.FourMotifClassificator`.
    
    Each instance of this class is callable mapping a motif to its class. For
    constructing such an object a SEN must be provided. The syntax is as follows,
    cf. :py:class:`sma.ThreeMotifClassificator`.
    
    .. code-block :: Python
    
        import sma    
        # Let G be some SEN
        motif = ('Peter', 'Lake', 'Forrest')
        classificator = sma.ThreeMotifClassificator(G)
        clss = classificator(motif) # e.g. 'I.C'
    
    
    Each inheritor of this class must provide the following attributes. Note, that
    the values listed here are dummies. See the inheriting classes.
    """
    #: the number of vertices a motif consists of
    arity   = 0
    #: the number of classes
    classes = 0
    #: the names of the classes as returned by the classificator
    names   = []
    def __init__(self, G : nx.Graph):
        self.G = G
    def __call__(self, motif):
        raise NotImplementedError("sma.MotifClassificator is an abstract class which should not be used as MotifClassificator")

def classify4Motif(G : nx.Graph, motif) -> str:
    """
    Classifies a 4-motif given as a 4-tuple of its nodes.
    
    See :py:meth:`sma.binaryCodeToClass4Motifs`.
    
    :param G: the graph
    :param motif: the motif given as 4-tuple of its nodes
    :returns: class of the motif as string, e.g. 'I.C'
    """
    s1,s2,e1,e2 = motif
    binary = sma.binaryArrayHornersMethod([
            G.has_edge(s1, s2),
            G.has_edge(s2, e2),
            G.has_edge(e1, e2),
            G.has_edge(s1, e1),
            G.has_edge(s1, e2),
            G.has_edge(s2, e1)
        ])
    return sma.binaryCodeToClass4Motifs(binary)

class FourMotifClassificator(MotifClassificator):
    """
    :py:class:`sma.MotifClassificator` for classifying 4-motifs. Wrapps
    :py:meth:`sma.classify4Motif`.
    """
    arity   = 4
    classes = 28
    #: cf. :py:const:`sma.MOTIF4_NAMES`
    names   = sma.MOTIF4_NAMES
    def __call__(self, motif):
        return classify4Motif(self.G, motif)

def classify3Motif(G : nx.Graph, motif) -> str:
    """
    Classifies a 3-motif given as a 3-tuple of its nodes.
    
    See :py:meth:`sma.binaryCodeToClass3Motifs`.
    
    :param G: the graph
    :param motif: the motif given as 3-tuple of its nodes
    :returns: class of the motif as string, e.g. 'I.C'
    """
    a, b1, b2 = motif
    binary = sma.binaryArrayHornersMethod([
            G.has_edge(b1,b2),
            G.has_edge(a, b1),
            G.has_edge(a, b2)
            ])
    return sma.binaryCodeToClass3Motifs(binary)

class ThreeMotifClassificator(MotifClassificator):
    """
    :py:class:`sma.MotifClassificator` for classifying 3-motifs such as 3E- or
    3S-motifs. Wrapps :py:meth:`sma.classify3Motif`. See also 
    :py:class:`sma.ThreePMotifClassificator` for plain motifs.
    """
    arity   = 3
    classes = 6
    #: cf. :py:const:`sma.MOTIF3_NAMES`
    names   = sma.MOTIF3_NAMES
    def __call__(self, motif):
        return classify3Motif(self.G, motif)

def classify2Motif(G : nx.Graph, motif) -> bool:
    """
    Classifies 2-motifs. These motifs consist of two vertices. Two classes of
    motifs occur. Either the two vertices are linked (type 1) or the two vertices 
    not linked (type 0).
    
    :param G: the SEN
    :param motif: a pair of two vertices, the motif
    """
    return G.has_edge(*motif)

class TwoMotifClassificator(MotifClassificator):
    """
    :py:class:`sma.MotifClassificator` for classifying 2-motifs. See 
    :py:meth:`sma.classify2Motif`.
    """
    arity   = 2
    classes = 2
    names   = [0,1]
    def __call__(self, motif):
        return classify2Motif(self.G, motif)
    
def classify3pMotif(G : nx.Graph, motif) -> int:
    """
    Classifies a plain 3-motif given as a 3-tuple of its nodes.
    
    Since the three vertices in the motif are not distinguishable, there exist 
    four classes of motifs:
        
        - type 0: no edges
        - type 1: one edge
        - type 2: two edges
        - type 3: three edges
    
    :param G: the graph
    :param motif: the motif given as 3-tuple of its nodes
    :returns: class of the motif as integer
    """
    return (G.has_edge(motif[0], motif[1]) 
            + G.has_edge(motif[1], motif[2])
            + G.has_edge(motif[2], motif[0]))
    
class ThreePMotifClassificator(MotifClassificator):
    """
    :py:class:`sma.MotifClassificator` for classifying plain 3-motifs. These are
    motifs that do not respect whether the individual nodes are social or ecological.
    
    See :py:class:`sma.ThreeMotifClassificator` for the classificator that respects
    the types of the nodes.
    """
    arity   = 3
    classes = 4
    names   = [0,1,2,3]
    def __call__(self, motif):
        return classify3pMotif(self.G, motif)
    
class MultiMotifClassificator(MotifClassificator):
    """
    :py:class:`sma.MotifClassificator` for classifying multi-motifs. This class
    is a wrapper class for several other motif classificators. Based on the given
    arities, i.e. the numbers of nodes from the different levels of the SEN, a
    suitable classificator is choosen automatically. This means that depending on
    the given parameters, the number of classes and their names is different.
    
    **Supported types of motifs by arities:**
    
        - ``1,2``: uses :py:class:`sma.ThreeMotifClassificator` and hence its
          classification terminology.
        - ``1,1``: uses :py:class:`sma.TwoMotifClassificator`.
        - ``3``: uses :py:class:`sma.ThreePMotifClassificator`.
        - ``2,2``: uses :py:class:`sma.FourMotifClassificator`.
        - ``1,1,1``: see documentation.
          
          Classes: 0, 1, 2, 3, 4, 5, 6, 7
        - ``1,1,2``: only partial classification available, see documentation.
          
          Classes: -1 (unclassified), 1, 2, 3, 4
        - ``1,2,2``: only partical classification available, see documentation.
          The classification follow the classification of 4-motifs. The two levels
          with two nodes are treated as the two levels of a 4-motif. If the node in 
          the third level is connected to both nodes in the second level but to
          none of the nodes in the first level, the motif is classified as *CLASS*.2
          where *CLASS* is the class returned by a :py:class:`sma.FourMotifClassificator`.
          If the node in the third level is linked to none of the other nodes, the
          returned class is accordingly *CLASS*.0. If the node in the third level
          is linked to the both nodes in the first level the class is *CLASS*.1.
          If the node in the third level is linked to all four other nodes, the class
          is *CLASS*.3.
          
          Classes: Unclassified, I.A.0, ... VII.D.0, ..., I.A.3, ... VII.D.3.
        - ``2,2,2``: only partical classification available, see documentation.
          
          Classes: -1 (unclassified), 1, 2, 3, 4
    
    Every instances of this class is aware of the names and amount of classes that
    it uses for classification. The corresponding object variables are ``classes``
    and ``names``.
    
    **Position matching:** The internal mechanism for matching the levels to the
    arities works as follows. Based on the given arities a matching classificator is
    determined. Each classificator has a pattern of arities that it requires. These
    patterns are listed above. For example the ``1,2,1`` classificator requires
    two levels with one node and one level with two nodes. If the parameter ``roles``
    is left empty, this class will choose the first level in ``arities`` with entry
    1 to be the source of the nodes in the first level of a ``1,2,1``-motif. In this
    way it proceeds with the other requirements. This procedure can be overwritten
    by providing a list of indices in ``roles``. The :math:`i`-th entry of this list
    should contain the index of the layer from which the nodes for level :math:`i`
    of the motif should be chosen from. 
    
    Let's have a look at an example: If ``arities`` is ``2,1,0``, a 
    :py:class:`sma.ThreeMotifClassificator` (``1,2``) will can do the job. Automatically, 
    level 1 will be determined as source for the distinct node and level 0 as source
    for the two other nodes. In case of ``arities = [0,2,2]`` it is more complicated.
    :py:class:`sma.FourMotifClassificator` can be applied here. Automatically, 
    level 1 will be associated with the first level of the 4-motif and level 2 with
    the second. However, this matching may not always be desirable. Level 1 of the
    SEN is treated as social level while level 2 is treated as ecological level. For
    inverting this, one may set ``roles = [2,1]``. Then level 1 is treated as ecological
    level and level 2 as social level.
    
    :param arities: Arities
    :param roles: List of indices
    :raises TypeError: whenever there is no matching classificator available
    """
    def __init__(self, G : nx.Graph, *arities : int, roles = []):
        super().__init__(G)
        self.arity = sum(arities)
        self.arities = arities
        self.roles = roles
        non_triv_ar = _multiSignature(arities)
        if non_triv_ar == [1,2]:
            distinct, others = _matchPositions([1,2], arities, roles)
            self.__inherit(ThreeMotifClassificator(G),
                           lambda motif, distinct=distinct, others=others: motif[distinct] + motif[others])
        elif non_triv_ar == [1,1]:
            pos0, pos1 = _matchPositions([1,1], arities, roles)
            self.__inherit(TwoMotifClassificator(G),
                           lambda motif, pos0 = pos0, pos1 = pos1: motif[pos0] + motif[pos1])
        elif non_triv_ar == [3]:
            position = _matchPositions([3], arities, roles)
            self.__inherit(ThreePMotifClassificator(G),
                           lambda motif, position = position: motif[position])
        elif non_triv_ar == [2,2]:
            pos0, pos1 = _matchPositions([2,2], arities, roles)
            self.__inherit(FourMotifClassificator(G),
                           lambda motif, pos0 = pos0, pos1 = pos1: motif[pos0] + motif[pos1])
        elif non_triv_ar == [1, 1, 1]:
            positions = _matchPositions([1,1,1], arities, roles)
            self.__inherit(Multi111MotifClassificator(G),
                           lambda motif, pos=positions : motif[pos[0]] + motif[pos[1]] + motif[pos[2]])
        elif non_triv_ar == [1, 1, 2]:
            positions = _matchPositions([1,2,1], arities, roles)
            self.__inherit(Multi121MotifClassificator(G),
                           lambda motif, pos=positions : motif[pos[0]] + motif[pos[1]] + motif[pos[2]])
        elif non_triv_ar == [1, 2, 2]:
            positions = _matchPositions([2,2,1], arities, roles)
            self.__inherit(Multi221MotifClassificator(G),
                           lambda motif, pos=positions : motif[pos[0]] + motif[pos[1]] + motif[pos[2]])
        elif non_triv_ar == [2, 2, 2]:
            positions = _matchPositions([2,2,2], arities, roles)
            self.__inherit(Multi222MotifClassificator(G),
                           lambda motif, pos=positions : motif[pos[0]] + motif[pos[1]] + motif[pos[2]])
        else:
            raise TypeError(("For the arities "+','.join(['%d'] * len(arities)) + 
                             " there is no classificator available.") % arities)
    def __inherit(self, classificator : MotifClassificator, adaptor):
        self.classificator = classificator
        self.arity    = classificator.arity
        self.classes  = classificator.classes
        self.names    = classificator.names
        self.__internal_call = lambda motif: classificator(adaptor(motif))
    def __inheritDirectly(self, function, adaptor, arity, classes, names):
        self.classificator = function
        self.arity    = arity
        self.classes  = classes
        self.names    = names
        self.__internal_call = lambda motif, G=self.G: function(G, adaptor(motif))
    def __call__(self, motif):
        return self.__internal_call(motif)
    def __str__(self):
        return 'MultiMotifClassificator[%s]' % str(self.classificator)

# Helper functions for the MultiMotifClassificator
        
def _multiSignature(arities):
    return sorted(filter(lambda a : a != 0, arities))

def _matchPositions(pattern, arities, roles):
    if len(pattern) == len(roles):
        return roles
    else:
        positions = []
        last = {}
        for p in pattern:
            if p in last:
                last[p] = arities.index(p, last[p]+1)
            else:
                last[p] = arities.index(p)
            positions.append(last[p])
        return positions

# Underneath you find very messy classificators for multi-motifs.

class Multi111MotifClassificator(MotifClassificator):
    arity   = 3
    classes = 8
    names   = [0, 1, 2, 3, 4, 5, 6, 7]
    def __call__(self, motif):
        return classify111Motif(self.G, motif)

def classify111Motif(G : nx.Graph, motif) -> int:
    a, b, c = motif
    return 4 * G.has_edge(a,c) + 2 * G.has_edge(b, c) + G.has_edge(a, b)

class Multi121MotifClassificator(MotifClassificator):
    arity   = 4
    classes = 5
    names   = [-1, 1, 2, 3, 4]
    def __call__(self, motif):
        return classify121Motif(self.G, motif)

def classify121Motif(G : nx.Graph, motif) -> int:
    a, b1, b2, c = motif
    if G.has_edge(b1, c) and G.has_edge(b2, c):
        if G.has_edge(a, c) and G.has_edge(b1, a) and G.has_edge(b2, a):
            # induced subgraphs {a, b1, c} and {a, b2, c} complete
            if G.has_edge(b1, b2):
                return 4 # Ohio E closed
            else:
                return 3 # Ohio E open
        if not(G.has_edge(b1, b2)) and not(G.has_edge(a,c)):
            t = G.has_edge(a, b1) + G.has_edge(a, b2)
            if t == 1:
                return 1 # (i)
            elif t == 2:
                return 2 # (h)
    return -1

class Multi221MotifClassificator(MotifClassificator):
    arity   = 5
    names   = ['Unclassified'] + list(map(lambda x : '%s.%d' % x, itertools.product(sma.MOTIF4_NAMES, [0,1,2,3])))
    classes = len(names)
    def __call__(self, motif):
        return classify221Motif(self.G, motif)

def classify221Motif(G : nx.Graph, motif) -> str:
    a1, a2, b1, b2, c = motif
    if G.has_edge(a1, c) ^ G.has_edge(a2, c):
        return 'Unclassified'
    if G.has_edge(b1, c) ^ G.has_edge(b2, c):
        return 'Unclassified'
    block4 = classify4Motif(G, (a1, a2, b1, b2))
    if G.has_edge(a1, c):
        if G.has_edge(b1, c):
            return '%s.%d' % (block4, 3) # both bound
        else:
            return '%s.%d' % (block4, 1) # only (a) bound
    else:
        if G.has_edge(b1, c):
            return '%s.%d' % (block4, 2) # only (b) bound
        else:
            return '%s.%d' % (block4, 0) # nothing bound
    return 'Unclassified'

class Multi222MotifClassificator(MotifClassificator):
    arity   = 6
    classes = 5
    names   = [-1, 1, 2, 3, 4]
    def __call__(self, motif):
        return classify222Motif(self.G, motif)

def classify222Motif(G : nx.Graph, motif) -> int:
    a1, a2, b1, b2, c1, c2 = motif
    if G.has_edge(b1, b2) or not(G.has_edge(c1,c2)):
        return -1
    AC = (G.has_edge(a1, c1) + G.has_edge(a2, c2) +
          G.has_edge(a1, c2) + G.has_edge(a2, c1))
    if AC == 4: # all a-c edges are there
        if (G.has_edge(a1, b1) and G.has_edge(a2, b2) and
            G.has_edge(a1, b2) and G.has_edge(a2, b1) and
            G.has_edge(b1, c1) and G.has_edge(b2, c2) and
            G.has_edge(b1, c2) and G.has_edge(b2, c1)):
            if G.has_edge(a1, a2):
                return 4 # Ohio H closed
            else:
                return 3 # Ohio H open
        return -1
    elif AC == 0: # no a-c edges
        if not(G.has_edge(a1, b1)): # swap b1 and b2 
            h = b1
            b1 = b2
            b2 = h
        if not(G.has_edge(b1, c1)): # swap c1 and c2
            h = c1
            c1 = c2
            c2 = h
        if (G.has_edge(a1, b1) and G.has_edge(b1, c1) and
            G.has_edge(a2, b2) and G.has_edge(b2, c2) and
            not(G.has_edge(a1, b2)) and not(G.has_edge(a2, b1)) and
            not(G.has_edge(b1, c2)) and not(G.has_edge(b2, c1))):
            if G.has_edge(a1, a2):
                return 2 # (m)
            else:
                return 1 # (n)
    return -1