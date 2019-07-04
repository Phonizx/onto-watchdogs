import  Net as nt 

class BayesNet:

    def __init__(self,_from,to):
        #get networkx from Net.py 
        self.n = nt.Net(_from,to)
        self.graph = self.n.get_network()
        self.to_node = self.n.get_ToNode()
    
    def probability_priori(self, B, N):
        if N>0:
            return self.graph.get_edge_data(B, B+"_freq")[0]["freq"]/N
        else:
            print("N = 0!")
            return -1

    def conditional_probability(self,node, to): #P (A  | B)
        if isinstance(node, list):
            if len(node)>1:
                p = self.n.numOutDegree(node[0], to) / self.n.numOutDegree(node[0]) *  self.conditional_probability(node[1:],to)
                return p
            else:
                if len(node)==1:
                    p = self.conditional_probability(node[0], to) 
                    return p
        else:
            p = self.n.numOutDegree(node, to) / self.n.numOutDegree(node) 
            return p

    def probability_FPT(self,Bs, N):
        P_B = 0
        for priori in self.to_node:
            pr = self.probability_priori(priori, N)
            # Calcola la prob condizionata e congiuta dei nodi Bs
            pc = self.conditional_probability(Bs, priori)
            P_B += pc * pr
        return  P_B

    def bayes_calc(self,cause, effects):
        tot_freq = self.n.totfreq
        p_FPT = self.probability_FPT(effects, tot_freq)
        if p_FPT <= 0:
            return 0
        else:
            p_A_B = self.conditional_probability(effects, cause)
            pr = self.probability_priori(cause, tot_freq)
            return (p_A_B * pr) / p_FPT