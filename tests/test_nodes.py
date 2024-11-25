# tests/test_nodes.py

import unittest
from src.nodes import Node

class TestNode(unittest.TestCase):

    def test_trust_initialization(self):
        node = Node(node_id=0)
        self.assertEqual(node.node_id, 0)
        self.assertEqual(node.alpha, 0.1)
        self.assertEqual(node.trust_scores, {})
        self.assertEqual(node.received_messages, [])

    def test_set_peers(self):
        node1 = Node(node_id=1)
        node2 = Node(node_id=2)
        node1.set_peers([node2])
        self.assertIn(node2, node1.peers)
        self.assertIn(node2.node_id, node1.trust_scores)
        self.assertEqual(node1.trust_scores[node2.node_id], 1.0)

    def test_compute_trust_feedback(self):
        node1 = Node(node_id=1)
        node2 = Node(node_id=2)
        feedback = node1.compute_trust_feedback(node2)
        self.assertIsInstance(feedback, float)

    def test_send_and_receive_message(self):
        node1 = Node(node_id=1)
        node2 = Node(node_id=2)
        node1.set_peers([node2])
        messages = node1.send_message()
        node2.receive_message(node1.node_id, messages[node2.node_id])
        self.assertEqual(len(node2.received_messages), 1)
        self.assertEqual(node2.received_messages[0][0], node1.node_id)

    def test_update_trust(self):
        node1 = Node(node_id=1)
        node2 = Node(node_id=2)
        node1.set_peers([node2])
        # Simulate receiving a message
        node1.receive_message(node2.node_id, 0.5)
        node1.update_trust()
        self.assertNotEqual(node1.trust_scores[node2.node_id], 1.0)
