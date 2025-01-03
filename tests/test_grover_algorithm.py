import unittest
from qiskit import QuantumCircuit, execute, Aer
from qiskit.circuit.library import GroverOperator  # Import GroverOperator
import sys
import os

# Add the directory containing grover_algorithm to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from grover_algorithm import GroverAlgorithm  # Import your main class

class TestGroverAlgorithm(unittest.TestCase):
    def setUp(self):
        self.grover = GroverAlgorithm()
        self.simulator = Aer.get_backend('qasm_simulator')

    def test_oracle_single_solution(self):
        # Test oracle for single solution case
        oracle = self.grover.create_oracle(4, [1])  # 4 qubits, solution state 1
        self.assertIsInstance(oracle, QuantumCircuit)
        self.assertEqual(oracle.num_qubits, 4)

    def test_case1_single_solution(self):
        # Test Case 1: Single solution
        circuit = self.grover.create_circuit(4, [1])
        result = execute(circuit, self.simulator, shots=1000).result()
        counts = result.get_counts()
        # Check if the most frequent outcome is the solution
        most_frequent = max(counts, key=counts.get)
        self.assertEqual(most_frequent, '0001')

    def test_case2_three_solutions(self):
        # Test Case 2: Three solutions
        circuit = self.grover.create_circuit(4, [1, 3, 7])
        result = execute(circuit, self.simulator, shots=1000).result()
        counts = result.get_counts()
        # Verify solutions appear with significant probability
        total_prob = sum(counts[state] for state in ['0001', '0011', '0111'])
        self.assertGreater(total_prob / 1000, 0.7)  # 70% probability threshold

    def test_case3_seven_solutions(self):
        # Test Case 3: Seven solutions
        solutions = [1, 3, 5, 7, 9, 11, 13]
        circuit = self.grover.create_circuit(4, solutions)
        result = execute(circuit, self.simulator, shots=1000).result()
        counts = result.get_counts()
        
        # Verify circuit has correct number of iterations
        expected_iterations = self.grover.calculate_iterations(16, 7)
        
        # Count Grover iterations by looking for 'Q' operations
        iteration_count = sum(1 for instr, _, _ in circuit.data 
                            if instr.name == 'Q')
        
        # Add debug information
        print("Expected iterations:", expected_iterations)
        print("Actual iterations:", iteration_count)
        print("Circuit operations:", [instr.name for instr, _, _ in circuit.data])
        
        # Check if the number of Grover iterations matches expected
        self.assertGreater(iteration_count, 0, "No Grover iterations found in circuit")
        self.assertEqual(iteration_count, expected_iterations, 
                        f"Expected {expected_iterations} iterations, found {iteration_count}")

    def test_diffusion_operator(self):
        """Test diffusion operator creation"""
        n = 4
        diffusion = self.grover.create_diffusion(n)
        
        # Basic circuit checks
        self.assertIsInstance(diffusion, QuantumCircuit)
        self.assertEqual(diffusion.num_qubits, n)
        
        # Get all operations
        ops = [instr.name for instr, _, _ in diffusion.data]
        print("Diffusion operator gates:", ops)
        
        # Check essential gates are present
        essential_gates = {'h', 'x', 'mcx'}  # Changed 'mct' to 'mcx'
        found_gates = set(ops)
        self.assertTrue(essential_gates.issubset(found_gates), 
                       f"Missing gates. Expected at least {essential_gates}, found {found_gates}")
        
        # Check gate sequence length (4n + 3 gates total: n H-gates + n X-gates + MCT + n X-gates + n H-gates)
        expected_length = 4 * n + 3
        self.assertEqual(len(ops), expected_length,
                        f"Expected {expected_length} gates, found {len(ops)}")

    def test_invalid_input(self):
        """Test handling of invalid inputs"""
        # Test invalid solution value
        with self.assertRaises(ValueError) as cm:
            self.grover.create_circuit(4, [16])
        self.assertIn("range [0, 15]", str(cm.exception))
        
        # Test invalid number of qubits
        with self.assertRaises(ValueError):
            self.grover.create_circuit(-1, [1])
            
        # Test empty solutions list
        with self.assertRaises(ValueError):
            self.grover.create_circuit(4, [])

    def test_circuit_structure(self):
        """Test the complete structure of a simple Grover circuit"""
        circuit = self.grover.create_circuit(2, [1])  # 2 qubits, marking state |01⟩
        
        # Check initial state preparation
        init_hadamards = sum(1 for instr, _, _ in circuit.data[:2] 
                           if instr.name == 'h')
        self.assertEqual(init_hadamards, 2, "Circuit should start with Hadamard gates")
        
        # Verify Grover iteration structure
        ops = [instr.name for instr, _, _ in circuit.data]
        print("Full circuit operations:", ops)
        
        # Basic structural checks
        self.assertTrue('Q' in ops, "Circuit should contain Grover operator")
        self.assertTrue(ops.count('measure') >= 2, "Circuit should end with measurements")
        
        # Test the output for the marked state
        result = execute(circuit, self.simulator, shots=1000).result()
        counts = result.get_counts()
        print("Measurement results:", counts)
        self.assertIn('01', counts, "Marked state should be measured")
        self.assertGreater(counts.get('01', 0) / 1000, 0.5, 
                          "Marked state should have high probability")

    def test_multiple_iterations(self):
        """Test that multiple Grover iterations work correctly"""
        # Test with 3 qubits and multiple solutions
        solutions = [2, 5]
        circuit = self.grover.create_circuit(3, solutions)
        
        # Count Grover iterations
        iterations = sum(1 for instr, _, _ in circuit.data if instr.name == 'Q')
        expected = self.grover.calculate_iterations(8, 2)  # N=8 (3 qubits), M=2 solutions
        
        print(f"Circuit contains {iterations} Grover iterations (expected {expected})")
        self.assertEqual(iterations, expected, 
                        f"Wrong number of iterations: got {iterations}, expected {expected}")
        
        # Verify results
        result = execute(circuit, self.simulator, shots=1000).result()
        counts = result.get_counts()
        print("Results distribution:", counts)
        
        # Check both solutions are found with good probability
        total_prob = sum(counts.get(format(sol, f'0{3}b'), 0) 
                        for sol in solutions) / 1000
        self.assertGreater(total_prob, 0.7, 
                          "Solutions should appear with high total probability")

if __name__ == '__main__':
    unittest.main()