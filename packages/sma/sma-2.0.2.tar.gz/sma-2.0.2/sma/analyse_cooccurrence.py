#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import networkx as nx
import itertools, numpy
import sma
import multiprocessing

def cooccurrenceTable(G : nx.Graph, *motifs, to_array : bool = False, to_dict : bool = False):
    """
    Returns the co-occurrence table for a given set of motif generators. This table
    contains one row for each node in the given SEN G. The :math:`i`-th entry for 
    the :math:`j`-th row represents the number of occurences of the :math:`j`-th 
    node in motifs yielded by the :math:`i`-th motif generator.
    
    For example, one could want to count the number of occurences of nodes in closed
    and open triangles::
        
        import sma
        # let G be some SEN
        result = sma.cooccurrenceTable(G, 
                                       sma.ThreeEMotifs(G) & sma.is3Type('I.C'), 
                                       sma.ThreeEMotifs(G) & sma.is3Type('II.C'))
    
    Then the first entry for each node contains the number of open triangles 
    (type I.C motif) this node is involved in and the second entry the number of
    closed triangles (type II.C motif). Note, that in this example the involvement
    of a node at any position (not only at the distinct position) counts, cf.
    :py:meth:`sma.triangleCoefficient`.
    
    See also :py:meth:`sma.cooccurrenceTableFull`.
    
    :param G: the SEN
    :param motifs: a list of motif generators, cf. :py:class:`sma.MotifIterator`
    :param to_array: boolean indicating whether the output should be a numpy
        array, entries for nodes a given in the order returned by the graph
    :param to_dict: boolean indicating whether the output should be a two-level
        dict. Values can be accessed by ``result[node][motif]`` where motif is 
        the string representation of the motif
    :returns: co-occurence table as described above
    """
    result = {node : [0]*len(motifs) for node in G.nodes}
    for generator, i in zip(motifs, itertools.count()):
        for motif in generator:
            for node in motif:
                result[node][i] += 1
    if to_array:
        return numpy.array(list(result.values()))
    if to_dict:
        gstrings = list(map(lambda x : x.__str__(), motifs))
        return {node : {gstrings[i] : result[node][i] for i in range(len(motifs))} for node in G.nodes}
    return result

def cooccurrenceTableFull(G : nx.Graph, 
                          iterator : sma.MotifIterator, 
                          classificator : sma.MotifClassificator,
                          to_array : bool = False):
    """
    This function returns a dict/array similar to the result of :py:meth:`sma.cooccurrenceTable`.
    This function should be used when the values for several classes of motifs taken
    from the same source iterator are of interest. For example, if all 3-motifs
    shall be fully classified, :py:meth:`sma.cooccurrenceTableFull` should be 
    preferred over :py:meth:`sma.cooccurrenceTable` since it does not incur any 
    redundant costs.
    
    If the parameter ``to_array`` is set to ``False`` (default), the result is 
    a dictionary which maps vertices to subdictionaries mapping motif types (taken
    from the classificator) to the integer representing the number of occasions this
    vertic occurs in a motif of this type. If ``to_array`` is flipped, the result 
    is converted to a matrix with one row for each vertex and one column for each
    motif class.
    
    The sum of all entries equals the total number of motifs in the iterator
    multiplied by the arity of the classificator.
    
    :param G: a SEN
    :param iterator: a :py:class:`sma.MotifIterator` as source of motifs
    :param classificator: a :py:class:`sma.MotifClassificator` for classifying the
        motifs
    :param to_array: whether the result should be an array or a dict.
    :returns: cooccurrences table featuring values for all types of motifs
    
    """
    result = {node : {} for node in G.nodes}
    for motif in iterator:
        for node in motif:
            typ = classificator(motif)
            if typ in result[node]:
                result[node][typ] += 1
            else:
                result[node][typ] = 1
    if to_array:
        return numpy.array([[row[motif] if motif in row else 0 for motif in classificator.names] for row in result.values()])
    return result
    
def motifMultigraph(G : nx.Graph, *motifs, attr = 'motif') -> nx.MultiGraph:
    """
    Returns a multigraph of motifs. In this multigraph every node represents motif.
    For example, when the second parameter is ``sma.FourMotif(G)``, then every
    node in the returned graph represents one 4-motif. Each edge connecting two 
    nodes :math:`m_1`, :math:`m_2` represents one node in the original graph that is shared by two
    motifs that :math:`m_1` and :math:`m_2` represent.
    
    Note that the motif multigraph does not contain any loops since each motifs
    shares trivially all its vertices with itself.
    
    A list of motif iterators must be given, cf. :py:class:`sma.MotifIterator`.
    In this way different types of motifs can be incorporated in one multigraph.
    For example, one could be interested in the adjacence of open triangles with
    distinct social node (social motif I.C) and closed triangles with distinct 
    ecological node (ecological motif II.C). Then these two motif iterators can
    be provided as input, cf. :py:class:`sma.ThreeEMotifs`, :py:class:`sma.ThreeSMotifs`
    and :py:class:`sma.is3Type`.
    
    The multigraph can be converted to a weighted simple graph with edge weights
    corresponding to edge multiplicities in the multigraph using :py:meth:`sma.multiToWeightedGraph`.
    See also :py:meth:`sma.motifWeightedGraph`.
    
    The type of the motifs, i.e. a string representation of the given motif 
    iterators, is stored as nodal attribute.
    
    :param G: a SEN
    :param motifs: one or several instances of :py:class:`sma.MotifIterator`
    :param attr: attribute key for the nodal attribute representing the type
        of the motifs, default ``motif``
    :returns: motif multigraph
    """
    M = nx.MultiGraph()
    for motif in motifs:
        M.add_nodes_from(motif, **{attr : motif.__str__()})
    sesTypes = nx.get_node_attributes(G, 'sesType')
    for m1, m2 in itertools.combinations(M.nodes, 2):
        common = set(m1).intersection(set(m2))
        for n in common:
            M.add_edge(m1, m2, sesType=sesTypes[n], name=n)
    return M

