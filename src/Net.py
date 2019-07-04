import rdflib 
from rdflib import Graph, Literal, BNode, Namespace, RDF, URIRef
from rdflib.namespace import DC, FOAF

from rdflib.extras.external_graph_libs import rdflib_to_networkx_multidigraph
import networkx as nx
import matplotlib.pyplot as plt
from rdflib.collection import Collection
from rdflib import ConjunctiveGraph, URIRef, RDFS
import re 



class Net:
    
    def __init__(self,_from,to):
        self.network = nx.MultiDiGraph() 
        self.dsub = {}
        self.to_list = {}
        self.to_node = [] 
        self.g = self.load_rdf()
        self.parseToGraph(self.g,_from,to)
        self.frequency_nodes("titolo") #identificativo entity 

    def load_rdf(self):        
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

        #g.parse(path+"ontologie/film.xml", format="xml")
        #g_parsed = parseToGraph(g,["actor","label","director","author"],["genre"])

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
        return g

    def get_ToNode(self):
        return self.to_node
    

    def get_network(self):
        return self.network

    
    def filter(self,s,p,o):
        s = s.strip().replace("//","/").split('/')
        s = s[len(s)-1]
        p = p.strip().replace("//","/")
        p = re.split('~|#|/',p)
        p = p[len(p)-1]
        o = o.strip().replace("//","/")
        o = re.split('~|#|/',o)
        o = o[len(o)-1]
        return s,p,o
    
    
    def parse_subject(self,g,to):
        for s,p,o in g: #da pdm lo so         
            s,pr,_o = self.filter(s,p,o)
            #entity_map(pr,o,"imdb")
            if(pr in to): #predicati 
                if(_o not in self.network.nodes()):
                    self.network.add_node(_o) # generi univoci nel grafo 
                    self.to_node.append(_o)
                self.to_list[s] = _o  

    
    def parseToGraph(self,g,_from,to,target=None): 
        g = self.g

        self.parse_subject(g,to) #parsing dei singoli nodi To
       
        for s,p,o in g:
            s,p,o = self.filter(s,p,o)

            if(s in self.dsub.keys()):
                if(p in self.dsub[s].keys()): 
                    #predicato gia inserito 
                    if(type(self.dsub[s][p])  is list):
                        self.dsub[s][p].append(o)
                    else:
                        tmp = self.dsub[s][p]
                        del self.dsub[s][p]
                        self.dsub[s][p] = []
                        self.dsub[s][p].append(tmp)
                        self.dsub[s][p].append(o)
                else:
                    #predicato sconosciuto 
                    self.dsub[s][p] = o
            else:
                self.dsub[s] = {}
                self.dsub[s][p] = o
            
            #RDF to NetworkX
            if(p in _from):
                if(o not in self.network.nodes()):
                    self.network.add_node(o)
                to_item = self.to_list[s]
                if(self.network.has_edge(o,to_item)):
                    w = self.network.get_edge_data(o,to_item)
                    w = w[0]["weight"] 
                    self.network[o][to_item][0]["weight"] = w + 1
                    #print(network.get_edge_data(o,to_item))
                else:
                    self.network.add_edge(o,to_item,attr=p,weight=1) 
        #print(self.network["HOODIE"])
        return self.network


    def frequency_nodes(self,name_label):
       # titolo ="label" #"titolo"
        count_node = 0
        for film in self.to_node:
            fre_film = 0 
            edj = self.network.in_edges(film)
            for e in edj:
                if(self.network.get_edge_data(e[0],e[1])[0]["attr"] == name_label):
                    fre_film += 1
            node = film + "_freq"    
            self.network.add_node(node)
            self.network.add_edge(film,node,freq=fre_film)
            count_node += fre_film
        return count_node



    def numOutDegree(self,node, to=None):
        weight = "weight"
        outdegree = 0
        if to == None:
            out_edges = list(self.network.out_edges(node, data=True))
            for out_edge in out_edges:        
                outdegree += out_edge[2][weight]
        else:        
            out_edges = list(self.network.out_edges(node, data=True))        
            for out_edge in out_edges: 
                if out_edge[1] == to:
                    outdegree += out_edge[2][weight]
        return outdegree

    def draw_network(self):
        pos = nx.spring_layout(self.network)   
        nx.draw_networkx_edge_labels(self.network, pos, labels=edge_labels,
                                        font_size=10, font_color='k', font_family='sans-serif',
                                        font_weight='normal', alpha=2.0, bbox=None, ax=None, rotate=False)
        nx.draw(self.network, pos=pos, with_labels=True, node_size=200,font_size=13) 
        plt.show()  