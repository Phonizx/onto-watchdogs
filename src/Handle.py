import os,glob 
import BayesNet as bn 
import  Net as nt

class Handle:
    def __init__(self):
        #self.bn = BN.BayesNet()
        self.path = "../ontologie/"
       
    def show_ontologies(self):
        os.chdir(self.path)
        print("Ontologie trovate: ")
        g = glob.glob("*.*")
        for file in glob.glob("*.xml"):
            print("\t- " + file.title())
    
    def load_demo(self,demo,_from,to):
        self.net = nt.Net("../ontologie/" + demo,_from,to)

        #bayes = bn.BayesNet(["titolo","direttore","attore","autore"],["genere"])
        #print("thBayes: "+ str(bayes.bayes_calc("CARTOON", ["HOODIE","ROCCO"])))
