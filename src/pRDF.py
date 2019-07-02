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
        
        print(sub, pre, o)

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
            if(network.has_edge(o, to_item)):
                w = network.get_edge_data(o, to_item)
                w = w[0]["weight"] 
                network[o][to_item][0]["weight"] = w + 1
                #print(network.get_edge_data(o,to_item))
            else:
                network.add_edge(o, to_item, attr=pre, weight=1)
    
    for u, v in network.edges():
        try:
            print(u, v)
            print(network.get_edge_data(u, v))
        except:
            print(u, v)
    #print("************")
    #print(network["nm0002071"]) #nm0002071
    return network
  
   
film1 = rdflib.URIRef('http://www.example.org/tt001')

film2 = rdflib.URIRef('http://www.example.org/tt002')

film3 = rdflib.URIRef('http://www.example.org/tt003')

attore = rdflib.URIRef('http://www.example.org/attore')
genere = rdflib.URIRef('http://www.example.org/genere')
direttore = rdflib.URIRef('http://www.example.org/direttore')
autore = rdflib.URIRef('http://www.example.org/autore')

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

#info film
g.add((film1, attore, Literal("HOODIE")))
g.add((film1, attore, Literal("BUZZ")))
g.add((film1, genere, Literal("CARTOON")))

g.add((film1, direttore, Literal("DISNEY")))
g.add((film1, autore, Literal("PIXAR")))

#info generali TT002
g.add((film2, FOAF.age, Literal(1999)))
g.add((film2, FOAF.name, Literal("TOY_STORY2")))

g.add((film2, direttore, Literal("DISNEY")))
g.add((film2, genere, Literal("CARTOON")))
g.add((film2, attore, Literal("HOODIE")))
g.add((film2, autore, Literal("ROCCO")))

#info generali TT002
g.add((film3, FOAF.age, Literal(2010)))
g.add((film3, FOAF.name, Literal("DILDO_STORY")))

g.add((film3, direttore, Literal("ROCCOACCADEMY")))
g.add((film3, genere, Literal("PORNO")))
g.add((film3, attore, Literal("HOODIE")))
g.add((film3, autore, Literal("ROCCO")))


g_parsed = parseToGraph(g, ["direttore","attore","autore"],["genere"])


def numOutDegree(graph, node, to=None):
    #TODO: utilizzare in_degree di networkx
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
#g_parsed

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
                return 1
        return 1
    else:
        p = numOutDegree(graph, node, to) / numOutDegree(graph, node)
        return p

def probability_priori(graph, B, N=3):

    if B == "CARTOON":
        return 2/3
    if B == "PORNO":
        return 1/3


    p = numOutDegree(graph, B) / N
    print("propriori: "+str(p))
    return p


def probability_FPT(graph, Bs, N=3):
    P_B = 0
    for node in Bs:
        P_B +=probability_condition(graph, node, "CARTOON") * probability_priori(graph, "CARTOON")
        P_B +=probability_condition(graph, node, "PORNO") * probability_priori(graph, "PORNO")
    return  P_B
    for B in Bs:
        for node in graph.nodes():
            if not(node in {"CARTOON", "PORNO"}):
                P_B +=  probability_condition(graph, node, B) * probability_priori(graph, B)
  
    return P_B
def bayes_calc(graph, cause, effects):
    p_FPT = probability_FPT(graph, effects)
    if p_FPT == 0:
        return 0
    else:
        return (probability_condition(graph, effects, cause) * probability_priori(graph, cause)) \
        /p_FPT






#print(probability_condition( g_parsed, "DISNEY", "CARTOON"))
print("thBayes : "+ str(bayes_calc(g_parsed, "DISNEY", ["ROCCO","HOODIE"])))
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
