import os, glob, sys
import BayesNet as bn
import  Net as nt
import networkx as nx

import time
ZERO_PROB = sys.float_info.min

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
    
    def load_ontologia(self, demo, _from, to, init=False): #warning, load ontologia NON DEMO
        print(demo)
        self.net = nt.Net()
        self.net.load_graph("../ontologie/" + demo, _from, to)

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

    def bayesianOp(self, workspace, effects, cause, show=False):
        self.path_workspace = self.ws + workspace
        net = self.loadGraph(self.path_workspace)
        bayes = bn.BayesNet(net)
        if(os.path.isdir(self.path_workspace)):
            print("P(" + str(cause) + "|" + str(effects) + "): " + str(bayes.bayes_calc(cause, effects)))
        if(show):
            net.draw_network()

    def bayesianOp_Random(self, workspace, show=False):
        self.path_workspace = self.ws + workspace
        net = self.loadGraph(self.path_workspace)
        cause, effects = net.random_node_pair()
        bayes = bn.BayesNet(net)
        if(os.path.isdir(self.path_workspace)):
            prob = bayes.bayes_calc(cause, effects)
            if (prob > ZERO_PROB):
                print("P(" + str(cause) + "|" + str(effects) + "): " + str(prob))
        if(show):
            net.draw_network()
        return (prob, cause, effects)

    def demos(self, example):
        if(example in "KBPs"):
            onts = ["cell", "nci", "teleost"]
            nums = ["250", "500", "750", "1000"]
            from_ = ["annotatedSource", "probability"]
            to_ = ["annotatedTarget"]
            caricamento KBPs
            for o in onts:
                for i in nums:
                    self.load_ontologia((o + "prob" + i + ".xml"), from_, to_)
            esecuzione queries
            tempi = []
            tot_tempo = 0
            for o in onts:
                for i in nums:
                    ws_ = o + "prob" + i
                    print(ws_)
                    
                    f = open("../queries/" + o + "/" + o + "_queries (" + str(int(i) % 250 + 1) + ").txt", "r")
                    tempo = 0
                    cont = 0
                    # lettura ed esecuzione di 100 queries
                    while True:
                        tmp = f.readline()
                        if tmp =="":
                            break
                        tmp = tmp.split("|")
                        a, b = tmp[0], (tmp[1].split("\n"))[0]
                        t1 = time.time()
                        # self.bayesianOp(ws_, [a], b)
                        self.bayesianOp_Random(ws_ )
                        tempo += time.time() - t1
                        cont += 1
                        tmp = f.readline()
                        # Generazione di 100 queries
                        
                    # risultati = open("queries"+ws_+".txt", "w")
                    # for i in range(0, 100):
                    #     # prob, cause, effects = self.bayesianOp_Random(ws_)
                    #     print(prob,cause,effects)
                    #     if prob > ZERO_PROB:
                    #         risultati.writelines(cause+"|"+effects+"\n")
                    #         print(cont, tot)
                    #         cont += 1
                    #     tot+=1
                    # risultati.close()
                    tot_tempo += tempo
                    tempomed = tempo / cont
                    tempi.append((ws_, tempomed, tempo))
                    print("Tempo medio impegato per la query: ", tempomed)
                    f.close()

            print("Tempo totale impiegato", tot_tempo)
            for t in tempi:
                print(t)

        if(example in "film"):
            self.load_ontologia("film.xml",["titolo","regista","attore","autore"],["genere"],True)
            self.bayesianOp("film", ["ATTORE2","AUTORE2"],"HORROR",True)
            self.bayesianOp("film", ["ATTORE2","AUTORE2"],"CARTOON",True)
        else:
            if(example in "metastaticcancer"):
                self.load_ontologia("metastaticcancer.xml",["paziente","BrainTumor","SerumCalcium"],["MetastaticCancer"],True)
                self.bayesianOp("metastaticcancer", ["TRUESC","FALSEBT"],"TRUEMC",True)

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