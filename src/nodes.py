# src/nodes.py

import numpy as np

class Node:
    """
    Represents a participant in the federated learning network.
    """

    def __init__(self, node_id, alpha=0.1):
        self.node_id = node_id
        self.alpha = alpha
        self.trust_scores = {}  # Trust scores for other nodes
        self.received_messages = []
        self.peers = []  # List of peer Node instances

    def set_peers(self, peers):
        self.peers = peers
        # Initialize trust scores for peers
        for peer in peers:
            self.trust_scores[peer.node_id] = 1.0  # Initial trust score

    def send_message(self):
        """
        Sends trust feedback messages to peers.
        Returns a dictionary of messages {peer_id: message}.
        """
        messages = {}
        for peer in self.peers:
            m_jk = self.compute_trust_feedback(peer)
            messages[peer.node_id] = m_jk
        return messages

    def compute_trust_feedback(self, peer):
        """
        Computes the trust feedback message for a given peer.
        """
        # Simulate predictive accuracies
        predictive_accuracy_with_k = np.random.uniform(0.7, 1.0)
        predictive_accuracy_without_k = np.random.uniform(0.5, 0.9)
        m_jk = predictive_accuracy_with_k - predictive_accuracy_without_k
        return m_jk

    def receive_message(self, sender_id, message):
        """
        Receives a message from a peer.
        """
        self.received_messages.append((sender_id, message))

    def update_trust(self):
        """
        Updates the trust scores based on received messages.
        """
        for sender_id, message in self.received_messages:
            T_ij = self.trust_scores.get(sender_id, 1.0)  # Trust in sender
            # Update trust in node k (assuming k is the sender)
            T_ik = self.trust_scores.get(sender_id, 1.0)
            T_ik_new = T_ik + self.alpha * T_ij * message
            self.trust_scores[sender_id] = T_ik_new
        # Clear messages after processing
        self.received_messages = []
