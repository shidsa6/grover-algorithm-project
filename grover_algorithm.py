import numpy as np
from qiskit import QuantumCircuit, Aer, transpile, QuantumRegister, ClassicalRegister
from qiskit.visualization import plot_histogram
from qiskit.circuit.library import GroverOperator
import os
import glob

# Ensure examples directory exists
os.makedirs("examples", exist_ok=True)

# Simulator
simulator = Aer.get_backend('aer_simulator')

def grover_oracle_from_list(n, s_list):
    size = 2 ** n
    oracle = np.eye(size)
    for idx in s_list:
        if 0 <= idx < size:
            oracle[idx, idx] = -1
        else:
            raise ValueError(f"Index {idx} is out of range for a 2^{n} space.")
    return oracle

def oracle_to_circuit(oracle_matrix, n):
    oracle_circuit = QuantumCircuit(n)
    oracle_circuit.unitary(oracle_matrix, range(n), label="Oracle")
    return oracle_circuit

def generate_generic_circuit():
    """
    Generates a generic Grover's Algorithm circuit diagram for visualization.
    This is independent of specific cases or solutions.
    """
    n = 3  # Number of qubits for generic example
    qc = QuantumCircuit(n, n)
    
    # Apply Hadamard gates
    qc.h(range(n))
    
    # Add a placeholder for the oracle
    qc.barrier()
    qc.append(GroverOperator(QuantumCircuit(n)), range(n))
    qc.barrier()
    
    # Apply diffusion operator (Hadamard + X + multi-controlled Z + X + Hadamard)
    qc.h(range(n))
    qc.x(range(n))
    qc.h(n - 1)
    qc.mct(list(range(n - 1)), n - 1)  # Multi-controlled Toffoli
    qc.h(n - 1)
    qc.x(range(n))
    qc.h(range(n))
    qc.barrier()
    
    # Measure the qubits
    qc.measure_all()
    
    # Save the generic circuit diagram
    circuit_path = "examples/generic_grover_circuit.png"
    qc.draw(output='mpl').savefig(circuit_path)
    print(f"Generic circuit diagram saved to {circuit_path}")

def run_grover_algorithm(n, solutions, case_name):
    oracle_matrix = grover_oracle_from_list(n, solutions)
    oracle_circuit = oracle_to_circuit(oracle_matrix, n)
    grover_operator = GroverOperator(oracle_circuit)
    k = int(np.floor((np.pi / 4) * np.sqrt(2**n / len(solutions))))
    qn = QuantumRegister(n, 'qn')
    c = ClassicalRegister(n, 'c')
    qc = QuantumCircuit(qn, c)
    qc.h(qn)
    for _ in range(k):
        qc.append(grover_operator, qn)
    qc.measure(qn, c)
    circuit_path = f"examples/{case_name}_circuit.png"
    qc.draw(output='mpl').savefig(circuit_path)
    print(f"Circuit diagram saved to {circuit_path}")
    qc_t = transpile(qc, simulator)
    result = simulator.run(qc_t, shots=3000).result()
    counts = result.get_counts()
    histogram_path = f"examples/{case_name}_histogram.png"
    plot_histogram(counts, title=f"{case_name} Results").savefig(histogram_path)
    print(f"Histogram saved to {histogram_path}")
    return counts

def cleanup_examples_folder():
    """
    Removes duplicate or redundant images from the 'examples/' folder.
    Ensures only the latest outputs remain.
    """
    files = glob.glob("examples/*.png")
    if files:
        print("Cleaning up 'examples/' folder...")
        for file in files:
            if os.path.exists(file):
                os.remove(file)
        print("Old files removed.")
    else:
        print("No files to clean up.")

# Main execution
if __name__ == "__main__":
    # Clean up old files
    cleanup_examples_folder()
    
    # Generate generic circuit diagram
    generate_generic_circuit()
    
    # Case 1: Single solution
    case_1_solutions = [36]
    run_grover_algorithm(n=6, solutions=case_1_solutions, case_name="Case_1")

    # Case 2: Three solutions
    case_2_solutions = [14, 23, 58]
    run_grover_algorithm(n=6, solutions=case_2_solutions, case_name="Case_2")

    # Case 3: Seven solutions
    case_3_solutions = [4, 19, 24, 45, 55, 59, 61]
    run_grover_algorithm(n=6, solutions=case_3_solutions, case_name="Case_3")
