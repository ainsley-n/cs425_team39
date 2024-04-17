import unittest
import os
import random_circuit_generator
from lcapy import Circuit

class TestRandomCircuitGeneration(unittest.TestCase):
    def setUp(self):
        #get the directory of the current file
        self.dirname = os.path.dirname(__file__)
        #remove the 'Tests' directory from the path
        self.dirname = os.path.dirname(self.dirname)
    
    def test_generate_random_circuit(self):
        # Test that the random circuit generator creates a circuit
        circuit = random_circuit_generator.generate_random_circuit()
        self.assertIsInstance(circuit, Circuit)


if __name__ == '__main__':
    unittest.main()