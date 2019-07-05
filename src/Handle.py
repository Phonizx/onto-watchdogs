import os,glob,sys
import BayesNet as bn 
import  Net as nt
import networkx as nx


class Handle:
    def __init__(self):
        #self.bn = BN.BayesNet()
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
    
    def load_demo(self,demo,_from,to):
        self.net = nt.Net("../ontologie/" + demo,_from,to)
        ws_name = demo.split('/')
        ws_name = ws_name[len(ws_name)-1]
        self.path_workspace = self.ws + ws_name 

        if(os.path.isdir(self.path_workspace)):
            print("Workspace Existed")
        else:
            os.mkdir(self.path_workspace)
            self.dumpGraph()

    def show_workspace(self):
        if(os.path.isdir(self.ws)):
            for r, d, f in os.walk(self.ws):
                for folder in d:
                    print("  - " + folder)
        else:
            print("Error: WorkSpace doesn't exists")

    def loadWorkspace(self,name):
        self.path_workspace = self.ws + name
        if(os.path.isdir(self.path_workspace)):
            self.loadGraph()

    def dumpGraph(self):    
        nx.write_gpickle(self.net.get_network(), self.path_workspace +"/graph.gpickle")

    def loadGraph(self):
        try:
            self.network = nx.read_gpickle(self.path_workspace + "/graph.gpickle")
        except:
            print("Exception: loading graph error")
