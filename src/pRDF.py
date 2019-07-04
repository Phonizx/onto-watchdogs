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
import Net as nt
import BayesNet as bn 



conds = " " 

bayes = bn.BayesNet(["direttore","attore","autore"],["genere"])


while(not(conds == "esci")):
    try:
        conds = input("inserire uno o piu nodi separta da ',': ")
        conds = conds.replace(" ","").upper()
        conds = conds.split(',')
        gen = input("inserire un genere: ")
        gen = gen.upper()
        print("Pr: "+ str(bayes.conditional_probability(conds, gen)))        
        print("thBayes: "+ str(bayes.bayes_calc(gen, conds , tot_freq)))
        #print(g_parsed[s])
        conds=" "
    except:
        print("exit",end="")
        break
 


