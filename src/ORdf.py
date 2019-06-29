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

italia = rdflib.URIRef('http://www.example.org/countryItalia')
france = rdflib.URIRef('http://www.example.org/countryFrancia')
germania = rdflib.URIRef('http://www.example.org/countryGermania')
svezia = rdflib.URIRef('http://www.example.org/countrySvezia')

europa = rdflib.URIRef('http://www.example.org/countryRomania')
#asia = rdflib.URIRef('http://www.example.org/part2')

#g.add((germany,has_border_with,france))
#g.add((china,has_border_with,mongolia))
#g.add((germany,located_in,europa))
#g.add((france,located_in,europa))
#g.add((china,located_in,asia))
#g.add((mongolia,located_in,asia))

# --- fn ---- 
prop = URIRef('http://www.example.org/has_border_withP70')
g.add((svezia,prop,germania))

prop = URIRef('http://www.example.org/has_border_withP97')
g.add((italia,prop,france))




prop = URIRef('http://www.example.org/has_border_withP01')
g.add((italia,prop,germania))

prop = URIRef('http://www.example.org/has_border_withP40')
g.add((italia,prop,europa))

#q = "select ?country ?has_border_withP where { ?country ?has_border_withP <http://www.example.org/countryRomania> }"

#q = "select ?country ?country1 where { ?country <http://www.example.org/has_border_withP70> ?country1 }"

q = "select ?country ?has_border_withP ?country1 where { ?country ?has_border_withP ?country1 FILTER ( ?has_border_withP = <http://www.example.org/has_border_withP70>) }"

#q = "select ?country where { ?country <http://www.example.org/has_border_withP70> ?country }"

x = g.query(q)
print(list(x))



g.serialize(destination='country.txt', format='turtle')



'''
#enumerazione dell'intero grafo rdf [u,w,v]
for subject,predicate,obj in g:
    print(subject,predicate,obj)
'''

'''
#Tests di esistenza nodi e archi 
eu = rdflib.URIRef('Romania')
if((None,None,eu) in g):
    print("Romania is contained")

linked = rdflib.URIRef('http://www.example.org/has_border_withP40')
if((None,linked,None) in g):
    print("Exists Edge")
'''



'''
#Costruzione grafo di supporto all'RDF 
G = rdflib_to_networkx_multidigraph(g)
for u,v in G.edges():
    kw = G.get_edge_data(u,v).keys()
    pw = ""
    for w in kw:
        pw = w.split('P')[1]
        #print(pw)
        cento = int(pw) / 100
    G.edges[u, v, w]["pr"] = str(cento)
pos = nx.spring_layout(G)   
edge_labels = nx.get_edge_attributes(G,'pr')
#print(edge_labels)
nx.draw_networkx_edge_labels(G, pos, labels=edge_labels,
                                font_size=10, font_color='k', font_family='sans-serif',
                                font_weight='normal', alpha=2.0, bbox=None, ax=None, rotate=False)
nx.draw(G, pos=pos, with_labels=True, node_size=200,font_size=13) 
plt.title('Mondiali')
plt.show()
'''