def motifWeightedGraph(G : nx.Graph, *motifs, attr='weight') -> nx.Graph:
    """
    Returns a weighted graph corresponding to the motif multigraph generated 
    by :py:meth:`sma.motifMultigraph`. That two motifs share vertices is not
    encoded by multiple edges but by edge weights.
    
    See :py:meth:`sma.multiToWeightedGraph`, the function that takes care of the
    translation.
    
    :param G: the SEN
    :param motifs: one or several instances of :py:class:`sma.MotifIterator`
    :param attr: the attribute key for the weight attribute, default is ``weight``.
    """
    M = motifMultigraph(G, *motifs)
    return sma.multiToWeightedGraph(M, attr)

def motifClassMatrix(G : nx.Graph, 
                     iterator : sma.MotifIterator, 
                     classificator : sma.MotifClassificator,
                     as_symmetric : bool = False) -> numpy.ndarray:
    """
    In the returned quadratic matrix every column and every row represents a motif
    class, i.e. a type of motif as recorgnized by the given :py:class:`sma.MotifClassificator`.
    For example, in case of 3-motifs the first column and the first row represent
    type 'I.A' motifs whereas the last row / column represents 'II.C' motifs. In
    total, the matrix would be of dimension :math:`6 \\times 6` since there are six
    3-motifs.
    
    The :math:`(i,j)`-th entry represents the number of vertices in the given SEN shared
    by motifs of type :math:`i` and :math:`j`. If a vertex is contained in several type 
    :math:`i` and type :math:`j` motifs, it is counted multiply.
    
    Let :math:`(C_{ij})` denote the returned matrix. Then for the sum of all upper
    triangular entries the following correspondance holds:
    
    .. math ::
        
        \\sum_{i \\geq j} C_{ij} = \\frac12 \\sum_{M_1} \\sum_{M_2 \\neq M_1} 
        \\left| M_1 \\cap M_2 \\right|
        
    where :math:`M_1` and :math:`M_2` are motifs taken from the iterator.
    
    This function computes the desired matrix based on the result of :py:meth:`sma.cooccurrenceTableFull`.
    For every vertex its occurrence in each of the possible classes of motifs is
    counted. Let red, blue and orange be three distinct motif classes. If a vertex occurres 
    :math:`n` times in red motifs, :math:`m_1` times in blue motifs and :math:`m_2`
    times in orange motifs, then it establishes :math:`\\binom{n}{2}` connections
    between red motifs. Hence it contributes this number to the red diagonal entry.
    This is the number of edges in the complete graph :math:`K_n`. Moreover, the
    vertex establishes :math:`m_1 \\cdot m_2` connections between blue and orange
    motifs. This is the number of edges in the complete bipartite graph :math:`K_{m_1,m_2}`
    and the vertex' contribution to the blue-orange off-diagonal entry.
    
    :param G: the SEN
    :param iterator: a :py:class:`sma.MotifIterator` as a source of motifs
    :param classificiator: a :py:class:`sma.MotifClassificator` for classifying 
        the motifs. Note that it must match with the given iterator.
    :param as_symmetric: per default the returned matrix is upper triangular. If
        this switch is set to ``True`` the returned matrix will be symmetrical, with
        the upper entries copied to the matrix' lower half.
    """
    ctable = cooccurrenceTableFull(G, iterator, classificator, to_array = True)
    choose2 = lambda n : n*(n-1)//2
    diag = numpy.diag(sum(choose2(ctable)))
    offdiag = numpy.array([[numpy.dot(ctable[:,i],ctable[:,j]) if i < j else 0 for j in range(classificator.classes)] for i in range(classificator.classes)])
    if as_symmetric:
        return offdiag + diag + numpy.transpose(offdiag)
    else:
        return offdiag + diag
 
