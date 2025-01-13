import simpy
import sys
import random
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from src.nodes import Node
from src.message_exchange import MessageExchange



def simulate_network(
    num_nodes=5,
    simulation_time=10,
    mode="p2p",
    malicious_fraction=0.3,
    noise_config=None,
):
    """
    Simulate the federated learning environment with trust and belief updates,
    optionally adding noise and testing malicious behavior.

    Parameters:
        num_nodes (int): Total number of nodes in the network.
        simulation_time (int): Duration of the simulation.
        mode (str): 'p2p' for peer-to-peer or 'server' for server-based.
        malicious_fraction (float): Fraction of nodes that are malicious.
        noise_config (dict): Configuration for adding noise (optional).

    Returns:
        None
    """
    env = simpy.Environment()
    nodes = []

    # Create nodes with optional noise configuration
    for i in range(num_nodes):
        is_noisy = noise_config and random.random() < noise_config.get("noise_fraction", 0)
        node = Node(node_id=i, noise_config=noise_config if is_noisy else None)
        nodes.append(node)

    # Set peers for each node
    for node in nodes:
        node.set_peers([peer for peer in nodes if peer.node_id != node.node_id])

    # Mark malicious nodes
    num_malicious = int(num_nodes * malicious_fraction)
    for i in range(num_malicious):
        nodes[i].is_malicious = True

    # Initialize message exchange
    message_log = []
    message_exchange = MessageExchange(env, nodes, mode=mode, message_log=message_log)
    env.run(until=simulation_time)

    # Display results
    print("\n--- Simulation Results ---")
    for node in nodes:
        print(f"Node {node.node_id} (malicious={node.is_malicious}):")
        for target, trust in node.trust_scores.items():
            print(f"  Trust in Node {target}: {trust:.4f}")
    print("\n--- Message Log ---")
    for log in message_log:
        print(log)


if __name__ == "__main__":
    # Example noise configuration
    noise_config = {
        "noise_type": "uniform",  # Choose: gaussian, uniform, binomial, poisson, etc.
        "apply_to_model_params": True,  # Add noise to model parameters
        "apply_to_trust": True,  # Add noise to trust values
        "noise_fraction": 0.3,  # Fraction of nodes affected by noise
    }

    # Run simulation
    simulate_network(
        num_nodes=10,
        simulation_time=20,
        mode="p2p",  # Choose: 'p2p' or 'server'
        malicious_fraction=0.2,
        noise_config=noise_config,
    )
