"""
quantum_generator.py - Functions for generating and manipulating entangled quantum states

This module provides functionality for creating various entangled states (Bell states, GHZ states),
measuring them in different bases, and analyzing the resulting correlations.
"""

from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
from qiskit_aer.backends.aer_simulator import AerSimulator
from qiskit.visualization import plot_histogram, plot_bloch_multivector
from qiskit.quantum_info import Statevector, partial_trace, state_fidelity
import numpy as np
from typing import Dict, List, Tuple, Optional, Union, Any


class EntanglementGenerator:
    """
    A class to generate and manipulate entangled quantum states.
    """
    
    def __init__(self):
        """Initialize the entanglement generator."""
        self.simulator = Aer.get_backend('aer_simulator')
        self.statevector_sim = Aer.get_backend('statevector_simulator')
        self.reset_state()
    
    def reset_state(self):
        """Reset the quantum state."""
        self.circuit = None
        self.statevector = None
        self.measured_results = None
    
    def create_bell_state(self, bell_type: str = 'phi_plus') -> QuantumCircuit:
        """
        Create a Bell state.
        
        Args:
            bell_type: Type of Bell state ('phi_plus', 'phi_minus', 'psi_plus', 'psi_minus')
            
        Returns:
            Quantum circuit with the Bell state
        """
        # Create a circuit with 2 qubits
        circuit = QuantumCircuit(2, 2)
        
        # Apply Hadamard to the first qubit
        circuit.h(0)
        
        # Apply CNOT with control=first qubit, target=second qubit
        circuit.cx(0, 1)
        
        # For different Bell states, apply additional gates
        if bell_type == 'phi_minus':
            # |Φ-⟩ = (|00⟩ - |11⟩)/√2
            circuit.z(1)
        elif bell_type == 'psi_plus':
            # |Ψ+⟩ = (|01⟩ + |10⟩)/√2
            circuit.x(1)
        elif bell_type == 'psi_minus':
            # |Ψ-⟩ = (|01⟩ - |10⟩)/√2
            circuit.x(1)
            circuit.z(1)
        
        self.circuit = circuit
        self._update_statevector()
        
        return circuit
    
    def create_ghz_state(self, num_qubits: int = 3) -> QuantumCircuit:
        """
        Create a GHZ state with the specified number of qubits.
        
        Args:
            num_qubits: Number of qubits in the GHZ state
            
        Returns:
            Quantum circuit with the GHZ state
        """
        # Create a circuit with the specified number of qubits
        circuit = QuantumCircuit(num_qubits, num_qubits)
        
        # Apply Hadamard to the first qubit
        circuit.h(0)
        
        # Apply CNOT gates to entangle all qubits
        for i in range(1, num_qubits):
            circuit.cx(0, i)
        
        self.circuit = circuit
        self._update_statevector()
        
        return circuit
    
    def create_w_state(self, num_qubits: int = 3) -> QuantumCircuit:
        """
        Create a W state with the specified number of qubits.
        
        Args:
            num_qubits: Number of qubits in the W state
            
        Returns:
            Quantum circuit with the W state
        """
        # This is a simplified implementation for 3 qubits
        # For more qubits, a more complex circuit would be needed
        if num_qubits != 3:
            raise ValueError("This implementation only supports 3-qubit W states")
        
        # Create a circuit with 3 qubits
        circuit = QuantumCircuit(3, 3)
        
        # Apply gates to create the W state |001⟩ + |010⟩ + |100⟩
        # This is a simplified approach
        circuit.ry(2 * np.arccos(1/np.sqrt(3)), 0)
        circuit.cx(0, 1)
        circuit.x(0)
        circuit.ccx(0, 1, 2)
        circuit.x(0)
        
        self.circuit = circuit
        self._update_statevector()
        
        return circuit
    
    def _update_statevector(self):
        """Update the statevector based on the current circuit."""
        if self.circuit is None:
            self.statevector = None
            return
        
        # Execute the circuit on the statevector simulator
        transpiled_circuit = transpile(self.circuit, self.statevector_sim)
        job = self.statevector_sim.run(transpiled_circuit)
        result = job.result()
        self.statevector = result.get_statevector()
    
    def measure_in_basis(self, basis: str = 'Z', qubit_indices: Optional[List[int]] = None) -> Dict[str, int]:
        """
        Measure the qubits in the specified basis.
        
        Args:
            basis: Measurement basis ('X', 'Y', 'Z')
            qubit_indices: Indices of qubits to measure (default: all qubits)
            
        Returns:
            Dictionary of measurement results
        """
        if self.circuit is None:
            raise ValueError("No circuit has been created")
        
        # Create a copy of the circuit for measurement
        meas_circuit = self.circuit.copy()
        num_qubits = meas_circuit.num_qubits
        
        # If no qubit indices are specified, measure all qubits
        if qubit_indices is None:
            qubit_indices = list(range(num_qubits))
        
        # Apply basis change gates before measurement
        for q in qubit_indices:
            if basis == 'X':
                meas_circuit.h(q)
            elif basis == 'Y':
                meas_circuit.sdg(q)  # S dagger gate
                meas_circuit.h(q)
        
        # Add measurement
        for i, q in enumerate(qubit_indices):
            meas_circuit.measure(q, i)
        
        # Execute the circuit
        transpiled_circuit = transpile(meas_circuit, self.simulator)
        job = self.simulator.run(transpiled_circuit, shots=1024)
        result = job.result()
        counts = result.get_counts()
        
        self.measured_results = counts
        return counts
    
    def measure_in_custom_basis(self, theta: float, phi: float, qubit_indices: Optional[List[int]] = None) -> Dict[str, int]:
        """
        Measure the qubits in a custom basis defined by angles on the Bloch sphere.
        
        Args:
            theta: Polar angle (0 to π)
            phi: Azimuthal angle (0 to 2π)
            qubit_indices: Indices of qubits to measure (default: all qubits)
            
        Returns:
            Dictionary of measurement results
        """
        if self.circuit is None:
            raise ValueError("No circuit has been created")
        
        # Create a copy of the circuit for measurement
        meas_circuit = self.circuit.copy()
        num_qubits = meas_circuit.num_qubits
        
        # If no qubit indices are specified, measure all qubits
        if qubit_indices is None:
            qubit_indices = list(range(num_qubits))
        
        # Apply rotation gates to change to the custom basis
        for q in qubit_indices:
            # First rotate around Y-axis by theta
            meas_circuit.ry(theta, q)
            # Then rotate around Z-axis by phi
            meas_circuit.rz(phi, q)
            # Finally, apply Hadamard to measure in the new basis
            meas_circuit.h(q)
        
        # Add measurement
        for i, q in enumerate(qubit_indices):
            meas_circuit.measure(q, i)
        
        # Execute the circuit
        transpiled_circuit = transpile(meas_circuit, self.simulator)
        job = self.simulator.run(transpiled_circuit, shots=1024)
        result = job.result()
        counts = result.get_counts()
        
        self.measured_results = counts
        return counts
    
    def get_density_matrix(self) -> np.ndarray:
        """
        Get the density matrix of the quantum state.
        
        Returns:
            NumPy array representing the density matrix
        """
        if self.statevector is None:
            raise ValueError("No statevector available")
        
        # Convert statevector to density matrix
        sv = np.array(self.statevector)
        # Reshape to column vector
        sv_col = sv.reshape(-1, 1)
        # Compute density matrix as |ψ⟩⟨ψ|
        rho = np.dot(sv_col, sv_col.conj().T)
        
        return rho
    
    def get_reduced_density_matrix(self, keep_indices: List[int]) -> np.ndarray:
        """
        Get the reduced density matrix by tracing out some qubits.
        
        Args:
            keep_indices: Indices of qubits to keep
            
        Returns:
            NumPy array representing the reduced density matrix
        """
        if self.statevector is None:
            raise ValueError("No statevector available")
        
        # Create a Statevector object
        sv = Statevector(self.statevector)
        
        # Get the number of qubits
        num_qubits = int(np.log2(len(self.statevector)))
        
        # Determine which qubits to trace out
        trace_indices = [i for i in range(num_qubits) if i not in keep_indices]
        
        # Compute the reduced density matrix
        reduced_dm = partial_trace(sv, trace_indices)
        
        return reduced_dm.data
    
    def get_concurrence(self) -> float:
        """
        Calculate the concurrence, a measure of entanglement for two qubits.
        
        Returns:
            Concurrence value (0 for separable states, 1 for maximally entangled states)
        """
        if self.statevector is None:
            raise ValueError("No statevector available")
        
        # Check if we have a two-qubit state
        if len(self.statevector) != 4:
            raise ValueError("Concurrence is only defined for two-qubit states")
        
        # Get the density matrix
        rho = self.get_density_matrix()
        
        # Define the spin-flipped density matrix
        sigma_y = np.array([[0, -1j], [1j, 0]])
        sigma_y_tensor = np.kron(sigma_y, sigma_y)
        rho_tilde = np.dot(sigma_y_tensor, np.dot(np.conj(rho), sigma_y_tensor))
        
        # Calculate R = sqrt(sqrt(rho) * rho_tilde * sqrt(rho))
        sqrt_rho = np.sqrt(rho)
        R = np.dot(sqrt_rho, np.dot(rho_tilde, sqrt_rho))
        
        # Get eigenvalues of R
        eigenvalues = np.linalg.eigvals(R)
        eigenvalues = np.sort(np.abs(eigenvalues))[::-1]  # Sort in descending order
        
        # Calculate concurrence
        concurrence = max(0, eigenvalues[0] - eigenvalues[1] - eigenvalues[2] - eigenvalues[3])
        
        return concurrence
    
    def get_correlation_matrix(self, bases: List[str] = ['X', 'Y', 'Z']) -> np.ndarray:
        """
        Calculate the correlation matrix between two qubits.
        
        Args:
            bases: List of measurement bases
            
        Returns:
            NumPy array representing the correlation matrix
        """
        if self.circuit is None or self.statevector is None:
            raise ValueError("No quantum state available")
        
        # Check if we have at least two qubits
        num_qubits = int(np.log2(len(self.statevector)))
        if num_qubits < 2:
            raise ValueError("Correlation matrix requires at least two qubits")
        
        # Initialize correlation matrix
        n_bases = len(bases)
        corr_matrix = np.zeros((n_bases, n_bases))
        
        # Calculate correlations for each pair of bases
        for i, basis1 in enumerate(bases):
            for j, basis2 in enumerate(bases):
                # Measure qubit 0 in basis1 and qubit 1 in basis2
                # This is a simplified calculation
                if basis1 == 'X' and basis2 == 'X':
                    # ⟨XX⟩
                    corr_matrix[i, j] = self._get_pauli_expectation('XX')
                elif basis1 == 'X' and basis2 == 'Y':
                    # ⟨XY⟩
                    corr_matrix[i, j] = self._get_pauli_expectation('XY')
                elif basis1 == 'X' and basis2 == 'Z':
                    # ⟨XZ⟩
                    corr_matrix[i, j] = self._get_pauli_expectation('XZ')
                elif basis1 == 'Y' and basis2 == 'X':
                    # ⟨YX⟩
                    corr_matrix[i, j] = self._get_pauli_expectation('YX')
                elif basis1 == 'Y' and basis2 == 'Y':
                    # ⟨YY⟩
                    corr_matrix[i, j] = self._get_pauli_expectation('YY')
                elif basis1 == 'Y' and basis2 == 'Z':
                    # ⟨YZ⟩
                    corr_matrix[i, j] = self._get_pauli_expectation('YZ')
                elif basis1 == 'Z' and basis2 == 'X':
                    # ⟨ZX⟩
                    corr_matrix[i, j] = self._get_pauli_expectation('ZX')
                elif basis1 == 'Z' and basis2 == 'Y':
                    # ⟨ZY⟩
                    corr_matrix[i, j] = self._get_pauli_expectation('ZY')
                elif basis1 == 'Z' and basis2 == 'Z':
                    # ⟨ZZ⟩
                    corr_matrix[i, j] = self._get_pauli_expectation('ZZ')
        
        return corr_matrix
    
    def _get_pauli_expectation(self, pauli_string: str) -> float:
        """
        Calculate the expectation value of a Pauli operator.
        
        Args:
            pauli_string: String representing the Pauli operator (e.g., 'XY', 'ZZ')
            
        Returns:
            Expectation value
        """
        if self.statevector is None:
            raise ValueError("No statevector available")
        
        # Create a Statevector object
        sv = Statevector(self.statevector)
        
        # Define Pauli matrices
        I = np.array([[1, 0], [0, 1]])
        X = np.array([[0, 1], [1, 0]])
        Y = np.array([[0, -1j], [1j, 0]])
        Z = np.array([[1, 0], [0, -1]])
        
        # Map characters to Pauli matrices
        pauli_map = {'I': I, 'X': X, 'Y': Y, 'Z': Z}
        
        # Build the operator
        op = np.array(1)
        for char in pauli_string:
            op = np.kron(op, pauli_map[char])
        
        # Calculate expectation value
        expectation = sv.expectation_value(op)
        
        return expectation.real
    
    def get_bell_inequality_value(self) -> float:
        """
        Calculate the CHSH Bell inequality value.
        
        Returns:
            CHSH value (classical limit: 2, quantum limit: 2√2 ≈ 2.82)
        """
        if self.statevector is None:
            raise ValueError("No statevector available")
        
        # Calculate the terms in the CHSH inequality
        # S = E(A,B) - E(A,B') + E(A',B) + E(A',B')
        # where A, A' are measurements on the first qubit
        # and B, B' are measurements on the second qubit
        
        # For Bell states, we can use specific measurement settings
        # that maximize the violation
        
        # E(A,B): Both qubits measured in Z basis
        E_AB = self._get_pauli_expectation('ZZ')
        
        # E(A,B'): First qubit in Z basis, second in X basis
        E_ABp = self._get_pauli_expectation('ZX')
        
        # E(A',B): First qubit in X basis, second in Z basis
        E_ApB = self._get_pauli_expectation('XZ')
        
        # E(A',B'): Both qubits measured in X basis
        E_ApBp = self._get_pauli_expectation('XX')
        
        # Calculate the CHSH value
        chsh = abs(E_AB - E_ABp + E_ApB + E_ApBp)
        
        return chsh
    
    def get_circuit_drawing(self, output: str = "text") -> Any:
        """
        Get a drawing of the quantum circuit.
        
        Args:
            output: Output format ('text', 'latex', 'mpl', etc.)
            
        Returns:
            Circuit drawing in the specified format
        """
        if self.circuit is None:
            raise ValueError("No circuit has been created")
        
        return self.circuit.draw(output=output)
    
    def get_bloch_multivector_figure(self):
        """
        Get a Bloch sphere representation of all qubits.
        
        Returns:
            Matplotlib figure object
        """
        if self.statevector is None:
            raise ValueError("No statevector available")
        
        return plot_bloch_multivector(self.statevector)
    
    def get_histogram_figure(self, counts: Optional[Dict[str, int]] = None):
        """
        Get a histogram figure of the measurement results.
        
        Args:
            counts: Dictionary of measurement results (default: use stored results)
            
        Returns:
            Matplotlib figure object
        """
        if counts is None:
            counts = self.measured_results
        
        if counts is None:
            raise ValueError("No measurement results available")
        
        return plot_histogram(counts)
    
    def get_state_vector_representation(self) -> str:
        """
        Get a string representation of the state vector.
        
        Returns:
            String representation of the state vector
        """
        if self.statevector is None:
            raise ValueError("No statevector available")
        
        # Format the statevector as a string
        n_qubits = int(np.log2(len(self.statevector)))
        state_str = ""
        
        # Threshold for considering an amplitude as zero
        threshold = 1e-10
        
        for i, amplitude in enumerate(self.statevector):
            if abs(amplitude) > threshold:
                # Convert index to binary representation (the basis state)
                basis_state = format(i, f'0{n_qubits}b')
                
                # Format the complex amplitude
                if amplitude.real == 0 and amplitude.imag == 0:
                    continue
                
                term = ""
                if amplitude.real != 0 and amplitude.imag != 0:
                    term = f"({amplitude.real:.4f}{'+' if amplitude.imag > 0 else ''}{amplitude.imag:.4f}j)"
                elif amplitude.real != 0:
                    term = f"{amplitude.real:.4f}"
                else:
                    term = f"{amplitude.imag:.4f}j"
                
                if state_str:
                    state_str += " + "
                
                state_str += f"{term}|{basis_state}⟩"
        
        return state_str