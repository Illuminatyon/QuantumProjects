"""
quantum_engine.py - Core functionality for quantum circuit manipulation using Qiskit

This module provides functions to create, modify, and simulate quantum circuits.
It serves as the backend for the quantum circuit simulator application.
"""

from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
from qiskit_aer.backends.aer_simulator import AerSimulator
from qiskit.visualization import plot_histogram, plot_bloch_multivector, plot_state_city
from qiskit.quantum_info import Statevector
import numpy as np
from typing import Dict, List, Tuple, Optional, Union, Any


class QuantumEngine:
    """
    A class to handle quantum circuit operations using Qiskit.
    """
    
    def __init__(self, num_qubits: int = 1, num_bits: int = 1):
        """
        Initialize a quantum circuit with the specified number of qubits and classical bits.
        
        Args:
            num_qubits: Number of qubits in the circuit
            num_bits: Number of classical bits in the circuit
        """
        self.num_qubits = num_qubits
        self.num_bits = num_bits
        self.circuit = QuantumCircuit(num_qubits, num_bits)
        self.simulator = Aer.get_backend('aer_simulator')
        
    def reset_circuit(self, num_qubits: Optional[int] = None, num_bits: Optional[int] = None):
        """
        Reset the quantum circuit with optionally new dimensions.
        
        Args:
            num_qubits: New number of qubits (default: use current value)
            num_bits: New number of classical bits (default: use current value)
        """
        self.num_qubits = num_qubits if num_qubits is not None else self.num_qubits
        self.num_bits = num_bits if num_bits is not None else self.num_bits
        self.circuit = QuantumCircuit(self.num_qubits, self.num_bits)
    
    # Single-qubit gates
    def add_hadamard(self, qubit: int):
        """Add Hadamard gate to the specified qubit."""
        self.circuit.h(qubit)
        return self
    
    def add_pauli_x(self, qubit: int):
        """Add Pauli-X (NOT) gate to the specified qubit."""
        self.circuit.x(qubit)
        return self
    
    def add_pauli_y(self, qubit: int):
        """Add Pauli-Y gate to the specified qubit."""
        self.circuit.y(qubit)
        return self
    
    def add_pauli_z(self, qubit: int):
        """Add Pauli-Z gate to the specified qubit."""
        self.circuit.z(qubit)
        return self
    
    def add_s_gate(self, qubit: int):
        """Add S gate (phase gate) to the specified qubit."""
        self.circuit.s(qubit)
        return self
    
    def add_t_gate(self, qubit: int):
        """Add T gate to the specified qubit."""
        self.circuit.t(qubit)
        return self
    
    def add_rx(self, theta: float, qubit: int):
        """Add rotation around X-axis to the specified qubit."""
        self.circuit.rx(theta, qubit)
        return self
    
    def add_ry(self, theta: float, qubit: int):
        """Add rotation around Y-axis to the specified qubit."""
        self.circuit.ry(theta, qubit)
        return self
    
    def add_rz(self, theta: float, qubit: int):
        """Add rotation around Z-axis to the specified qubit."""
        self.circuit.rz(theta, qubit)
        return self
    
    # Multi-qubit gates
    def add_cnot(self, control: int, target: int):
        """Add CNOT (Controlled-X) gate with the specified control and target qubits."""
        self.circuit.cx(control, target)
        return self
    
    def add_cz(self, control: int, target: int):
        """Add Controlled-Z gate with the specified control and target qubits."""
        self.circuit.cz(control, target)
        return self
    
    def add_swap(self, qubit1: int, qubit2: int):
        """Add SWAP gate between the specified qubits."""
        self.circuit.swap(qubit1, qubit2)
        return self
    
    def add_toffoli(self, control1: int, control2: int, target: int):
        """Add Toffoli (CCNOT) gate with the specified control and target qubits."""
        self.circuit.ccx(control1, control2, target)
        return self
    
    # Measurement
    def measure_all(self):
        """Add measurement to all qubits."""
        self.circuit.measure_all()
        return self
    
    def measure_qubit(self, qubit: int, bit: int):
        """
        Measure a specific qubit and store the result in the specified classical bit.
        
        Args:
            qubit: Index of the qubit to measure
            bit: Index of the classical bit to store the result
        """
        self.circuit.measure(qubit, bit)
        return self
    
    # Simulation
    def simulate(self, shots: int = 1024) -> Dict[str, int]:
        """
        Simulate the quantum circuit and return measurement results.
        
        Args:
            shots: Number of times to run the simulation
            
        Returns:
            Dictionary mapping measurement outcomes to their counts
        """
        # Check if the circuit has any measurements
        has_measurements = False
        for instruction in self.circuit.data:
            if instruction.operation.name == 'measure':
                has_measurements = True
                break
        
        # If no measurements, add measurements to all qubits
        if not has_measurements:
            # Create a copy of the circuit to avoid modifying the original
            circuit_copy = self.circuit.copy()
            circuit_copy.measure_all()
            transpiled_circuit = transpile(circuit_copy, self.simulator)
        else:
            transpiled_circuit = transpile(self.circuit, self.simulator)
        
        job = self.simulator.run(transpiled_circuit, shots=shots)
        result = job.result()
        counts = result.get_counts()
        return counts
    
    def get_statevector(self) -> np.ndarray:
        """
        Get the statevector representation of the quantum state.
        
        Returns:
            NumPy array representing the quantum state vector
        """
        # Create a new simulator that returns the statevector
        statevector_sim = Aer.get_backend('statevector_simulator')
        
        # Create a copy of the circuit without measurements to get the statevector
        circuit_copy = self.circuit.copy()
        
        # Remove any measurements from the circuit copy
        # This is a simplistic approach; in a real application, you might want to
        # create a new circuit with just the gates
        for instruction in circuit_copy.data:
            if instruction.operation.name == 'measure':
                circuit_copy.data.remove(instruction)
        
        # Execute the circuit
        transpiled_circuit = transpile(circuit_copy, statevector_sim)
        job = statevector_sim.run(transpiled_circuit)
        result = job.result()
        statevector = result.get_statevector()
        
        return statevector
    
    def get_bloch_vector(self, qubit: int) -> Tuple[float, float, float]:
        """
        Get the Bloch vector representation for a single qubit.
        
        Args:
            qubit: Index of the qubit
            
        Returns:
            Tuple (x, y, z) representing the Bloch vector
        """
        # This is a simplified implementation
        # In a real application, you would extract the Bloch vector from the density matrix
        statevector = self.get_statevector()
        state = Statevector(statevector)
        bloch = state.expectation_value([("X", [qubit]), ("Y", [qubit]), ("Z", [qubit])])
        return (bloch[0].real, bloch[1].real, bloch[2].real)
    
    # Visualization helpers (these will be used by utils.py)
    def get_circuit_drawing(self, output: str = "text") -> Any:
        """
        Get a drawing of the quantum circuit.
        
        Args:
            output: Output format ('text', 'latex', 'mpl', etc.)
            
        Returns:
            Circuit drawing in the specified format
        """
        return self.circuit.draw(output=output)
    
    def get_histogram_figure(self, counts: Dict[str, int]):
        """
        Get a histogram figure of the measurement results.
        
        Args:
            counts: Dictionary of measurement results from simulate()
            
        Returns:
            Matplotlib figure object
        """
        return plot_histogram(counts)
    
    def get_statevector_figure(self):
        """
        Get a visualization of the statevector.
        
        Returns:
            Matplotlib figure object
        """
        statevector = self.get_statevector()
        return plot_state_city(statevector)
    
    def get_bloch_multivector_figure(self):
        """
        Get a Bloch sphere representation of all qubits.
        
        Returns:
            Matplotlib figure object
        """
        statevector = self.get_statevector()
        return plot_bloch_multivector(statevector)
    
    def get_bra_ket_notation(self) -> str:
        """
        Get the quantum state in bra-ket notation.
        
        Returns:
            String representation of the quantum state in bra-ket notation
        """
        statevector = self.get_statevector()
        
        # Format the statevector as a bra-ket string
        n_qubits = int(np.log2(len(statevector)))
        bra_ket = ""
        
        # Threshold for considering an amplitude as zero
        threshold = 1e-10
        
        for i, amplitude in enumerate(statevector):
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
                
                if bra_ket:
                    bra_ket += " + "
                
                bra_ket += f"{term}|{basis_state}⟩"
        
        return bra_ket