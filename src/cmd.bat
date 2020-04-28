cd C:\Users\curci\Desktop\IC\progettoic\onto-watchdogs\src
 

pRDF.py parse --ws film --path KBfilm.xml
pRDF.PY bayes --ws film

pause
pause
pRDF.py demo --eg film
pRDF.py parse --ws film --path KBfilm.xml
pRDF.py query --ws film

pRDF.py parse --ws film --path KBfilm.xml
pRDF.py load C:\Users\curci\Desktop\IC\progettoic\onto-watchdogs
\ontologie\film.xml --about titolo,regista,attore,autore --to genere --prob


1) intro doc
2) mostro ontologia e significato
3) esempio di utilizzo con semantica

ESEMPIO:	
	"TIZIO -> RUOLO -> STUDENTE/DOCENTE" VERO/FALSO
	"TIZIO -> STUDENTE/DOCENTE -> 0,7/0,3" 
in questa proposizione viene sottinteso la relazione/predicato
 "ruolo"

Il sistema aggiunge la parte probabilistica delle
 nuove triple che rappresentano delle proposizioni 
 logiche probabilistiche
	ONTOLOGIA	->	ONTOLOGIA PROBABILISTICA/KBP
	<RDF>		->	<RDF> + <TRIPLE CON PROB>

è possibile interagire con la KB con query SPARQL in 
modo da poter usufruire anche della parte puramente logica


entailed http://www.dis.uniroma1.it/rosati/semanticweb/slides5.pdf