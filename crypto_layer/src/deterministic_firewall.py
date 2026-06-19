import networkx as nx

class DeterministicRiskFirewall:
    def __init__(self):
        self.tx_graph = nx.DiGraph()

    def intercept_transaction(self, sender: str, receiver: str, amount: float, timestamp: float) -> bool:
        self.tx_graph.add_edge(sender, receiver, amount=amount, time=timestamp)
        try:
            cycles = list(nx.find_cycle(self.tx_graph, source=sender, orientation="original"))
            if len(cycles) > 2:
                return False
        except nx.NetworkXNoCycle:
            pass
        return True
