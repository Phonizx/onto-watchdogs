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
    to_list = {}

    network = nx.MultiDiGraph()  


    for s,p,o in g: #da pdm lo so 
        s = s.strip().replace("//","/").split('/')
        sub = s[len(s)-1]
        p = p.strip().replace("//","/")
        p = re.split('~|#|/',p)
        pre = p[len(p)-1]
        o = o.strip().replace("//","/")
        o = re.split('~|#|/',o)
        o = o[len(o)-1]
        if(pre in to): #predicati 
            if(o not in network.nodes()):
                network.add_node(o) # generi univoci nel grafo 
            to_list[sub] = o  #i soggetti con i relativi generi 

    for s,p,o in g:
        s = s.strip().replace("//","/").split('/')
        sub = s[len(s)-1]
        
        p = p.strip().replace("//","/")
        p = re.split('~|#|/',p)
        pre = p[len(p)-1]
        o = o.strip().replace("//","/")
        o = re.split('~|#|/',o)
        o = o[len(o)-1]
        
        print(sub,pre,o)

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
            to_item = to_list[sub]
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
    print("\n\n\n\n\n\n\n\n")
    print(network["nm0002071"]) #nm0002071
    return network
    

film = rdflib.URIRef('http://www.example.org/tt001')

film1 = rdflib.URIRef('http://www.example.org/tt002')

film2 = rdflib.URIRef('http://www.example.org/tt003')


pr = rdflib.URIRef('http://www.example.org/~attr_prob')
id = rdflib.URIRef('http://www.example.org/unique_id')

attore = rdflib.URIRef('http://www.example.org/attore')
genere = rdflib.URIRef('http://www.example.org/genere')
direttore = rdflib.URIRef('http://www.example.org/direttore')
autore = rdflib.URIRef('http://www.example.org/autore')

g = ConjunctiveGraph()
g.parse("/home/phinkie/Scrivania/turbo-watchdogs/ontologie/film.xml", format="xml")
G = parseToGraph(g,["actor","director","author"],["genre"])
'''
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
g.add((film1,attore,Literal("hoodie")))


g.add((film2,direttore,Literal("RoccoAccademy")))
g.add((film2,genere,Literal("Porno")))
g.add((film2,attore,Literal("hoodie")))

#g.add((id,FOAF.age,Literal(0.90)))


g.add((italia,pr,id))
g.add((id,RDF.value,Literal(9.0)))
'''

'''
#G = parseToGraph(g,["direttore","attore","autore"],["genere"])
edge_labels = []
pos = nx.spring_layout(G)   
#edge_labels = nx.get_edge_attributes(G,'pr')
#print(edge_labels)
nx.draw_networkx_edge_labels(G, pos, labels=edge_labels,
                                font_size=10, font_color='k', font_family='sans-serif',
                                font_weight='normal', alpha=2.0, bbox=None, ax=None, rotate=False)
nx.draw(G, pos=pos, with_labels=True, node_size=200,font_size=13) 

plt.show()

'''