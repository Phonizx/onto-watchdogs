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
    
    def load_demo(self,demo,_from,to): #warning, load ontologia NON DEMO
        self.net = nt.Net()
        self.net.load_graph("../ontologie/" + demo,_from,to)
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
            self.loadGraph(self.path_workspace)

    def dumpGraph(self):   
        self.net.dump_net(self.path_workspace + "/graph.pickle") 
        #nx.write_gpickle(self.net.get_network(), self.path_workspace +"/graph.gpickle")

    def loadGraph(self,path_workspace):
        try:
            self.net = nt.Net()
            self.net.load_net(path_workspace + "/graph.pickle")
            self.network = self.net.get_network()
            #print(self.network["HOODIE"])
            return self.network
        except:
            print("Exception: loading graph error")
            return None
        

    def bayesanOp(self,workspace,effects,cause):
        self.path_workspace = self.ws + workspace
        if(os.path.isdir(self.path_workspace)):
            print("ktm")
            #self.bn = BN.BayesNet()
