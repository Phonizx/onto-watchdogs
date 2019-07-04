import  Net as nt
import sys
ZERO_PROB = sys.float_info.min

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
            return ZERO_PROB

    #add a weight "probability", if there aren't edges, we assume prob equals to ZERO_PROB
    def add_prob_edge(self, node, to, prob):
        if (self.graph.has_edge(node, to)):
            edge = self.graph.get_edge_data(node, to)[0]
            self.graph.remove_edge(node, to)
            self.graph.add_edge(node, to, attr=edge["attr"], weight=edge["weight"], probability=prob)
        else:
            self.graph.add_edge(node, to, attr="ruolo", weight=0, probability=ZERO_PROB) 


    def conditional_probability(self, node, to): #P (A  | B)
        if isinstance(node, list):
            if len(node)>1:
                try:
                    p_A_B = self.graph.get_edge_data(node, to)[0]["probability"]/N
                except:
                    p_A_B = self.n.numOutDegree(node[0], to) / self.n.numOutDegree(node[0])
                    self.add_prob_edge(node[0], to, p_A_B)
                p = p_A_B * self.conditional_probability(node[1:],to)
                return p
            else:
                if len(node)==1:
                    p = self.conditional_probability(node[0], to) 
                    return p
        else:
            try:
                p = self.graph.get_edge_data(node, to)[0]["probability"]/N
            except:
                p = self.n.numOutDegree(node, to) / self.n.numOutDegree(node)
                self.add_prob_edge(node, to, p)
            return p

    def probability_FPT(self, Bs, N):
        P_B = ZERO_PROB
        for priori in self.to_node:
            pr = self.probability_priori(priori, N)
            # Calcola la prob condizionata e congiuta dei nodi Bs
            pc = self.conditional_probability(Bs, priori)
            P_B += pc * pr
        return  P_B

    def bayes_calc(self, cause, effects):
        tot_freq = self.n.totfreq
        p_FPT = self.probability_FPT(effects, tot_freq)
        if p_FPT <= 0:
            print("p_FPT = 0!")
            return ZERO_PROB
        else:
            p_A_B = self.conditional_probability(effects, cause)
            pr = self.probability_priori(cause, tot_freq)
            bayesP=(p_A_B * pr) / p_FPT
            if (bayesP == 0):
                bayesP = ZERO_PROB
            return bayesP