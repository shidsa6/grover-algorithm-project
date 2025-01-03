import numpy as np
from qiskit import QuantumCircuit, Aer, transpile, QuantumRegister, ClassicalRegister
from qiskit.visualization import plot_histogram
from qiskit.circuit.library import GroverOperator
import os
import glob
import matplotlib.pyplot as plt
import seaborn as sns

# Ensure examples directory exists
os.makedirs("examples", exist_ok=True)

# Simulator
simulator = Aer.get_backend('aer_simulator')

# Add professional styling configuration
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("deep")
plt.rcParams.update({
    'font.size': 12,
    'axes.labelsize': 14,
    'axes.titlesize': 16,
    'figure.titlesize': 18,
    'figure.figsize': [12, 8],
    'figure.dpi': 300
})

# Define the GroverAlgorithm class
class GroverAlgorithm:
    def create_oracle(self, n, s_list):
        # Input validation
        if not isinstance(n, int) or n <= 0:
            raise ValueError("Number of qubits must be a positive integer")
        if not s_list or not isinstance(s_list, list):
            raise ValueError("Solutions must be provided as a non-empty list")
        
        size = 2 ** n
        if any(not isinstance(s, int) or s < 0 or s >= size for s in s_list):
            raise ValueError(f"All solutions must be integers in range [0, {size-1}]")
        
        # Create oracle matrix
        oracle = np.eye(size)
        for idx in s_list:
            oracle[idx, idx] = -1
        
        # Convert to quantum circuit
        oracle_circuit = QuantumCircuit(n)
        try:
            oracle_circuit.unitary(oracle, range(n), label="Oracle")
        except Exception as e:
            raise RuntimeError(f"Failed to create oracle circuit: {str(e)}")
        
        return oracle_circuit

    def calculate_iterations(self, N, M):
        if M >= N:
            return 1
        iterations = int(np.floor((np.pi / 4) * np.sqrt(N / M)))
        return max(1, iterations)  # Ensure at least one iteration

    def create_diffusion(self, n):
        """Creates the diffusion operator for Grover's algorithm."""
        if not isinstance(n, int) or n <= 0:
            raise ValueError("Number of qubits must be a positive integer")
            
        qc = QuantumCircuit(n)
        
        # Apply H gates
        for i in range(n):
            qc.h(i)
            
        # Apply X gates
        for i in range(n):
            qc.x(i)
            
        # Multi-controlled Z implementation
        qc.h(n-1)
        qc.mcx(list(range(n-1)), n-1)  # Using mcx consistently
        qc.h(n-1)
        
        # Reverse X and H gates
        for i in range(n):
            qc.x(i)
        for i in range(n):
            qc.h(i)
            
        return qc

    def create_circuit(self, n, solutions):
        try:
            # Validate inputs first
            if not isinstance(n, int) or n <= 0:
                raise ValueError("Number of qubits must be a positive integer")
            
            size = 2 ** n
            if any(not isinstance(s, int) or s < 0 or s >= size for s in solutions):
                raise ValueError(f"All solutions must be integers in range [0, {size-1}]")
                
            # Create circuit components
            oracle_circuit = self.create_oracle(n, solutions)
            grover_operator = GroverOperator(oracle_circuit)
            
            # Calculate optimal number of iterations
            k = self.calculate_iterations(2**n, len(solutions))
            
            # Create quantum and classical registers
            qn = QuantumRegister(n, 'qn')
            c = ClassicalRegister(n, 'c')
            qc = QuantumCircuit(qn, c)
            
            # Initialize superposition
            qc.h(qn)
            
            # Apply Grover iterations
            for _ in range(k):
                qc.append(grover_operator, qn)
            
            # Measure results
            qc.measure(qn, c)
            
            return qc
            
        except ValueError as e:
            # Re-raise ValueError directly instead of wrapping in RuntimeError
            raise e
        except Exception as e:
            raise RuntimeError(f"Circuit creation failed: {str(e)}")

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
    """Generate a detailed Grover's Algorithm circuit with clear labels and operations."""
    n = 3  # Number of qubits for generic example
    qn = QuantumRegister(n, 'q')  # Named quantum register
    cr = ClassicalRegister(n, 'c')  # Named classical register
    qc = QuantumCircuit(qn, cr)
    
    # Initial state preparation
    qc.barrier(label='Initial State')
    for i in range(n):
        qc.h(i)
    qc.barrier(label='Superposition')
    
    # Grover Iteration (showing 1 iteration for clarity)
    qc.barrier(label='Begin Grover Iteration')
    
    # Oracle
    qc.barrier(label='Oracle')
    qc.append(GroverOperator(QuantumCircuit(n)), range(n))
    qc.barrier(label='Oracle Complete')
    
    # Diffusion Operator
    qc.barrier(label='Diffusion Operator')
    for i in range(n):
        qc.h(i)
    for i in range(n):
        qc.x(i)
    qc.barrier(label='Phase Inversion')
    qc.h(n-1)
    qc.mct(list(range(n-1)), n-1)
    qc.h(n-1)
    qc.barrier(label='Multi-Control Phase')
    for i in range(n):
        qc.x(i)
    for i in range(n):
        qc.h(i)
    qc.barrier(label='Diffusion Complete')
    
    # Measurement
    qc.barrier(label='Measurement')
    qc.measure(qn, cr)
    
    # Enhanced visualization with adjusted spacing
    fig = plt.figure(figsize=(24, 14))  # Increased figure size
    circuit_diagram = qc.draw(
        output='mpl',
        style={
            'backgroundcolor': '#FFFFFF',
            'linecolor': '#000000',
            'fontsize': 14,
            'subfontsize': 12,
            'displaycolor': {
                'oracle': '#FF0000',
                'diffusion': '#0000FF',
                'initialize': '#00FF00'
            },
            'gatefacecolor': '#EECFA1',
            'gatetextcolor': '#000000',
            'barrier': True,
            'showindex': True,
            'labelsize': 16,
            'margin': [3.0, 0.7, 0.7, 0.5]  # Increased margins [top, right, bottom, left]
        }
    )
    
    # Adjust title position and spacing
    plt.title("Detailed Grover's Algorithm Circuit\nWith State Preparation, Oracle, and Diffusion Operations", 
              pad=30, fontsize=18, fontweight='bold', y=1.05)
    
    # Adjust annotation positions
    plt.figtext(0.02, 0.95, "Circuit Components:", fontsize=12, fontweight='bold')
    plt.figtext(0.02, 0.92, "1. State Preparation (Green)", fontsize=10)
    plt.figtext(0.02, 0.89, "2. Oracle Operation (Red)", fontsize=10)
    plt.figtext(0.02, 0.86, "3. Diffusion Operator (Blue)", fontsize=10)
    plt.figtext(0.02, 0.83, "4. Measurement", fontsize=10)
    
    # Save with adjusted layout
    plt.tight_layout(rect=[0.05, 0, 0.95, 0.95])  # Adjust layout to prevent overlap
    circuit_path = "examples/generic_grover_circuit.png"
    plt.savefig(circuit_path, bbox_inches='tight', dpi=300, facecolor='white', pad_inches=0.5)
    plt.close()

