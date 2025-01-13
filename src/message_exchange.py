# # import simpy

# # class MessageExchange:
# #     """
# #     Manages the message exchange process between nodes in the network.

# #     mode = 'p2p' or 'server'
# #       - p2p: all nodes send messages to all peers directly.
# #       - server: one node (e.g., node_id=0) is designated as the server.
# #     """

# #     def __init__(self, env, nodes, message_log, mode='p2p'):
# #         self.env = env
# #         self.nodes = nodes
# #         self.message_log = message_log
# #         self.mode = mode
# #         self.action = env.process(self.run())

# #     def run(self):
# #         while True:
# #             if self.mode == 'p2p':
# #                 self.run_p2p_mode()
# #             else:
# #                 self.run_server_mode()

# #             yield self.env.timeout(1)

# #             # After message exchange, update trust
# #             for node in self.nodes:
# #                 node.update_trust()

# #     def run_p2p_mode(self):
# #         # Each node sends messages to peers
# #         for node in self.nodes:
# #             messages = node.send_message()
# #             for peer_id, msg in messages.items():
# #                 self.log_message(node.node_id, peer_id, msg, node.is_malicious)
# #                 peer_node = self.get_node_by_id(peer_id)
# #                 if peer_node:
# #                     peer_node.receive_message(node.node_id, msg)

# #     def run_server_mode(self):
# #         # In server mode, assume node 0 is the server
# #         server_node = self.get_node_by_id(0)
# #         if server_node is None:
# #             raise ValueError("No server node found. Ensure node with node_id=0 is present.")

# #         # Non-server nodes send messages to the server
# #         for node in self.nodes:
# #             if node.node_id != 0:
# #                 messages = node.send_message()
# #                 # In server mode, the 'peers' of a non-server node might just be [server_node]
# #                 for srv_id, msg in messages.items():
# #                     self.log_message(node.node_id, srv_id, msg, node.is_malicious)
# #                     if srv_id == 0:
# #                         server_node.receive_message(node.node_id, msg)

# #         # The server can then process these messages and optionally broadcast something back
# #         # For simplicity, we just let the server send its own messages to all others
# #         # (or do nothing if not needed)
# #         server_msgs = server_node.send_message()
# #         for peer_id, msg in server_msgs.items():
# #             self.log_message(server_node.node_id, peer_id, msg, server_node.is_malicious)
# #             peer_node = self.get_node_by_id(peer_id)
# #             if peer_node:
# #                 peer_node.receive_message(server_node.node_id, msg)

# #     def get_node_by_id(self, node_id):
# #         for node in self.nodes:
# #             if node.node_id == node_id:
# #                 return node
# #         return None

# #     def log_message(self, sender, receiver, msg, is_malicious):
# #         self.message_log.append({
# #             'time': self.env.now,
# #             'sender': sender,
# #             'receiver': receiver,
# #             'message': msg,
# #             'is_malicious_sender': is_malicious
# #         })
# class MessageExchange:
#     """
#     Handles the trust and belief exchange process in the network.
#     """

#     def __init__(self, env, nodes, mode='p2p', server_id=0, message_log=None):
#         self.env = env
#         self.nodes = nodes
#         self.mode = mode
#         self.server_id = server_id
#         self.server = self.get_node_by_id(server_id) if mode == 'server' else None
#         self.message_log = message_log if message_log is not None else []  # Initialize message log
#         self.action = env.process(self.run())

#     def run(self):
#         """
#         Simulation loop for message exchange.
#         """
#         while True:
#             if self.mode == 'p2p':
#                 self.peer_to_peer_exchange()
#             elif self.mode == 'server':
#                 self.server_based_exchange()
#             else:
#                 raise ValueError("Unsupported mode: " + self.mode)
#             yield self.env.timeout(1)  # Simulate a time step
#             for node in self.nodes:
#                 node.update_trust_scores()

#     def peer_to_peer_exchange(self):
#         """
#         Peer-to-peer message exchange.
#         """
#         for node in self.nodes:
#             feedback = node.send_feedback()
#             for peer in node.peers:
#                 peer.receive_feedback(node.node_id, feedback)
#                 # Log the message
#                 self.message_log.append({
#                     'time': self.env.now,
#                     'sender': node.node_id,
#                     'receiver': peer.node_id,
#                     'feedback': feedback
#                 })

#     def server_based_exchange(self):
#         """
#         Server-based message exchange.
#         """
#         all_feedback = {}
#         for node in self.nodes:
#             if node.node_id != self.server_id:
#                 feedback = node.send_feedback()
#                 self.server.receive_feedback(node.node_id, feedback)
#                 all_feedback[node.node_id] = feedback
#                 # Log the message
#                 self.message_log.append({
#                     'time': self.env.now,
#                     'sender': node.node_id,
#                     'receiver': self.server_id,
#                     'feedback': feedback
#                 })
#         # Server broadcasts aggregated feedback to all nodes
#         for node in self.nodes:
#             if node.node_id != self.server_id:
#                 node.receive_feedback(self.server_id, all_feedback)
#                 # Log the broadcast
#                 self.message_log.append({
#                     'time': self.env.now,
#                     'sender': self.server_id,
#                     'receiver': node.node_id,
#                     'feedback': all_feedback
#                 })

#     def get_node_by_id(self, node_id):
#         """
#         Retrieve a node by its ID.
#         """
#         for node in self.nodes:
#             if node.node_id == node_id:
#                 return node
#         return None

class MessageExchange:
    """
    Handles the trust and belief exchange process in the network.
    """

    def __init__(self, env, nodes, mode='p2p', server_id=0, message_log=None):
        self.env = env
        self.nodes = nodes
        self.mode = mode
        self.server_id = server_id
        self.server = self.get_node_by_id(server_id) if mode == 'server' else None
        self.message_log = message_log if message_log is not None else []
        self.action = env.process(self.run())

    def run(self):
        """
        Simulation loop for message exchange.
        """
        while True:
            if self.mode == 'p2p':
                self.peer_to_peer_exchange()
            elif self.mode == 'server':
                self.server_based_exchange()
            yield self.env.timeout(1)
            for node in self.nodes:
                node.update_trust_scores()

    def peer_to_peer_exchange(self):
        """
        Peer-to-peer message exchange.
        """
        for node in self.nodes:
            feedback, model_params = node.send_feedback()
            for peer in node.peers:
                peer.receive_feedback(node.node_id, feedback, model_params)
                self.log_message(node.node_id, peer.node_id, feedback, model_params)

    def server_based_exchange(self):
        """
        Server-based message exchange.
        """
        aggregated_feedback = {}
        aggregated_model_params = []
        for node in self.nodes:
            if node.node_id != self.server_id:
                feedback, model_params = node.send_feedback()
                self.server.receive_feedback(node.node_id, feedback, model_params)
                aggregated_feedback[node.node_id] = feedback
                aggregated_model_params.append(model_params)
                self.log_message(node.node_id, self.server_id, feedback, model_params)

        # Server broadcasts aggregated data
        for node in self.nodes:
            if node.node_id != self.server_id:
                node.receive_feedback(self.server_id, aggregated_feedback, aggregated_model_params)

    def log_message(self, sender_id, receiver_id, feedback, model_params):
        """
        Log messages exchanged during the simulation.
        """
        self.message_log.append({
            'sender': sender_id,
            'receiver': receiver_id,
            'feedback': feedback,
            'model_params': model_params
        })

    def get_node_by_id(self, node_id):
        """
        Retrieve a node by its ID.
        """
        return next((node for node in self.nodes if node.node_id == node_id), None)
