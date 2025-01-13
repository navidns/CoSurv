import simpy
import random
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from src.nodes import Node
from src.message_exchange import MessageExchange

def simulate_network(num_nodes=5, simulation_time=10, malicious_fraction=0.4, mode='p2p', malicious_distribution='uniform'):
    """
    Simulate a federated learning setup with trust and optional malicious behavior.

    Parameters:
    - num_nodes: number of nodes in the network
    - simulation_time: how many time steps to simulate
    - malicious_fraction: fraction of nodes that are malicious
    - mode: 'p2p' or 'server' for architecture type
    - malicious_distribution: distribution type for malicious noise ('uniform' or 'normal')
    """

    env = simpy.Environment()
    nodes = []

    # Create nodes
    for i in range(num_nodes):
        node = Node(node_id=i)
        nodes.append(node)

    # Set peers
    if mode == 'p2p':
        # Each node sees others as peers
        for node in nodes:
            peers = [p for p in nodes if p.node_id != node.node_id]
            node.set_peers(peers)
    else:
        # Server mode:
        # Let's assume node 0 is the server.
        # Other nodes have only the server as peer.
        server_node = nodes[0]
        non_server_nodes = nodes[1:]
        for node in non_server_nodes:
            node.set_peers([server_node])
        # The server considers all others as peers (or none, depending on design)
        server_node.set_peers([p for p in nodes if p.node_id != 0])

    # Select some nodes as malicious
    num_malicious = int(num_nodes * malicious_fraction)
    malicious_nodes = random.sample(nodes, num_malicious)
    for m_node in malicious_nodes:
        m_node.is_malicious = True
        m_node.malicious_distribution = malicious_distribution

    # Set up message logging
    message_log = []

    # Start message exchange
    message_exchange = MessageExchange(env, nodes, message_log, mode=mode)
    env.run(until=simulation_time)

    # Print trust scores after simulation
    print("Final Trust Scores:")
    for node in nodes:
        print(f"Node {node.node_id} (malicious={node.is_malicious}) trust scores:")
        for pid, tscore in node.trust_scores.items():
            print(f"  Trust in Node {pid}: {tscore:.4f}")

    # Analyze messages
    print("\nMessages Sent During Simulation:")
    for entry in message_log:
        sender = entry['sender']
        receiver = entry['receiver']
        msg = entry['message']
        mal = entry['is_malicious_sender']
        print(f"Time {entry['time']}: Node {sender} (mal={mal}) -> Node {receiver}: {msg:.4f}")

if __name__ == "__main__":
    # Example runs:
    # P2P mode with uniform malicious distribution
    simulate_network(num_nodes=5, simulation_time=5, malicious_fraction=0.4, mode='p2p', malicious_distribution='uniform')
    
    # Server-based mode with normal malicious distribution
    # simulate_network(num_nodes=5, simulation_time=5, malicious_fraction=0.4, mode='server', malicious_distribution='normal')
