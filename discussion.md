# Discussion of Results

## Overview

This document provides insights into the results obtained from the implementation of Grover’s Algorithm for three different test cases. The algorithm is tested with varying numbers of solutions to demonstrate its efficiency and correctness.

---

## **Case 1: Single Solution**

### Parameters:
- **Number of Qubits**: 6
- **Number of Solutions**: 1 (State 36)

### Results:
- **Number of Iterations**: 6
- **Measurement Results**:
  - The histogram shows a high probability for the solution state: **36** (`100100` in binary).
  - Other states have significantly lower probabilities, indicating the success of Grover's Algorithm in amplifying the correct solution.

### Observations:
- The number of iterations calculated using the formula \( k = \lfloor \frac{\pi}{4} \sqrt{\frac{2^n}{M}} \rfloor \) maximized the probability of measuring the correct solution state.
- The algorithm efficiently amplified the single solution state while suppressing all other states.

---

## **Case 2: Three Solutions**

### Parameters:
- **Number of Qubits**: 6
- **Number of Solutions**: 3 (States: 14, 23, 58)

### Results:
- **Number of Iterations**: 3
- **Measurement Results**:
  - The histogram displays three peaks corresponding to the three solution states:
    - **14** (`001110` in binary)
    - **23** (`010111` in binary)
    - **58** (`111010` in binary)
  - Non-solution states have close-to-zero probabilities.

### Observations:
- The calculated number of iterations successfully amplified all three solutions, showing Grover’s Algorithm’s scalability for multiple solutions.
- Each solution has a roughly equal probability, demonstrating the fairness of the amplification process.

---

## **Case 3: Seven Solutions**

### Parameters:
- **Number of Qubits**: 6
- **Number of Solutions**: 7 (States: 4, 19, 24, 45, 55, 59, 61)

### Results:
- **Number of Iterations**: 2
- **Measurement Results**:
  - The histogram shows peaks at the seven solution states:
    - **4** (`000100`)
    - **19** (`010011`)
    - **24** (`011000`)
    - **45** (`101101`)
    - **55** (`110111`)
    - **59** (`111011`)
    - **61** (`111101`)
  - Non-solution states have near-zero probabilities.

### Observations:
- Fewer iterations were needed due to the higher number of solutions.
- Grover's Algorithm efficiently amplified all seven solution states, even with reduced iterations.

---

## **Overall Observations**

1. **Efficiency**:
   - The number of iterations required decreases as the number of solutions increases.
   - This demonstrates Grover's Algorithm's adaptability for different problem sizes.

2. **Accuracy**:
   - The algorithm consistently amplifies the correct solution states while suppressing non-solutions.
   - Histograms clearly highlight the success of the algorithm in finding solutions.

3. **Scalability**:
   - Grover's Algorithm performs equally well with a single solution or multiple solutions.
   - The visualizations and results confirm its effectiveness for various scenarios.

---

## Conclusion

The implementation of Grover’s Algorithm successfully demonstrates its quadratic speedup and accuracy for unstructured search problems. The results align with theoretical expectations, making this a robust demonstration of quantum computing principles.