def motifClassGraph(G : nx.Graph, 
                    iterator : sma.MotifIterator, 
                    classificator : sma.MotifClassificator) -> nx.Graph:
    """
    Returns an :py:class:`networkx.Graph` with one node for every motif class as 
    described by the given :py:class:`sma.MotifClassificator`. The edges are weighted
    by the entries of :py:meth:`sma.motifClassMatrix`. The graph contains loops.
    
    :param G: the SEN
    :param iterator: a :py:class:`sma.MotifIterator` as a source of motifs
    :param classificiator: a :py:class:`sma.MotifClassificator` for classifying 
        the motifs. Note that it must match with the given iterator.
    """
    graph = nx.from_numpy_array(motifClassMatrix(G, iterator, classificator, as_symmetric=True))
    return nx.relabel_nodes(graph, dict(zip(itertools.count(), classificator.names)), copy=True)

class _cooccurrenceEdgeTableFullMapper:
    def __init__(self, classificator, nodes_rows, nodes_columns, dyad):
        self.classificator = classificator
        self.indexer_rows    = {n : i for n, i in zip(nodes_rows, itertools.count())}
        self.indexer_columns = {n : i for n, i in zip(nodes_columns, itertools.count())}
        self.indexer_motifs  = {n : i for n, i in zip(classificator.names, itertools.count())}
        self.dyad = dyad
    def __call__(self, motif):
        cl = self.classificator(motif)
        return (self.indexer_rows[motif[self.dyad[0]]], 
                self.indexer_columns[motif[self.dyad[1]]], 
                self.indexer_motifs[cl])

def cooccurrenceEdgeTableFull(G : nx.Graph,
                              iterator : sma.MotifIterator,
                              classificator : sma.MotifClassificator,
                              dyad : tuple,
                              levels : tuple,
                              processes : int = 0,
                              chunksize : int = 10000):
    """
    Computes a cooccurrence table on edge level. Given an edge :math:`(v_1, v_2)`
    of a motif, :math:`v_1` in level :math:`i`, :math:`v_2` in level :math:`j`, this
    table consists of :math:`|V_i| \\times |V_j| \\times M` entries where :math:`V_i`,
    :math:`V_j` denotes the set of notes from level :math:`i`, resp. :math:`j` in
    the SEN and :math:`M` denotes the number of motif classes as classified by the
    given classificator. The :math:`(a,b,c)`th entry contains the number of times
    the edge :math:`(a,b)` occurs in a motif of type :math:`c`.
    
    The edge is specified using the ``dyad`` parameter. This parameter must contain
    a tuple of two integers specifying the index of the nodes spanning the edge in 
    the motifs provided by the iterator. For example, a typical 3E-motif looks like
    :math:`(e, s_1, s_2)` where :math:`s_1` and :math:`s_2` are social and :math:`e`
    is ecological. In this case, ``dyad = (1,2)`` would imply that the cooccurrence
    matrix for the edge :math:`(s_1, s_2)` would be computed. For technical reasons,
    a paramter ``levels`` must be provided. ``levels`` must be a tuple of length two
    specifying the ``sesType`` of the nodes in edge specified by ``dyad``. In the
    example, ``levels`` would be (:py:const:`sma.NODE_TYPE_SOC`,:py:const:`sma.NODE_TYPE_SOC`).
    
    Multiprocessing is supported. Use parameters ``processes`` and ``types``.
    
    **Example** Compute the cooccurrence table for 3S-motifs
    
    .. code :: Python 
    
        sma.cooccurrenceEdgeTableFull(G, 
                                      sma.ThreeSMotifs(G), 
                                      sma.ThreeMotifClassificator(G), 
                                      (1,2), # dyad, social nodes
                                      (0,0)) # levels, both social
    
    :param G: the SEN
    :param iterator: source of motifs
    :param classificator: classificator for the motifs
    :param dyad: specificiation of the esge for which the cooccurrence table is 
        computed (tuple of length 2)
    :param levels: ``sesTypes`` of the nodes in ``dyad`` (tuple of length 2)
    :param processes: number of processes for multiprocessing
    :param chunksize: chunksize for multiprocessing
    :returns: three values: the cooccurrence table, list of nodes as index for the rows,
        list of nodes as index for the columns
    """
    nodes_rows = list(sma.sesSubgraph(G, levels[0]))
    if levels[0] == levels[1]:
        nodes_columns = nodes_rows
    else:
        nodes_columns = list(sma.sesSubgraph(G, levels[0]))
    
    matrix = numpy.zeros((len(nodes_rows), len(nodes_columns), classificator.classes), dtype=int)
    mapper = _cooccurrenceEdgeTableFullMapper(classificator, nodes_rows, nodes_columns, dyad)
    
    if processes == 0:
        for index in map(mapper, iterator):
            matrix[index] +=1
            del index
    else:
        with multiprocessing.Pool(processes) as p:
            classified = p.imap_unordered(mapper, iterator, chunksize = chunksize)
            for index in classified:
                matrix[index] +=1
                del index
            p.close()
            p.join()
    
    if levels[0] == levels[1]:
        for i in range(classificator.classes):
            matrix[:,:,i] = numpy.triu(matrix[:,:,i] + matrix[:,:,i].T) - numpy.diag(numpy.diag(matrix[:,:,i]))
    
    return matrix, nodes_rows, nodes_columns
