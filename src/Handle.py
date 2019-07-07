import os,glob,sys
import BayesNet as bn 
import  Net as nt
import networkx as nx


class Handle:
    def __init__(self):
        self.ws = ".ws/"
        if(not os.path.isdir(self.ws)):
            os.mkdir(self.ws)
        self.path = "../ontologie/"
        
    def show_ontologies(self):
        os.chdir(self.path)
        print("Ontologie trovate: ")
        g = glob.glob("*.*")
        for file in glob.glob("*.xml"):
            print("\t- " + file.title())
    
    def load_ontologia(self,demo,_from,to,init=False): #warning, load ontologia NON DEMO
        self.net = nt.Net()
        self.net.load_graph("../ontologie/" + demo,_from,to)

        if(init):
            bayes = bn.BayesNet(self.net)
            bayes.inizialize_probability()
        ws_name = demo.split('/')
        ws_name = ws_name[len(ws_name)-1]
        self.path_workspace = self.ws + ws_name 
        self.path_workspace = '.' + self.path_workspace.split('.')[1]
        
        if(os.path.isdir(self.path_workspace)):
            print(" Workspace gia' esistente ")
        else:
            os.mkdir(self.path_workspace)
            self.dumpGraph()

    def show_workspace(self):
        if(os.path.isdir(self.ws)):
            for r, d, f in os.walk(self.ws):
                for folder in d:
                    print("  - " + folder)
        else:
            print("Errore: WorkSpace non esistente.")

    def loadWorkspace(self,name):
        self.path_workspace = self.ws + name
        if(os.path.isdir(self.path_workspace)):
            self.loadGraph(self.path_workspace)

    def dumpGraph(self):   
        self.net.dump_net(self.path_workspace + "/graph.pickle") 

    def loadGraph(self,path_workspace): #load il dumping di net
        try:
            self.net = nt.Net()
            self.net.load_net(path_workspace + "/graph.pickle")
            self.network = self.net.get_network()
            return self.net
        except:
            print("Errore nel caricamento  del grafo.")
            return None
        
    
    def bayesanOp(self,workspace,effects,cause,show=False):
        self.path_workspace = self.ws + workspace
        net = self.loadGraph(self.path_workspace)
        bayes = bn.BayesNet(net)
        if(os.path.isdir(self.path_workspace)):
            print("P(" + str(cause) + "|" + str(effects) + "): " + str(bayes.bayes_calc(cause, effects)))
        if(show):
            net.draw_network()
        

    def demos(self,example):
        if(example in "toystory"):
            self.load_ontologia("toystory.xml",["titolo","direttore","attore","autore"],["genere"],True)
            self.bayesanOp("toystory", ["HOODIE","ROCCO"],"CARTOON",True)
        else:
            if(example in "metastaticcancer"):
                self.load_ontologia("metastaticcancer.xml",["paziente","BrainTumor","SerumCalcium"],["MetastaticCancer"],True)
                self.bayesanOp("metastaticcancer", ["TRUESC","FALSEBT"],"TRUEMC",True)

    def draw_graph(self,workspace):
        self.path_workspace = self.ws + workspace
        try:
            net = self.loadGraph(self.path_workspace)
            net.draw_network()
        except:
            print("Errore nella visualizzazione del grafo.")

    def parseToRdf(self,workspace,path):
        self.path_workspace = self.ws + workspace
        net  = self.loadGraph(self.path_workspace)
        net.decoding(self.path_workspace,path)

    def quering(self,workspace,query):
        self.path_workspace = self.ws + workspace
        net  = self.loadGraph(self.path_workspace) 
        net.query(query)