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

import xml.etree.ElementTree as ET


entity = {}
to_node = []  #nodi univoci di to


'''
def graph_toRdf():
    root = ET.Element("rdf:RDF")
    doc = ET.SubElement(root, "rdf:Description")
    
    ET.SubElement(doc, "field1", name="blah").text = "some value1"
    ET.SubElement(doc, "field2", name="asdfasd").text = "some vlaue2"
    
    tree = ET.ElementTree(root)
    tree.write("serCustom.xml")
'''



#single target 
def entity_map(p,o,target):
    if(target in o):
        s = o.split('/')
        u = "" 
        for i in range(0,len(s)-1):
            u += s[i] + "/"
        #print(u)
        entity[p] = u


def filter(s,p,o):
    s = s.strip().replace("//","/").split('/')
    s = s[len(s)-1]
    p = p.strip().replace("//","/")
    p = re.split('~|#|/',p)
    p = p[len(p)-1]
    o = o.strip().replace("//","/")
    o = re.split('~|#|/',o)
    o = o[len(o)-1]
    return s,p,o


#calcola il numero dei film presenti per ogni genere e il numero totale de 
def frequency_nodes(network):
    count_node = 0
    for film in to_node:
        fre_film = 0 
        edj = network.in_edges(film)
        for e in edj:
            if(network.get_edge_data(e[0],e[1])[0]["attr"] == "titolo"):
                fre_film += 1
        node = film + "_freq"    
        network.add_node(node)
        network.add_edge(film,node,freq=fre_film)
        count_node += fre_film
    return count_node

def parseToGraph(g,_from,to,target=None): 
    dsub = {}
    to_list = {}
    
    network = nx.MultiDiGraph()  

    for s,p,o in g: #da pdm lo so 
        s,pr,_o = filter(s,p,o)
        #entity_map(pr,o,"imdb")
        if(pr in to): #predicati 
            if(_o not in network.nodes()):
                network.add_node(_o) # generi univoci nel grafo 
                to_node.append(_o)
            to_list[s] = _o  #i soggetti con i relativi generi 
    #print(to_node)
    
    for s,p,o in g:
        s,p,o = filter(s,p,o)

        if(s in dsub.keys()):
            if(p in dsub[s].keys()): 
                #predicato gia inserito 
                if(type(dsub[s][p])  is list):
                    dsub[s][p].append(o)
                else:
                    tmp = dsub[s][p]
                    del dsub[s][p]
                    dsub[s][p] = []
                    dsub[s][p].append(tmp)
                    dsub[s][p].append(o)
            else:
                #predicato sconosciuto 
                dsub[s][p] = o
        else:
            dsub[s] = {}
            dsub[s][p] = o
        
        #graph 
        if(p in _from):
            if(o not in network.nodes()):
                network.add_node(o)
            to_item = to_list[s]
            if(network.has_edge(o,to_item)):
                w = network.get_edge_data(o,to_item)
                w = w[0]["weight"] 
                network[o][to_item][0]["weight"] = w + 1
                #print(network.get_edge_data(o,to_item))
            else:
                network.add_edge(o,to_item,attr=p,weight=1)    
        
    '''
    network.add_edge("Pixar","hoodie",weight=21)
    network.add_edge("Pixar","buzz",weight=94)
    print(network["Pixar"])
    '''

    '''
    for u,v in network.edges():
        try:
            print(u,v)
            print(network.get_edge_data(u,v))
        except:
            print(u,v)
    '''
    print("\n\n")
    #print(network["nm0002071"]) #nm0002071
    #print(network["hoodie"]) 

    #print(len(network.nodes()))
    return network
    




film = rdflib.URIRef('http://www.example.org/tt001')

film1 = rdflib.URIRef('http://www.example.org/tt002')

film2 = rdflib.URIRef('http://www.example.org/tt003')


#entita 
attore = rdflib.URIRef('http://www.example.org/attore')
genere = rdflib.URIRef('http://www.example.org/genere')
direttore = rdflib.URIRef('http://www.example.org/direttore')
autore = rdflib.URIRef('http://www.example.org/autore')
titolo = rdflib.URIRef('http://www.example.org/titolo') 

g = ConjunctiveGraph()
#g.parse("/home/phinkie/Scrivania/turbo-watchdogs/ontologie/film.xml", format="xml")
#G = parseToGraph(g,["actor","director","author"],["genre"])
#decoder(g)


#info generali 
g.add((film,FOAF.age,Literal(1997)))
g.add((film,FOAF.name,Literal("toy story")))

#info film
g.add((film,attore,Literal("http://www.imdb.com/name/hoodie")))
g.add((film,attore,Literal("http://www.imdb.com/name/buzz")))
g.add((film,genere,Literal("http://www.imdb.com/genr/Cartoon")))
g.add((film,titolo,Literal("http://www.imdb.com/title/ToyStory")))
g.add((film,direttore,Literal("http://www.imdb.com/company/disney")))
g.add((film,autore,Literal("http://www.imdb.com/name/Pixar")))
g.add((film,titolo,Literal("http://www.imdb.com/title/ToyStory")))


g.add((film1,direttore,Literal("http://www.imdb.com/company/disney")))
g.add((film1,genere,Literal("http://www.imdb.com/genr/Cartoon")))
g.add((film1,attore,Literal("http://www.imdb.com/company/hoodie")))
g.add((film1,titolo,Literal("http://www.imdb.com/title/Toy2")))


g.add((film2,direttore,Literal("http://www.imdb.com/company/RoccoAccademy")))
g.add((film2,genere,Literal("http://www.imdb.com/genr/Porno")))
g.add((film2,attore,Literal("http://www.imdb.com/name/hoodie")))
g.add((film2,titolo,Literal("http://www.imdb.com/title/HoodieFuckEveryone")))

G = parseToGraph(g,["titolo","attore","direttore","autore"],["genere"])
frequency_nodes(G)
 

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


#print(entity)