def run_grover_algorithm(n, solutions, case_name):
    try:
        # Validate inputs
        if not isinstance(case_name, str) or not case_name:
            raise ValueError("Invalid case name")
            
        # Create and run circuit
        grover = GroverAlgorithm()
        circuit = grover.create_circuit(n, solutions)
        
        # Enhanced circuit visualization with adjusted spacing
        fig = plt.figure(figsize=(24, 14))  # Increased figure size
        circuit_diagram = circuit.draw(
            output='mpl',
            style={
                'backgroundcolor': '#FFFFFF',
                'linecolor': '#000000',
                'fontsize': 14,
                'subfontsize': 12,
                'displaycolor': {
                    'oracle': '#FF0000',
                    'diffusion': '#0000FF',
                    'initialize': '#00FF00'
                },
                'gatefacecolor': '#EECFA1',
                'gatetextcolor': '#000000',
                'barrier': True,
                'showindex': True,
                'labelsize': 16,
                'margin': [3.0, 0.7, 0.7, 0.5]  # Increased margins
            }
        )
        
        # Adjust title and text placement
        plt.title(f"{case_name}: Grover's Algorithm Circuit\n"
                 f"Searching for {len(solutions)} solution{'s' if len(solutions)>1 else ''} "
                 f"in {2**n} states\n"
                 f"Number of iterations: {circuit.count_ops().get('Q', 0)}", 
                 pad=30, fontsize=18, fontweight='bold', y=1.05)
        
        # Adjust solution information placement
        solution_text = "Target States: " + ", ".join([f"|{format(s, f'0{n}b')}⟩" for s in solutions])
        plt.figtext(0.02, 0.95, solution_text, fontsize=12, fontweight='bold')
        
        # Adjust circuit statistics placement
        stats_text = (f"Circuit Statistics:\n"
                     f"Qubits: {n}\n"
                     f"Gates: {sum(circuit.count_ops().values())}\n"
                     f"Depth: {circuit.depth()}")
        plt.figtext(0.02, 0.85, stats_text, fontsize=10)
        
        # Save with adjusted layout
        plt.tight_layout(rect=[0.05, 0, 0.95, 0.95])
        circuit_path = f"examples/{case_name}_circuit.png"
        plt.savefig(circuit_path, bbox_inches='tight', dpi=300, facecolor='white', pad_inches=0.5)
        plt.close()
        
        # Run simulation
        qc_t = transpile(circuit, simulator)
        result = simulator.run(qc_t, shots=3000).result()
        counts = result.get_counts()
        
        # Enhanced histogram visualization
        fig = plt.figure(figsize=(12, 8))
        plot_histogram(
            counts,
            figsize=(12, 8),
            bar_labels=True,
            title=f"{case_name}: Measurement Results Distribution\n{len(solutions)} solution{'s' if len(solutions)>1 else ''}"
        )
        plt.xlabel('Measured States', fontsize=14)
        plt.ylabel('Probability', fontsize=14)
        
        # Highlight solution states
        solution_states = [format(s, f'0{n}b') for s in solutions]
        ax = plt.gca()
        for patch, label in zip(ax.patches, ax.get_xticklabels()):
            if label.get_text() in solution_states:
                patch.set_facecolor('#2ecc71')  # Highlight solutions in green
        
        histogram_path = f"examples/{case_name}_histogram.png"
        plt.savefig(histogram_path, bbox_inches='tight', dpi=300)
        plt.close()
        
        # Validate results
        solution_states = [format(s, f'0{n}b') for s in solutions]
        total_prob = sum(counts.get(state, 0) for state in solution_states) / 3000
        if total_prob < 0.7:
            print(f"Warning: Low success probability ({total_prob:.2f}) for {case_name}")
            
        return counts
        
    except Exception as e:
        print(f"Error in {case_name}: {str(e)}")
        raise

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
    print("Grover's Algorithm Implementation v1.0")
    try:
        cleanup_examples_folder()
        generate_generic_circuit()
        
        test_cases = [
            (6, [36], "Case_1"),
            (6, [14, 23, 58], "Case_2"),
            (6, [4, 19, 24, 45, 55, 59, 61], "Case_3")
        ]
        
        for n, solutions, case_name in test_cases:
            print(f"\nRunning {case_name}...")
            results = run_grover_algorithm(n, solutions, case_name)
            print(f"Completed {case_name} successfully")
            
    except Exception as e:
        print(f"Program failed: {str(e)}")
        raise
