# tests/test_simulation.py

import unittest
from src.simulation.run_simulation import simulate_network

class TestSimulation(unittest.TestCase):

    def test_simulate_network(self):
        # Run simulation for a small network
        simulate_network(num_nodes=3, simulation_time=5)
        # Since the function prints output, we can manually check the console

# Note: For automated testing, consider capturing stdout and asserting on outputs.
