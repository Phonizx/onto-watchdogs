cd C:\Users\curci\Desktop\IC\progettoic\onto-watchdogs\src

pRDF.py demo --eg KBPs
pause
pRDF.py bayes --ws cellprob250
pause
http://amigo.geneontology.org/amigo/term/CL:0000463



pRDF.py bayes --ws nciprob250
pRDF.py bayes --ws teleostprob250

pRDF.py load cellprob250.xml --about annotatedSource,probability --to annotatedTarget
pRDF.py load cellprob500.xml --about annotatedSource,probability --to annotatedTarget
pRDF.py load cellprob750.xml --about annotatedSource,probability --to annotatedTarget
pRDF.py load cellprob1000.xml --about annotatedSource,probability --to annotatedTarget

pRDF.py load nciprob250.xml --about annotatedSource,probability --to annotatedTarget
pRDF.py load nciprob500.xml --about annotatedSource,probability --to annotatedTarget
pRDF.py load nciprob750.xml --about annotatedSource,probability --to annotatedTarget
pRDF.py load nciprob1000.xml --about annotatedSource,probability --to annotatedTarget

pRDF.py load teleostprob250.xml --about annotatedSource,probability --to annotatedTarget
pRDF.py load teleostprob500.xml --about annotatedSource,probability --to annotatedTarget
pRDF.py load teleostprob750.xml --about annotatedSource,probability --to annotatedTarget
pRDF.py load teleostprob1000.xml --about annotatedSource,probability --to annotatedTarget