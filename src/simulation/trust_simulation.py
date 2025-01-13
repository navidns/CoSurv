import simpy
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from src.nodes import Node
from src.message_exchange import MessageExchange

def simulate_network(num_nodes=5, simulation_time=10, mode='p2p', malicious_fraction=0.3):
    env = simpy.Environment()
    nodes = []

    # Create nodes
    for i in range(num_nodes):
        node = Node(node_id=i)
        nodes.append(node)

    # Set peers
    for node in nodes:
        node.set_peers([peer for peer in nodes if peer.node_id != node.node_id])

    # Mark malicious nodes
    num_malicious = int(num_nodes * malicious_fraction)
    malicious_nodes = nodes[:num_malicious]  # For simplicity, first nodes are malicious
    for m_node in malicious_nodes:
        m_node.is_malicious = True
        m_node.malicious_distribution = 'normal'

    # Create a message log to store communication data
    message_log = []

    # Start message exchange
    message_exchange = MessageExchange(env, nodes, mode=mode, message_log=message_log)
    env.run(until=simulation_time)

    # Display results
    for node in nodes:
        print(f"Node {node.node_id} (malicious={node.is_malicious}):")
        for target, trust in node.trust_scores.items():
            print(f"  Trust in Node {target}: {trust:.4f}")

    # Display message log (optional)
    print("\nMessage Log:")
    for entry in message_log:
        print(entry)

if __name__ == "__main__":
    # Default simulation parameters for standalone execution
    simulate_network(num_nodes=5, simulation_time=10, mode='p2p', malicious_fraction=0.3)
