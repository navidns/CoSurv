# src/simulation/run_simulation.py

import simpy
from src.nodes import Node
from src.message_exchange import MessageExchange

def simulate_network(num_nodes=5, simulation_time=10):
    env = simpy.Environment()
    nodes = []

    # Create nodes
    for i in range(num_nodes):
        node = Node(node_id=i)
        nodes.append(node)

    # Set peers for each node
    for node in nodes:
        peers = [peer for peer in nodes if peer.node_id != node.node_id]
        node.set_peers(peers)

    # Initialize message exchange
    message_exchange = MessageExchange(env, nodes)

    # Run the simulation
    env.run(until=simulation_time)

    # Output the trust scores
    for node in nodes:
        print(f"Node {node.node_id} trust scores:")
        for peer_id, trust_score in node.trust_scores.items():
            print(f"  Trust in Node {peer_id}: {trust_score:.4f}")

if __name__ == "__main__":
    simulate_network()
