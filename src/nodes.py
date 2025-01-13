# # import numpy as np

# # class Node:
# #     """
# #     Represents a participant in the federated learning network.
# #     """

# #     def __init__(self, node_id, alpha=0.1, is_malicious=False, malicious_distribution='uniform'):
# #         self.node_id = node_id
# #         self.alpha = alpha
# #         self.is_malicious = is_malicious
# #         self.malicious_distribution = malicious_distribution
# #         self.trust_scores = {}
# #         self.received_messages = []
# #         self.peers = []

# #     def set_peers(self, peers):
# #         self.peers = peers
# #         for peer in peers:
# #             self.trust_scores[peer.node_id] = 1.0

# #     def send_message(self):
# #         """
# #         Sends trust feedback messages.
# #         In P2P mode: sends to all peers.
# #         In server-based mode: may send only to the server.
# #         """
# #         messages = {}
# #         for peer in self.peers:
# #             m_jk = self.compute_trust_feedback(peer)
# #             messages[peer.node_id] = m_jk
# #         return messages

# #     def compute_trust_feedback(self, peer):
# #         """
# #         Compute trust feedback for the given peer. If malicious, generate misleading feedback.
# #         """
# #         if self.is_malicious:
# #             return self.generate_malicious_feedback()
# #         else:
# #             # Honest node feedback:
# #             predictive_accuracy_with_k = np.random.uniform(0.7, 1.0)
# #             predictive_accuracy_without_k = np.random.uniform(0.5, 0.9)
# #             m_jk = predictive_accuracy_with_k - predictive_accuracy_without_k
# #             return m_jk

# #     def generate_malicious_feedback(self):
# #         """
# #         Generate malicious feedback based on the selected distribution.
# #         Examples:
# #          - Uniform: random value in a certain negative range
# #          - Normal: random value from a Gaussian distribution centered around negative or zero
# #         """
# #         if self.malicious_distribution == 'uniform':
# #             # Uniform random noise in a negative range
# #             return np.random.uniform(-0.5, 0.0)
# #         elif self.malicious_distribution == 'normal':
# #             # Normal distribution with mean=0 and std=0.1, likely negative influence
# #             # Adjust as needed (e.g., mean < 0 to ensure negativity)
# #             return np.random.normal(loc=-0.1, scale=0.1)
# #         else:
# #             # Default fallback if unknown distribution is given
# #             return np.random.uniform(-0.5, 0.0)

# #     def receive_message(self, sender_id, message):
# #         self.received_messages.append((sender_id, message))

# #     def update_trust(self):
# #         for sender_id, message in self.received_messages:
# #             T_ij = self.trust_scores.get(sender_id, 1.0)
# #             T_ik = self.trust_scores.get(sender_id, 1.0)
# #             T_ik_new = T_ik + self.alpha * T_ij * message
# #             self.trust_scores[sender_id] = T_ik_new
# #         self.received_messages = []
# import numpy as np

# class Node:
#     """
#     Represents a participant in the federated learning network.
#     """

#     def __init__(self, node_id, alpha=0.1, is_malicious=False, malicious_distribution='uniform'):
#         """
#         Initialize a node with its ID, learning rate, and malicious status.
#         """
#         self.node_id = node_id
#         self.alpha = alpha
#         self.is_malicious = is_malicious
#         self.malicious_distribution = malicious_distribution
#         self.trust_scores = {}  # Trust in other nodes
#         self.received_feedback = []  # Feedback received from peers
#         self.peers = []  # List of peer nodes

#     def set_peers(self, peers):
#         """
#         Define peers for the node.
#         """
#         self.peers = peers
#         for peer in peers:
#             self.trust_scores[peer.node_id] = 1.0  # Initialize trust to 1.0

#     def send_feedback(self):
#         """
#         Sends feedback about all peers.
#         """
#         feedback = {}
#         for peer in self.peers:
#             feedback[peer.node_id] = self.generate_feedback(peer)
#         return feedback

#     def generate_feedback(self, peer):
#         """
#         Generate feedback about a peer's contribution.
#         """
#         if self.is_malicious:
#             return self.generate_malicious_feedback()
#         else:
#             # Honest feedback based on predictive accuracy
#             accuracy_with_peer = np.random.uniform(0.7, 1.0)
#             accuracy_without_peer = np.random.uniform(0.5, 0.9)
#             return accuracy_with_peer - accuracy_without_peer

#     def generate_malicious_feedback(self):
#         """
#         Generate misleading feedback using the specified distribution.
#         """
#         if self.malicious_distribution == 'uniform':
#             return np.random.uniform(-0.5, 0.0)
#         elif self.malicious_distribution == 'normal':
#             return np.random.normal(loc=-0.2, scale=0.1)
#         else:
#             raise ValueError("Unsupported distribution: " + self.malicious_distribution)

#     def receive_feedback(self, sender_id, feedback):
#         """
#         Receive feedback from a peer.
#         """
#         self.received_feedback.append((sender_id, feedback))

