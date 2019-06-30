import rdflib 
from rdflib import Graph, Literal, BNode, Namespace, RDF, URIRef
from rdflib.namespace import DC, FOAF

from rdflib.extras.external_graph_libs import rdflib_to_networkx_multidigraph
import networkx as nx
import matplotlib.pyplot as plt
from rdflib.collection import Collection
from rdflib import ConjunctiveGraph, URIRef, RDFS
from rdflib.namespace import XSD



italia = rdflib.URIRef('http://www.example.org/cItalia')
pr = rdflib.URIRef('http://www.example.org/has_prob')

id = rdflib.URIRef('http://www.example.org/unique_id')


g = Graph()

g.add((italia,pr,id))
g.add((id,RDF.value,Literal(1)))

for subject,predicate,obj in g:
    print(subject,predicate,obj)


edge_labels = [] 
G = rdflib_to_networkx_multidigraph(g)
pos = nx.spring_layout(G)   
#edge_labels = nx.get_edge_attributes(G,'pr')
#print(edge_labels)
nx.draw_networkx_edge_labels(G, pos, labels=edge_labels,
                                font_size=10, font_color='k', font_family='sans-serif',
                                font_weight='normal', alpha=2.0, bbox=None, ax=None, rotate=False)
nx.draw(G, pos=pos, with_labels=True, node_size=200,font_size=13) 
plt.show()


q = "select  ?v where { ?c <http://www.example.org/has_prob> ?unique_id . ?unique_id <http://www.w3.org/1999/02/22-rdf-syntax-ns#value> ?v FILTER(?v <= 10) }"

x = g.query(q)
print(list(x))