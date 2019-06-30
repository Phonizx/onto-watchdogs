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



def parser(g):
    
    sbj = {} #dizionario soggetti 
    
    f = True 
    s = ""  
    for subject,predicate,obj in g:
        if(f == True):
            s = subject
            f = False
       # print(subject,predicate,obj)
        if(subject in sbj):
            sbj[subject][predicate] = obj
        else:
             sbj[subject] = {} 
        #if(subject in sbj):
    print(sbj[s])
    print(s)


def parseToGraph(g):
    dict_attr = {}
    sbj_list = set()

    for subject,predicate,obj in g:
        p = re.split('~|#',predicate)
        p = p[1]
        #print(dict_attr)
        if(subject in dict_attr):
            dict_attr[dict_attr.get(subject)] = obj.value
            sbj_list.add(subject)
        if("attr" in p):
            p = p.split('_')[1]
            dict_attr[obj] = p
        
        #print(subject,p,obj)
        #input()
    for s in sbj_list: #warning 
        del dict_attr[s]
    print(dict_attr)


italia = rdflib.URIRef('http://www.example.org/cItalia')
pr = rdflib.URIRef('http://www.example.org/~attr_prob')

id = rdflib.URIRef('http://www.example.org/unique_id')


g = Graph()
g.parse("/home/phinkie/Scrivania/turbo-watchdogs/src/film.xml", format="xml")
'''
g.add((italia,pr,id))
g.add((italia,FOAF.name,Literal("juan")))
g.add((id,RDF.value,Literal(0.90)))
'''
#parseToGraph(g)
parser(g)




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