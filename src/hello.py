import rdflib 
from rdflib import Graph, Literal, BNode, Namespace, RDF, URIRef
from rdflib.namespace import DC, FOAF

from rdflib.extras.external_graph_libs import rdflib_to_networkx_multidigraph
import networkx as nx
import matplotlib.pyplot as plt
from rdflib.collection import Collection
from rdflib import ConjunctiveGraph, URIRef, RDFS

g = Graph()
g.parse("https://raw.githubusercontent.com/stardog-union/stardog-examples/develop/examples/machinelearning/movies.ttl",format="ttl")

g.serialize(destination='film.xml', format='xml')


for s,p,o in g:
    print(s,p,o)


'''
G = rdflib_to_networkx_multidigraph(g)
pos = nx.spring_layout(G, scale=2)
edge_labels = nx.get_edge_attributes(G, 'r')
nx.draw_networkx_edge_labels(G, pos, labels=edge_labels)
nx.draw(G, with_labels=True)
plt.show()
'''
























'''
# Create an identifier to use as the subject for Donna.
donna = BNode()
horse = BNode()


# Add triples using store's add method.
g.add( (donna, RDF.type, FOAF.Person) )
g.add((donna,FOAF.familyName,Literal("Equini")))
g.add( (donna, FOAF.nick, Literal("donna", lang="foo")) )
g.add( (donna, FOAF.name, Literal("CatWoman")) )
g.add( (donna, FOAF.mbox, URIRef("mailto:donna@example.org")) )


g.add((horse,RDF.type,FOAF.Person))
g.add( (horse, FOAF.nick, Literal("giovan", lang="foo")) )
g.add((horse,FOAF.familyName,Literal("Equini")))
g.add( (horse, FOAF.name, Literal("Donato")) )
g.add( (horse, FOAF.mbox, URIRef("mailto:horsegiovan@pornhub.org")) )


# Iterate over triples in store and print them out.
print("--- printing raw triples ---")

for person in g.subjects(RDF.type, FOAF.Person):
    for mbox in g.objects(person, FOAF.mbox):
        print(mbox)

#print(g.serialize(format='ttl'))

#for s, p, o in g:
    #print((s, p, o))

#save rdf graph 
g.serialize(destination='ttlout.ttl', format='ttl')



'''

'''
person = URIRef('ex:person')
dad = URIRef('ex:d')
mom = URIRef('ex:m')
momOfDad = URIRef('ex:gm0')
momOfMom = URIRef('ex:gm1')
dadOfDad = URIRef('ex:gf0')
dadOfMom = URIRef('ex:gf1')

parent = URIRef('ex:parent')
bob = URIRef("ex:bob")
 
g = ConjunctiveGraph()
g.add((person, parent, dad))
g.add((person, parent, mom))

g.add((dad, parent, momOfDad))
g.add((dad, parent, dadOfDad))
g.add((mom, parent, momOfMom))
g.add((mom, parent, dadOfMom))
g.add((mom,parent,bob))

print("Parents, forward from `ex:person`:")
for i in g.transitive_objects(person, parent): #la prop. Transitiva sta nell'enumerare l'entità C:
    print(i)                                   #person(A) => parent(B) ^ parent(B) => Entity(C) => person(A) => Entity(C)
print("Parents, *backward* from `ex:gm1`:")
for i in g.transitive_subjects(parent, momOfMom):
    print(i)



g.add((bob,RDFS.label,Literal(1099)))


g.serialize(destination='persons.xml', format='xml')
'''
