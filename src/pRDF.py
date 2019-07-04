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
#utilizzato in prob_FPT
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
    print("COUNTING NODES GENRE")
    titolo ="label" #"titolo"
    count_node = 0
    for film in to_node:
        fre_film = 0 
        edj = network.in_edges(film)
        for e in edj:
            if(network.get_edge_data(e[0],e[1])[0]["attr"] == titolo):
                fre_film += 1
        node = film + "_freq"    
        network.add_node(node)
        network.add_edge(film,node,freq=fre_film)
        count_node += fre_film
    return count_node

def parseToGraph(g,_from,to,target=None): 
    print("PARSING TO GRAPH")
    dsub = {}
    to_list = {}
    
    network = nx.MultiDiGraph()  

    for s,p,o in g: #da pdm lo so         
        print("s: "+str(s)+" p: "+str(p)+" o: "+str(o))
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
        print("CREATING GRAPH")
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
#path = "/home/phinkie/Scrivania/turbo-watchdogs/"
path =  "../"

g.parse(path+"ontologie/film.xml", format="xml")
g_parsed = parseToGraph(g,["actor","label","director","author"],["genre"])
"""
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

#info generali TT002
g.add((film3, FOAF.age, Literal(2010)))
g.add((film3, FOAF.name, Literal("DILDO_STORY")))

g.add((film3, direttore, Literal("ROCCOACCADEMY")))
g.add((film3, genere, Literal("PORNO")))
g.add((film3, attore, Literal("HOODIE")))
g.add((film3, autore, Literal("ROCCO")))
g.add((film3, titolo, Literal("DILDO_STORY")))

g_parsed = parseToGraph(g, ["titolo","direttore","attore","autore"],["genere"])
"""
tot_freq = frequency_nodes(g_parsed)
'''
with open("NODE.txt","w") as f:
    f.write(str(g_parsed.nodes()))
f.close()
'''
#TODO: utilizzare in_degree di networkx
def numOutDegree(graph, node, to=None):
    weight = "weight"
    n = graph[node]
    outdegree = 0
    if to == None:
        out_edges = list(graph.out_edges(node, data=True))
        for out_edge in out_edges:        
            outdegree += out_edge[2][weight]
        """ for films in n:
            attrdict = graph.get_edge_data(node, films) 
            for attrs in attrdict:
                outdegree += attrdict[attrs][weight] 
        """ 
    else:        
        out_edges = list(graph.out_edges(node, data=True))        
        for out_edge in out_edges: 
            if out_edge[1] == to:
                outdegree += out_edge[2][weight]
        """ attrdict = graph.get_edge_data(node, to) 
        if attrdict == None:
            outdegree = 0
        else:
            for attrs in attrdict:
                outdegree += attrdict[attrs][weight]   
        """  
    return outdegree

def conditional_probability(graph, node, to): #P (A  | B)
    if isinstance(node, list):
        if len(node)>1:
            p = numOutDegree(graph, node[0], to) / numOutDegree(graph, node[0]) * \
             conditional_probability(graph,node[1:],to)
            return p
        else:
            if len(node)==1:
                p = conditional_probability(graph, node[0], to) 
                return p
    else:
        p = numOutDegree(graph, node, to) / numOutDegree(graph, node) 
        return p

def probability_priori(graph, B, N):
    if N>0:
        return graph.get_edge_data(B, B+"_freq")[0]["freq"]/N
    else:
        print("N = 0!")
        return -1

def probability_FPT(graph, Bs, N):
    P_B = 0
    for priori in to_node:
        pr = probability_priori(graph, priori, N)
        # Calcola la prob condizionata e congiuta dei nodi Bs
        pc = conditional_probability(graph, Bs, priori)
        P_B += pc * pr
    return  P_B

def bayes_calc(graph, cause, effects, tot_freq):
    p_FPT = probability_FPT(graph, effects, tot_freq)
    if p_FPT <= 0:
        return 0
    else:
        p_A_B = conditional_probability(graph, effects, cause)
        pr = probability_priori(graph, cause, tot_freq)
        return (p_A_B * pr) / p_FPT

conds = " " 
while(not(conds == "esci")):
    try:
        conds = input("inserire uno o piu nodi separta da ',': ")
        conds = conds.replace(" ","")
        conds = conds.split(',')
        gen = input("inserire un genere: ")
        #gen = gen.upper()
        print("Pr: "+ str(conditional_probability(g_parsed, conds, gen)))        
        print("thBayes: "+ str(bayes_calc(g_parsed, gen, conds , tot_freq)))
        #print(g_parsed[s])
        conds=" "
    except:
        print("exit",end="")
        break
 
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