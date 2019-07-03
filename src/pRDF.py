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

entity = {}
to_node = []  #nodi univoci di to

'''
import xml.etree.ElementTree as ET
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
    for u,v in network.edges():
        try:
            print(u, v)
            print(network.get_edge_data(u, v))
        except:
            print(u,v)
    ''' 
    #print(network["nm0002071"]) #nm0002071
    #print(network["hoodie"]) 

    #print(len(network.nodes()))
    return network
    
film1 = rdflib.URIRef('http://www.example.org/tt001')
film2 = rdflib.URIRef('http://www.example.org/tt002')
film3 = rdflib.URIRef('http://www.example.org/tt003')

attore = rdflib.URIRef('http://www.example.org/attore')
genere = rdflib.URIRef('http://www.example.org/genere')
direttore = rdflib.URIRef('http://www.example.org/direttore')
autore = rdflib.URIRef('http://www.example.org/autore')
titolo = rdflib.URIRef('http://www.example.org/titolo') 

g = ConjunctiveGraph()
'''
#path = "/home/phinkie/Scrivania/turbo-watchdogs/"
path =  "../"

g.parse(path+"ontologie/film.xml", format="xml")
G = parseToGraph(g,["actor","director","author"],["genre"])
'''
#info generali TT001
g.add((film1, FOAF.age, Literal(1997)))
g.add((film1, FOAF.name, Literal("TOY_STORY")))

g.add((film1, attore, Literal("HOODIE")))
g.add((film1, attore, Literal("BUZZ")))
g.add((film1, genere, Literal("CARTOON")))
g.add((film1, direttore, Literal("DISNEY")))
g.add((film1, autore, Literal("PIXAR")))
g.add((film1, titolo, Literal("TOY_STORY")))

#info generali TT002
g.add((film2, FOAF.age, Literal(1999)))
g.add((film2, FOAF.name, Literal("TOY_STORY2")))

g.add((film2, direttore, Literal("DISNEY")))
g.add((film2, genere, Literal("CARTOON")))
g.add((film2, attore, Literal("HOODIE")))
g.add((film2, autore, Literal("ROCCO")))
g.add((film2, titolo, Literal("TOY_STORY2")))
""" 
g.add((film2,direttore,Literal("http://www.imdb.com/company/RoccoAccademy")))
g.add((film2,genere,Literal("http://www.imdb.com/genr/Porno")))
g.add((film2,attore,Literal("http://www.imdb.com/name/hoodie")))
g.add((film2,titolo,Literal("http://www.imdb.com/title/HoodieFuckEveryone"))) """

#info generali TT002
g.add((film3, FOAF.age, Literal(2010)))
g.add((film3, FOAF.name, Literal("DILDO_STORY")))

g.add((film3, direttore, Literal("ROCCOACCADEMY")))
g.add((film3, genere, Literal("PORNO")))
g.add((film3, attore, Literal("HOODIE")))
g.add((film3, autore, Literal("ROCCO")))
g.add((film3, titolo, Literal("DILDO_STORY")))

g_parsed = parseToGraph(g, ["titolo","direttore","attore","autore"],["genere"])
tot_freq = frequency_nodes(g_parsed)
print(g_parsed.nodes()) 

#TODO: utilizzare in_degree di networkx
def numOutDegree(graph, node, to=None):
    weight = "weight" 
    n = graph[node]
    outdegree = 0 
    if to==None:        
        for films in n:
            attrdict = graph.get_edge_data(node, films) 
            for attrs in attrdict:
                outdegree += attrdict[attrs][weight] 
    else:
        attrdict = graph.get_edge_data(node, to) 
        if attrdict == None:
            outdegree = 0
        else:
            for attrs in attrdict:
                outdegree += attrdict[attrs][weight]    
    return outdegree

def probability_condition(graph, node, to): #P (A  | B)
    if isinstance(node, list):
        if len(node)>1:
            p = numOutDegree(graph, node[0], to) / numOutDegree(graph, node[0]) * \
             probability_condition(graph,node[1:],to)
            return p
        else:
            if len(node)==1:
                p = probability_condition(graph, node[0], to) 
                return p
    else:
        p = numOutDegree(graph, node, to) / numOutDegree(graph, node) 
        return p

def probability_priori(graph, B, N):
    if N>0:
        return graph.get_edge_data(B,B+"_freq")[0]["freq"]/N
    else:
        print("N = 0!")
        return -1

def probability_FPT(graph, Bs, N):
    P_B = 0
    for node in Bs:
        pr = probability_priori(graph, "CARTOON", N)
        P_B +=probability_condition(graph, node, "CARTOON") * pr

        pr = probability_priori(graph, "PORNO", N)
        P_B +=probability_condition(graph, node, "PORNO") * pr
    return  P_B
    """ for B in Bs:
        for node in graph.nodes():
            if not(node in {"CARTOON", "PORNO"}):
                P_B +=  probability_condition(graph, node, B) * probability_priori(graph, B)
  
    return P_B
    """
def bayes_calc(graph, cause, effects, tot_freq):
    p_FPT = probability_FPT(graph, effects, tot_freq)
    if p_FPT == 0:
        return 0
    else:
        return (probability_condition(graph, effects, cause) * probability_priori(graph, cause, tot_freq)) \
        /p_FPT


#print(probability_condition( g_parsed, "DISNEY", "CARTOON"))
print("thBayes : "+ str(1-bayes_calc(g_parsed, "CARTOON", ["HOODIE","ROCCO","BUZZ"], tot_freq)))
s = " "
'''
while(not(s == "esci")):
    try:
        s = input("inserire nodo:")
        s = s.upper()
        print("OutDegree : "+ str(numOutDegree(g_parsed, s)))
        print("Pr : "+ str(probability_condition(g_parsed,[s,"BUZZ"], "CARTOON")))
        #print(g_parsed[s])
    except:
        print("exit",end="")
        break
     
'''
 
""" 
#G = parseToGraph(g,["direttore","attore","autore"],["genere"])
edge_labels = []
pos = nx.spring_layout(g_parsed)   
#edge_labels = nx.get_edge_attributes(G,'pr')
#print(edge_labels)
nx.draw_networkx_edge_labels(g_parsed, pos, labels=edge_labels,
                                font_size=10, font_color='k', font_family='sans-serif',
                                font_weight='normal', alpha=2.0, bbox=None, ax=None, rotate=False)
nx.draw(g_parsed, pos=pos, with_labels=True, node_size=200,font_size=13) 

plt.show()  """