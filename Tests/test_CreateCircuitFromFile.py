import unittest
from Circuit_Analyzer import create_circuit_from_file
import os



class TestCreateCircuitFromFile(unittest.TestCase):
    def setUp(self):
        # Get the directory of the current file
        self.dirname = os.path.dirname(__file__)
        # Get the directory of the parent directory
        self.dirname = os.path.dirname(self.dirname)
    
    def test_valid_netlist(self):
        filename = os.path.join(self.dirname, 'Circuits\circuit1.txt')
        try:
            test_circuit = create_circuit_from_file(filename)
        except:
            self.fail("create_circuit_from_file() raised exception unexpectedly")
    
    def test_invalid_netlist(self):
        filename = os.path.join(self.dirname, 'Circuits\\bad_circuit.txt')
        with self.assertRaises(ValueError):
            test_circuit = create_circuit_from_file(filename)

    def test_invalid_filepath(self):
        filename = os.path.join(self.dirname, 'Circuits\\bad_path.txt')
        with self.assertRaises(FileNotFoundError):
            test_circuit = create_circuit_from_file(filename)
        

if __name__ == '__main__':
    unittest.main()