# Grover's Algorithm Implementation

## Overview
This project implements Grover's Algorithm using Qiskit, demonstrating quantum search capabilities through various test cases.

![Generic Grover Circuit](examples/generic_grover_circuit.png)
*Generic Grover's Algorithm Circuit Structure*

## Features
- Implementation of Grover's Algorithm with configurable parameters
- Multiple test cases demonstrating different search scenarios
- Visualization of quantum circuits and measurement results
- Comprehensive test suite
- Detailed documentation and discussion of results

## Implementation Examples

### Case 1: Single Solution Search
![Case 1 Circuit](examples/Case_1_circuit.png)
*Circuit for single solution search (state |100100⟩)*

![Case 1 Histogram](examples/Case_1_histogram.png)
*Measurement results showing high probability for target state*

### Case 2: Multiple Solutions
![Case 2 Circuit](examples/Case_2_circuit.png)
*Circuit for three-solution search (states |001110⟩, |010111⟩, |111010⟩)*

![Case 2 Histogram](examples/Case_2_histogram.png)
*Measurement results showing balanced distribution among three solutions*

### Case 3: Large Solution Set
![Case 3 Circuit](examples/Case_3_circuit.png)
*Circuit optimized for seven solutions*

![Case 3 Histogram](examples/Case_3_histogram.png)
*Measurement results demonstrating successful amplification of all seven states*

## Installation

1. Clone the repository:
```bash
git clone https://github.com/shidsa6/grover-algorithm-project.git
cd grover-algorithm-project
```

2. Create and activate a virtual environment:
```bash
python -m venv qiskit_env
source qiskit_env/bin/activate  # On Windows: qiskit_env\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the main implementation:
```bash
python grover_algorithm.py
```

2. Run tests:
```bash
python -m unittest tests/test_grover_algorithm.py
```

## Project Structure
```
grover_algorithm/
├── README.md
├── requirements.txt
├── LICENSE
├── grover_algorithm.py
├── discussion.md
├── examples/          # Contains all circuit diagrams and histograms
└── tests/
    └── test_grover_algorithm.py
```

## Results
The implementation includes three test cases:
- Case 1: Single solution search
- Case 2: Three-solution search
- Case 3: Seven-solution search

Results and visualizations are automatically generated in the `examples/` directory.

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