#     def update_trust_scores(self):
#         """
#         Update trust scores based on received feedback.
#         """
#         for sender_id, feedback in self.received_feedback:
#             for target_id, m_jk in feedback.items():
#                 T_ij = self.trust_scores.get(sender_id, 1.0)  # Trust in the sender
#                 T_ik = self.trust_scores.get(target_id, 1.0)  # Current trust in the target
#                 # Update trust score using the aggregation rule
#                 self.trust_scores[target_id] = T_ik + self.alpha * T_ij * m_jk
#         # Clear feedback after processing
#         self.received_feedback = []

import numpy as np
import random


class Node:
    """
    Represents a participant in the federated learning network.
    """

    def __init__(self, node_id, alpha=0.1, is_malicious=False, malicious_distribution='uniform', noise_config=None):
        """
        Initialize a node with its ID, learning rate, malicious status, and noise configuration.
        """
        self.node_id = node_id
        self.alpha = alpha
        self.is_malicious = is_malicious
        self.malicious_distribution = malicious_distribution
        self.trust_scores = {}  # Trust in other nodes
        self.received_feedback = []  # Feedback received from peers
        self.peers = []  # List of peer nodes
        self.local_model_params = np.random.rand(10)  # Example local model parameters
        self.noise_config = noise_config  # Dictionary containing noise settings

    def set_peers(self, peers):
        """
        Define peers for the node.
        """
        self.peers = peers
        for peer in peers:
            self.trust_scores[peer.node_id] = 1.0  # Initialize trust to 1.0

    def send_feedback(self):
        """
        Sends feedback about all peers, including local model parameters.
        """
        feedback = {}
        for peer in self.peers:
            feedback[peer.node_id] = self.generate_feedback(peer)

        # Share local model parameters
        model_params = (
            self.add_noise_to_params(self.local_model_params)
            if self.noise_config and self.noise_config.get("apply_to_model_params", False)
            else self.local_model_params
        )

        return feedback, model_params

    def generate_feedback(self, peer):
        """
        Generate feedback about a peer's contribution.
        """
        if self.is_malicious:
            return self.generate_malicious_feedback()
        else:
            accuracy_with_peer = np.random.uniform(0.7, 1.0)
            accuracy_without_peer = np.random.uniform(0.5, 0.9)
            feedback = accuracy_with_peer - accuracy_without_peer
            return (
                self.add_noise_to_trust(feedback)
                if self.noise_config and self.noise_config.get("apply_to_trust", False)
                else feedback
            )

    def generate_malicious_feedback(self):
        """
        Generate misleading feedback using the specified distribution.
        """
        if self.malicious_distribution == "uniform":
            return np.random.uniform(-0.5, 0.0)
        elif self.malicious_distribution == "normal":
            return np.random.normal(loc=-0.2, scale=0.1)
        else:
            raise ValueError("Unsupported distribution: " + self.malicious_distribution)

    def add_noise_to_trust(self, value):
        """
        Add noise to trust/belief messages based on the selected noise type.
        """
        noise_type = self.noise_config["noise_type"]
        if noise_type == "speckle":
            return value * (1 + self.generate_noise(noise_type, ()))
        return value + self.generate_noise(noise_type, ())

    def add_noise_to_params(self, params):
        """
        Add noise to local model parameters based on the selected noise type.
        """
        noise_type = self.noise_config["noise_type"]
        if noise_type == "speckle":
            return params * (1 + self.generate_noise(noise_type, params.shape))
        return params + self.generate_noise(noise_type, params.shape)

    def generate_noise(self, noise_type, shape):
        """
        Generate noise based on the selected noise type.
        """
        if noise_type == "gaussian":
            return np.random.normal(0, 0.1, size=shape)
        elif noise_type == "uniform":
            return np.random.uniform(-0.1, 0.1, size=shape)
        elif noise_type == "binomial":
            return np.random.binomial(1, 0.1, size=shape) - 0.5
        elif noise_type == "poisson":
            return np.random.poisson(0.1, size=shape) - 0.05
        elif noise_type == "exponential":
            return np.random.exponential(0.1, size=shape)
        elif noise_type == "speckle":
            return np.random.normal(0, 0.1, size=shape)  # Speckle noise is multiplicative
        elif noise_type == "salt_and_pepper":
            noise = np.random.choice([0, 1], size=shape, p=[0.9, 0.1])
            return noise * np.random.uniform(-1, 1, size=shape)
        elif noise_type == "laplace":
            return np.random.laplace(0, 0.1, size=shape)
        elif noise_type == "cauchy":
            return np.random.standard_cauchy(size=shape)
        else:
            raise ValueError(f"Unsupported noise type: {noise_type}")

    def receive_feedback(self, sender_id, feedback, model_params):
        """
        Receive feedback and model parameters from a peer.
        """
        self.received_feedback.append((sender_id, feedback, model_params))

    def update_trust_scores(self):
        """
        Update trust scores based on received feedback.
        """
        for sender_id, feedback, model_params in self.received_feedback:
            for target_id, m_jk in feedback.items():
                T_ij = self.trust_scores.get(sender_id, 1.0)
                T_ik = self.trust_scores.get(target_id, 1.0)
                self.trust_scores[target_id] = T_ik + self.alpha * T_ij * m_jk
        self.received_feedback = []
