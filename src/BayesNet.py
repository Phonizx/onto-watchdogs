import  Net as nt
import sys
ZERO_PROB = sys.float_info.min

class BayesNet:

    def __init__(self, net):
        self.n = net
        self.graph = net.get_network()
        self.to_node = net.get_ToNode()

    def inizialize_probability(self):
        causes = self.to_node.copy()
        for to in self.to_node:
            causes.append(to+"_freq")
        nodi = list(self.graph.nodes())
        for cas in causes:
            try:
                for n in nodi:
                    if n==cas:
                        nodi.remove(cas)
            except:
                print(end="")
        for cause in self.to_node:
            self.bayes_calc(cause, nodi)



    def normalize_zero(self, prob):
        return ZERO_PROB if prob == 0 else prob

    def probability_priori(self, B, N):
        if N>0:
            try:
                pr = self.graph.get_edge_data(B, B+"_freq")[0]["probability"]
            except:
                pr = self.graph.get_edge_data(B, B+"_freq")[0]["freq"]/N
                self.add_prob_edge(B, B+"_freq", pr)
            return self.normalize_zero(pr)
        else:
            print("N = 0!")
            return ZERO_PROB

    #add a weight "probability", if there aren't edges, we assume prob equals to ZERO_PROB
    def add_prob_edge(self, node, to, prob):
        if (self.graph.has_edge(node, to)):
            edge = self.graph.get_edge_data(node, to)[0]
            self.graph.remove_edge(node, to)
            try:
                self.graph.add_edge(node, to, attr=edge["attr"], weight=edge["weight"], probability=prob)
            except:
                self.graph.add_edge(node, to, probability=prob)
        else:
            self.graph.add_edge(node, to, attr="ruolo", weight=0, probability=prob)

    def conditional_probability(self, node, to): #P (A | B)
        if isinstance(node, list):
            if len(node)>1:
                try:
                    p_A_B = self.graph.get_edge_data(node[0], to)[0]["probability"]
                except:
                    p_A_B = self.n.numOutDegree(node[0], to) / self.n.numOutDegree(node[0])
                    p_A_B = self.normalize_zero(p_A_B)
                    self.add_prob_edge(node[0], to, p_A_B)
                p = p_A_B * self.conditional_probability(node[1:], to)
            else:
                if len(node)==1:
                    p = self.conditional_probability(node[0], to)
        else: 
            try:
                p = self.graph.get_edge_data(node, to)[0]["probability"]
            except:
                p = self.n.numOutDegree(node, to) / self.n.numOutDegree(node)
                p = self.normalize_zero(p)
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
            bayesP = (p_A_B * pr) / p_FPT
            return bayesP if bayesP > 0 else ZERO_PROB