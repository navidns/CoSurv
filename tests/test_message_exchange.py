# tests/test_message_exchange.py

import unittest
import simpy
from src.nodes import Node
from src.message_exchange import MessageExchange

class TestMessageExchange(unittest.TestCase):

    def test_message_exchange(self):
        env = simpy.Environment()
        node1 = Node(node_id=1)
        node2 = Node(node_id=2)
        node1.set_peers([node2])
        node2.set_peers([node1])
        message_exchange = MessageExchange(env, [node1, node2])
        env.run(until=1)
        # Check if nodes have updated their trust scores
        self.assertNotEqual(node1.trust_scores[node2.node_id], 1.0)
        self.assertNotEqual(node2.trust_scores[node1.node_id], 1.0)
