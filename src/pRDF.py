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



# add predicato-obj transitivo  
def parseToGraph(g,_from,to): 
    dsub = {}
    to_list = []

    network = nx.MultiDiGraph()  


    for s,p,o in g: #da pdm lo so 
        p = p.strip().replace("//","/")
        p = re.split('~|#|/',p)
        pre = p[len(p)-1]
        o = o.strip().replace("//","/")
        o = re.split('~|#|/',o)
        o = o[len(o)-1]
        if(pre in to): #predicati 
            if(o not in network.nodes()):
                network.add_node(o)
                to_list.append(o) 
    
    for s,p,o in g:
        s = s.strip().replace("//","/").split('/')
        sub = s[len(s)-1]
        
        p = p.strip().replace("//","/")
        p = re.split('~|#|/',p)
        pre = p[len(p)-1]
        o = o.strip().replace("//","/")
        o = re.split('~|#|/',o)
        o = o[len(o)-1]
        
        #print(sub,pre,o)

        if(sub  in dsub.keys()):
            if(pre in dsub[sub].keys()): 
                #predicato gia inserito 
                if(type(dsub[sub][pre])  is list):
                    dsub[sub][pre].append(o)
                else:
                    tmp = dsub[sub][pre]
                    del dsub[sub][pre]
                    dsub[sub][pre] = []
                    dsub[sub][pre].append(tmp)
                    dsub[sub][pre].append(o)
            else:
                #predicato sconosciuto 
                dsub[sub][pre] = o
        else:
            dsub[sub] = {}
            dsub[sub][pre] = o
        #graph 
        if(pre in _from):
            if(o not in network.nodes()):
                network.add_node(o)
            for to_item in to_list:
                if(network.has_edge(o,to_item)):
                    w = network.get_edge_data(o,to_item)
                    w = w[0]["weight"] 
                    network[o][to_item][0]["weight"] = w + 1
                    #print(network.get_edge_data(o,to_item))
                else:
                    network.add_edge(o,to_item,attr=pre,weight=1)    
    '''
    network.add_edge("Pixar","hoodie",weight=21)
    network.add_edge("Pixar","buzz",weight=94)
    print(network["Pixar"])
    '''

    
    for u,v in network.edges():
        try:
            print(u,v)
            print(network.get_edge_data(u,v))
        except:
            print(u,v)
    
    #print(dsub)
    

film = rdflib.URIRef('http://www.example.org/tt001')

film1 = rdflib.URIRef('http://www.example.org/tt002')


pr = rdflib.URIRef('http://www.example.org/~attr_prob')
id = rdflib.URIRef('http://www.example.org/unique_id')

attore = rdflib.URIRef('http://www.example.org/attore')
genere = rdflib.URIRef('http://www.example.org/genere')
direttore = rdflib.URIRef('http://www.example.org/direttore')
autore = rdflib.URIRef('http://www.example.org/autore')

g = ConjunctiveGraph()
#g.parse("/home/phinkie/Scrivania/turbo-watchdogs/src/film.xml", format="xml")


#info generali 
g.add((film,FOAF.age,Literal(1997)))
g.add((film,FOAF.name,Literal("toy story")))

#info film
g.add((film,attore,Literal("hoodie")))
g.add((film,attore,Literal("buzz")))
g.add((film,genere,Literal("Cartoon")))

g.add((film,direttore,Literal("disney")))
g.add((film,autore,Literal("Pixar")))


g.add((film1,direttore,Literal("disney")))
g.add((film1,genere,Literal("Cartoon")))
#g.add((id,FOAF.age,Literal(0.90)))

'''
g.add((italia,pr,id))
g.add((id,RDF.value,Literal(9.0)))
'''
parseToGraph(g,["direttore","attore","autore"],["genere"])
 

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
p0 = point(2,3)
p1 = point(4,6)

G.add_node(0,data=p0)
G.add_node(1,data=p1)
G.add_edge(0,1,weight=4)
G.add_edge(0,1,name="stringa as weighted")

for e in G.edges:
    print(G.node[e[0]]["data"].data(),G.node[e[1]]["data"].data())





def parseToGraph(g,_from,to): 
    dsub = {}
    network = nx.MultiDiGraph()  
    i = 1 
    for s,p,o in g:
        s = s.strip().replace("//","/").split('/')
        sub = s[len(s)-1]
        
        p = p.strip().replace("//","/")
        p = re.split('~|#|/',p)
        pre = p[len(p)-1]
        o = o.strip().replace("//","/")
        o = re.split('~|#|/',o)
        o = o[len(o)-1]
        #print(sub,pre,o)

        if(sub  in dsub.keys()):
            if(pre in dsub[sub].keys()): 
                #predicato gia inserito 
                if(type(dsub[sub][pre])  is list):
                    dsub[sub][pre].append(o)
                else:
                    tmp = dsub[sub][pre]
                    del dsub[sub][pre]
                    dsub[sub][pre] = []
                    dsub[sub][pre].append(tmp)
                    dsub[sub][pre].append(o)
            else:
                #predicato sconosciuto 
                dsub[sub][pre] = o
        else:
            dsub[sub] = {}
            dsub[sub][pre] = o
        if(pre in _from):
            network.add_node(o)
            #i = i + 1 
        if(pre in to):
            network.add_node(0,data=o)
   
    for node in network.nodes():
        if(node != 0):
            network.add_edge(node,0,weight=2)
   
    
    network.add_edge("Pixar","hoodie",weight=21)
    network.add_edge("Pixar","buzz",weight=94)
    print(network["Pixar"])
    for u,v in network.edges():
        try:
            print(u,network.node[v]["data"])
        except:
            print(u,v)

'''