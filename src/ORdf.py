import rdflib 
from rdflib import Graph, Literal, BNode, Namespace, RDF, URIRef
from rdflib.namespace import DC, FOAF

from rdflib.extras.external_graph_libs import rdflib_to_networkx_multidigraph
import networkx as nx
import matplotlib.pyplot as plt
from rdflib.collection import Collection
from rdflib import ConjunctiveGraph, URIRef, RDFS



g = Graph()

prop = URIRef('http://www.example.org/has_border_withP99')


has_border_with = rdflib.URIRef('http://www.example.org/has_border_with')
located_in = rdflib.URIRef('http://www.example.org/located_in')

germany = rdflib.URIRef('germany')
france = rdflib.URIRef('france')
china = rdflib.URIRef('china')
mongolia = rdflib.URIRef('mongolia')

europa = rdflib.URIRef('http://www.example.org/part1')
asia = rdflib.URIRef('http://www.example.org/part2')

#g.add((germany,has_border_with,france))
#g.add((china,has_border_with,mongolia))
#g.add((germany,located_in,europa))
#g.add((france,located_in,europa))
#g.add((china,located_in,asia))
#g.add((mongolia,located_in,asia))

# --- fn ---- 
prop = URIRef('http://www.example.org/has_border_withP11')
g.add((mongolia,prop,china))

prop = URIRef('http://www.example.org/has_border_withP97')
g.add((germany,prop,france))




prop = URIRef('http://www.example.org/has_border_withP01')
g.add((germany,prop,china))
#q = "select ?country where { ?country <http://www.example.org/located_in> <http://www.example.org/part2> }"
#x = g.query(q)
#print(list(x))

g.serialize(destination='country.xml', format='xml')



G = rdflib_to_networkx_multidigraph(g)
for u,v in G.edges():
    kw = G.get_edge_data(u,v).keys()
    pw = ""
    for w in kw:
        pw = w.split('P')[1]
        #print(pw)
    G.edges[u, v, w]["pr"] = pw
pos = nx.spring_layout(G)   
edge_labels = nx.get_edge_attributes(G,'pr')
#print(edge_labels)
nx.draw_networkx_edge_labels(G, pos, labels=edge_labels,
                                font_size=10, font_color='k', font_family='sans-serif',
                                font_weight='normal', alpha=2.0, bbox=None, ax=None, rotate=True)
nx.draw(G, pos=pos, with_labels=True, node_size=700) 
plt.show()

