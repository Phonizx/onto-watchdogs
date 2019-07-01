import rdflib 
from rdflib import Graph, Literal, BNode, Namespace, RDF, URIRef
from rdflib.namespace import DC, FOAF

from rdflib.extras.external_graph_libs import rdflib_to_networkx_multidigraph
import networkx as nx
import matplotlib.pyplot as plt
from rdflib.collection import Collection
from rdflib import ConjunctiveGraph, URIRef, RDFS
from rdflib.namespace import XSD

import re 




def pKTM(g):
    dsub = {}
    for s,p,o in g:
        s = s.strip().replace("//","/").split('/')
        sub = s[len(s)-1]

        p = p.strip().replace("//","/")
        p = re.split('~|#|/',p)
        pre = p[len(p)-1]
        o = o.strip()  

       # print(sub,pre,o)#print 
        if(sub  in dsub.keys()):
            if(pre in dsub[sub].keys()): #bug
                if(type(dsub[sub][pre])  is list):
                    dsub[sub][pre].append(o)
                else:
                    tmp = dsub[sub][pre]
                    del dsub[sub][pre]
                    dsub[sub][pre] = []
                    dsub[sub][pre].append(tmp)
                    dsub[sub][pre].append(o)
            else:
                dsub[sub][pre] = o
        else:
            dsub[sub] = {}
            dsub[sub][pre] = o
    print(dsub)
     

italia = rdflib.URIRef('http://www.example.org/cItalia')
pr = rdflib.URIRef('http://www.example.org/~attr_prob')

id = rdflib.URIRef('http://www.example.org/unique_id')


g = Graph()
#g.parse("/home/phinkie/Scrivania/turbo-watchdogs/src/film.xml", format="xml")

#g.add((italia,FOAF.age,Literal(21)))
g.add((italia,FOAF.age,Literal(1)))
g.add((italia,FOAF.name,Literal("gaston")))
g.add((italia,FOAF.name,Literal("juan")))
g.add((id,"http://www.example.org/attr_prob",Literal(0.90)))
 
 

pKTM(g)


'''
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


q = "select  ?v where { ?c <http://www.example.org/attr_prob> ?unique_id . \
    ?unique_id <http://www.w3.org/1999/02/22-rdf-syntax-ns#value> ?v \
    FILTER(?v <= 10) }"

x = g.query(q)
print(list(x))
'''



'''
class point():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def data(self):
        print(self.x,self.y)
        
import networkx as nx
G = nx.Graph()
p0 = point(0,0)
p1 = point(1,1)

G.add_node(0,data=p0)
G.add_node(1,data=p1)
G.add_edge(0,1,weight=4)
G.add_edge(0,1,name="stringa as weighted")

print(G.node[1]["data"].data())


'''