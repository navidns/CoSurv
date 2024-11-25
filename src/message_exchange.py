# src/message_exchange.py

import simpy

class MessageExchange:
    """
    Manages the message exchange process between nodes in the network.
    """

    def __init__(self, env, nodes):
        self.env = env
        self.nodes = nodes
        self.action = env.process(self.run())

    def run(self):
        """
        Simulates the message exchange over time.
        """
        while True:
            # Each node sends messages to peers
            for node in self.nodes:
                messages = node.send_message()
                for peer_id, message in messages.items():
                    # Find the peer node
                    peer_node = self.get_node_by_id(peer_id)
                    if peer_node:
                        peer_node.receive_message(node.node_id, message)
            # Wait for the next time step
            yield self.env.timeout(1)
            # Each node updates trust scores
            for node in self.nodes:
                node.update_trust()

    def get_node_by_id(self, node_id):
        """
        Returns the node instance with the given node_id.
        """
        for node in self.nodes:
            if node.node_id == node_id:
                return node
        return None
