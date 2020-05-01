import rdflib
from rdflib import Graph, Literal, BNode, Namespace, RDF, URIRef
from rdflib.namespace import DC, FOAF
from rdflib.extras.external_graph_libs import rdflib_to_networkx_multidigraph
import networkx as nx
import matplotlib.pyplot as plt
from rdflib.collection import Collection
from rdflib import ConjunctiveGraph, URIRef, RDFS
import re
import _pickle as cPickle
import sys
import random

ZERO_PROB = sys.float_info.min
PREDICATI = ["annotatedSource", "annotatedTarget", "probability"]

class Net:

    def __init__(self):
        pass

    def load_graph(self, path_rdf, _from, to):
        self.network = nx.MultiDiGraph()
        self.dsub = {}
        self.entity = {}
        self.to_list = {}
        self.to_node = []
        self.from_node = set()
        self.g = self.load_rdf(path_rdf)
        self.totfreq=1
        if to[0] == PREDICATI[1]:
            self.parse_to_graph_probabilistic(self.g, _from, to)
        else:
            self.parse_to_graph(self.g, _from, to)
            self.totfreq = self.frequency_nodes(_from[0])

    def load_net(self, path_dump):
        f = open(path_dump, 'rb')
        tmp_dict = cPickle.load(f)
        f.close()
        self.__dict__.update(tmp_dict)

    def load_rdf(self, path):  # carica rdf da path
        g = Graph()
        try:
            return g.parse(path)
        except:
            print("Errore: Percorso rdf invalido.")

    def get_entity(self):
        return self.entity

    def get_ToNode(self):
        return self.to_node

    def get_network(self):
        return self.network

    def get_Rdf(self):
        return self.g

    def get_FromNode(self):
        return self.from_node

    def filter(self, s, p, o):
        s = s.strip().replace("//", "/").split('/')
        s = s[len(s)-1]
        p = p.strip().replace("//", "/")
        p = re.split('~|#|/', p)
        p = p[len(p)-1]
        o = o.strip().replace("//", "/")
        o = re.split('~|#|/', o)
        o = o[len(o)-1]
        return s, p, o

    def parse_entity(self, g, _from, to):
        for s, p, o in g:
            s, pr, _o = self.filter(s, p, o)
            if(pr in to):  # predicati
                if(_o not in self.network.nodes()):
                    self.network.add_node(_o)   # generi univoci nel grafo
                    self.to_node.append(_o)
                self.to_list[s] = _o
            if(pr in _from and pr not in _from[0]):
                self.entity[pr] = p
                self.from_node.add(_o)

    def parse_to_graph(self, g, _from, to, target=None):
        g = self.g
        self.parse_entity(g, _from, to)  # parsing dei singoli nodi To
        for s, p, o in g:
            s, p, o = self.filter(s, p, o)
            if(s in self.dsub.keys()):
                if(p in self.dsub[s].keys()):
                    # predicato gia inserito
                    if(type(self.dsub[s][p]) is list):
                        self.dsub[s][p].append(o)
                    else:
                        tmp = self.dsub[s][p]
                        del self.dsub[s][p]
                        self.dsub[s][p] = []
                        self.dsub[s][p].append(tmp)
                        self.dsub[s][p].append(o)
                else:
                    # predicato sconosciuto
                    self.dsub[s][p] = o
            else:
                self.dsub[s] = {}
                self.dsub[s][p] = o

            # RDF to NetworkX
            if(p in _from):
                if(o not in self.network.nodes()):
                    self.network.add_node(o)
                to_item = self.to_list[s]
                if(self.network.has_edge(o, to_item)):
                    w = self.network.get_edge_data(o, to_item)
                    w = w[0]["weight"]
                    self.network[o][to_item][0]["weight"] = w + 1
                else:
                    self.network.add_edge(o, to_item, attr=p, weight=1)
        return self.network

    def parse_to_graph_probabilistic(self, g, _from, to, target=None):
        g = self.g
        self.parse_entity(g, _from, to)  # parsing dei singoli nodi To
        for s, p, o in g:
            s, p, o = self.filter(s, p, o)
            if(s in self.dsub.keys()):  # se il soggeto è stato già trovato
                if(p in self.dsub[s].keys()):   # se il predicato è stato già trovato
                    if(type(self.dsub[s][p]) is list): # se sono presenti dei oggetti 
                        self.dsub[s][p].append(o)
                    else:
                        tmp = self.dsub[s][p]
                        del self.dsub[s][p]
                        self.dsub[s][p] = []
                        self.dsub[s][p].append(tmp)
                        self.dsub[s][p].append(o)
                else:
                    self.dsub[s][p] = o
            else:
                self.dsub[s] = {}
                self.dsub[s][p] = o
        nodi = set()
        for k, v in self.dsub.items():
            if k[0] == "N" or  k[0] == "T" :
                sogg, ogg, prob = v[_from[0]], v[to[0]], v[_from[1]]
                nodi.add(sogg)
                nodi.add(ogg)
                self.add_node([sogg, ogg])
                self.to_node.append(ogg)
                self.network.add_edge(sogg, ogg, probability=float(prob))
            else:
                if k[0]=="g":
                    nodi.add(k.split("#")[1])
                    try:
                        tmp = v["subClassOf"]
                        if isinstance(tmp, list):
                            for x in v:
                                nodi.add(x)
                        else:
                            nodi.add(tmp)
                    except:
                        pass
        self.to_node =list(set(self.to_node))
        
        da_eliminare = ["type","Thing","subClassOf","type","ObsoleteClass"]
        eliminati = 0
        for e in da_eliminare:
            if e in nodi:
                nodi.remove(e)
                eliminati +=1 
        self.totfreq = len(nodi)-eliminati
        return self.network

    def add_node(self, x):
        if isinstance(x, list):
            for e in x:
                self.add_node(e)
        else:
            if (x not in self.network.nodes()):
                self.network.add_node(x)



    def frequency_nodes(self, name_label):
       # titolo ="label" #"titolo"
        count_node = 0
        for entity in self.to_node:
            freq_entity = 0
            edj = self.network.in_edges(entity)
            for e in edj:
                if(self.network.get_edge_data(e[0], e[1])[0]["attr"] == name_label):
                    freq_entity += 1
            node = entity + "_freq"
            self.network.add_node(node)
            self.network.add_edge(entity, node, freq=freq_entity)
            count_node += freq_entity
        return count_node

    def numOutDegree(self, node, to=None):
        weight = "weight"
        outdegree = 0
        out_edges = list(self.network.out_edges(node, data=True))
        if to == None:  # richiede il totale di archi uscenti
            try:
                for out_edge in out_edges:
                    outdegree += out_edge[2][weight]
            except:
                out_edge=ZERO_PROB
        else:
            for out_edge in out_edges:
                if out_edge[1] == to:
                    outdegree += out_edge[2][weight]
        return outdegree

    def draw_network(self):
        pos = nx.spring_layout(self.network, k=100)
        nx.draw_networkx_edge_labels(self.network, pos,
                                     font_size=10, font_color='k', font_family='sans-serif',
                                     font_weight='normal', alpha=2.0, bbox=None, ax=None, rotate=False)
        nx.draw(self.network, pos=pos, with_labels=True,
                node_size=200, font_size=13)
        plt.show()

    def dump_net(self, path_dump):
        f = open(path_dump, 'wb')
        cPickle.dump(self.__dict__, f, 2)
        f.close()

    def decoding(self, ws, path="polarize.xml"):
        for fnode in self.from_node:
            for e in self.network.edges(fnode):
                pr = self.network.get_edge_data(e[0], e[1])[0]["probability"]
                role = self.network.get_edge_data(e[0], e[1])[0]["attr"]
                s = URIRef(self.entity.get(
                    role, "http:www.example.com/ruolo") + "/" + str(e[0]).lower())
                p = URIRef("http://www.example.com/genere/" +
                           str(e[1]).lower())
                o = URIRef((Literal(pr)))
                self.g.add((s, p, o))
        self.g.serialize(path, format="xml")
        # aggiornamento di net con kb probabilistica
        self.dump_net(ws + "/graph.pickle")

    def query(self, query="SELECT ?genere ?prob  WHERE {<http://www.example.org/attore/hoodie> ?genere ?prob}"):
        result_set = []
        try:
            rows = self.g.query(query)

            result_set = []
            for binding in rows.bindings:
                for k, v in binding.items():
                    k = str(k)
                    v = str(v)
                    v = v.split('/')
                    v = v[len(v)-1]
                    result_set.append({v: k})
            print(result_set)
        except:
            print("Errore di sintassi.")

    def random_node_pair(self):
        len_to = len(self.to_node)-1

        while True:
            to = random.randint(0, len_to)
            a = self.to_node[to]
            if a[0] == "C" or a[0] == "N" or a[0] == "T":
                out_edges = list(self.network.out_edges(a, data=True))
                
                if len(out_edges) > 0:
                    b = out_edges[random.randint(0, len(out_edges)-1)][1]
                    break

        # while True:
        #     to = random.randint(0, len_to)
        #     b = self.to_node[to]
        #     if b[0] == "C" or b[0] == "N" or b[0] == "T":
        #         break

        primo = random.randint(0, 1)
        if primo == 1:
            return a, b
        else:
            return b, a

