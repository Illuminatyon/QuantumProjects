"""
main.py - Streamlit interface for the quantum circuit simulator

This is the main entry point for the quantum circuit simulator application.
It provides a user interface for creating, visualizing, and simulating quantum circuits.
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from quantum_engine import QuantumEngine
import utils
import os

# Set page configuration
st.set_page_config(
    page_title="Quantum Circuit Simulator",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom styling
utils.set_page_style()

def main():
    # Page header
    st.title("Quantum Circuit Simulator")
    st.markdown("""
    Build, visualize, and simulate quantum circuits using Qiskit.
    Add gates, run simulations, and explore the quantum state.
    """)
    
    # Sidebar for circuit configuration and gate selection
    with st.sidebar:
        st.header("Circuit Configuration")
        
        # Number of qubits and classical bits
        num_qubits = st.slider("Number of Qubits", min_value=1, max_value=5, value=2)
        num_bits = st.slider("Number of Classical Bits", min_value=1, max_value=5, value=2)
        
        # Create or reset the quantum engine
        if 'quantum_engine' not in st.session_state or st.button("Reset Circuit"):
            st.session_state.quantum_engine = QuantumEngine(num_qubits, num_bits)
            st.session_state.counts = None
            st.session_state.statevector = None
            st.success(f"Created a new circuit with {num_qubits} qubits and {num_bits} classical bits.")
        
        # Gate selection
        st.header("Add Gates")
        
        # Single-qubit gates
        st.subheader("Single-Qubit Gates")
        single_qubit_col1, single_qubit_col2 = st.columns(2)
        
        with single_qubit_col1:
            gate_type = st.selectbox(
                "Gate Type",
                ["Hadamard (H)", "Pauli-X", "Pauli-Y", "Pauli-Z", "S Gate", "T Gate", "RX", "RY", "RZ"]
            )
        
        with single_qubit_col2:
            qubit_idx = st.selectbox("Qubit", range(num_qubits), format_func=lambda x: f"q{x}")
        
        # For rotation gates, add angle selection
        theta = None
        if gate_type in ["RX", "RY", "RZ"]:
            theta = st.slider("Rotation Angle (radians)", min_value=0.0, max_value=2*np.pi, value=np.pi/2, step=0.1)
        
        # Button to add the single-qubit gate
        if st.button("Add Single-Qubit Gate"):
            engine = st.session_state.quantum_engine
            
            if gate_type == "Hadamard (H)":
                engine.add_hadamard(qubit_idx)
                st.success(f"Added Hadamard gate to qubit {qubit_idx}")
            elif gate_type == "Pauli-X":
                engine.add_pauli_x(qubit_idx)
                st.success(f"Added Pauli-X gate to qubit {qubit_idx}")
            elif gate_type == "Pauli-Y":
                engine.add_pauli_y(qubit_idx)
                st.success(f"Added Pauli-Y gate to qubit {qubit_idx}")
            elif gate_type == "Pauli-Z":
                engine.add_pauli_z(qubit_idx)
                st.success(f"Added Pauli-Z gate to qubit {qubit_idx}")
            elif gate_type == "S Gate":
                engine.add_s_gate(qubit_idx)
                st.success(f"Added S gate to qubit {qubit_idx}")
            elif gate_type == "T Gate":
                engine.add_t_gate(qubit_idx)
                st.success(f"Added T gate to qubit {qubit_idx}")
            elif gate_type == "RX":
                engine.add_rx(theta, qubit_idx)
                st.success(f"Added RX({theta:.2f}) gate to qubit {qubit_idx}")
            elif gate_type == "RY":
                engine.add_ry(theta, qubit_idx)
                st.success(f"Added RY({theta:.2f}) gate to qubit {qubit_idx}")
            elif gate_type == "RZ":
                engine.add_rz(theta, qubit_idx)
                st.success(f"Added RZ({theta:.2f}) gate to qubit {qubit_idx}")
        
        # Multi-qubit gates
        st.subheader("Multi-Qubit Gates")
        multi_gate_type = st.selectbox(
            "Gate Type",
            ["CNOT", "CZ", "SWAP", "Toffoli (CCNOT)"]
        )
        
        # Different controls and targets based on gate type
        if multi_gate_type in ["CNOT", "CZ"]:
            control = st.selectbox("Control Qubit", range(num_qubits), format_func=lambda x: f"q{x}")
            target_options = [q for q in range(num_qubits) if q != control]
            target = st.selectbox("Target Qubit", target_options, format_func=lambda x: f"q{x}") if target_options else None
            
            if st.button("Add Two-Qubit Gate") and target is not None:
                engine = st.session_state.quantum_engine
                
                if multi_gate_type == "CNOT":
                    engine.add_cnot(control, target)
                    st.success(f"Added CNOT gate with control={control} and target={target}")
                elif multi_gate_type == "CZ":
                    engine.add_cz(control, target)
                    st.success(f"Added CZ gate with control={control} and target={target}")
        
        elif multi_gate_type == "SWAP":
            qubit1 = st.selectbox("First Qubit", range(num_qubits), format_func=lambda x: f"q{x}")
            qubit2_options = [q for q in range(num_qubits) if q != qubit1]
            qubit2 = st.selectbox("Second Qubit", qubit2_options, format_func=lambda x: f"q{x}") if qubit2_options else None
            
            if st.button("Add SWAP Gate") and qubit2 is not None:
                engine = st.session_state.quantum_engine
                engine.add_swap(qubit1, qubit2)
                st.success(f"Added SWAP gate between qubits {qubit1} and {qubit2}")
        
        elif multi_gate_type == "Toffoli (CCNOT)":
            if num_qubits >= 3:
                control1 = st.selectbox("First Control Qubit", range(num_qubits), format_func=lambda x: f"q{x}")
                control2_options = [q for q in range(num_qubits) if q != control1]
                control2 = st.selectbox("Second Control Qubit", control2_options, format_func=lambda x: f"q{x}") if control2_options else None
                target_options = [q for q in range(num_qubits) if q != control1 and q != control2]
                target = st.selectbox("Target Qubit", target_options, format_func=lambda x: f"q{x}") if target_options and control2 is not None else None
                
                if st.button("Add Toffoli Gate") and target is not None:
                    engine = st.session_state.quantum_engine
                    engine.add_toffoli(control1, control2, target)
                    st.success(f"Added Toffoli gate with controls={control1},{control2} and target={target}")
            else:
                st.warning("Toffoli gate requires at least 3 qubits.")
        
        # Measurement
        st.subheader("Measurement")
        measure_type = st.radio("Measurement Type", ["Measure All Qubits", "Measure Specific Qubit"])
        
        if measure_type == "Measure All Qubits":
            if st.button("Add Measurement to All Qubits"):
                engine = st.session_state.quantum_engine
                engine.measure_all()
                st.success("Added measurement to all qubits")
        else:
            measure_qubit = st.selectbox("Qubit to Measure", range(num_qubits), format_func=lambda x: f"q{x}")
            measure_bit = st.selectbox("Classical Bit for Result", range(num_bits), format_func=lambda x: f"c{x}")
            
            if st.button("Add Measurement"):
                engine = st.session_state.quantum_engine
                engine.measure_qubit(measure_qubit, measure_bit)
                st.success(f"Added measurement from qubit {measure_qubit} to classical bit {measure_bit}")
        
        # Simulation
        st.header("Simulation")
        shots = st.slider("Number of Shots", min_value=1, max_value=10000, value=1024)
        
        if st.button("Run Simulation"):
            engine = st.session_state.quantum_engine
            
            with st.spinner("Running simulation..."):
                # Get the counts from simulation
                st.session_state.counts = engine.simulate(shots=shots)
                
                # Get the statevector
                try:
                    st.session_state.statevector = engine.get_statevector()
                except Exception as e:
                    st.error(f"Error getting statevector: {e}")
                    st.session_state.statevector = None
            
            st.success("Simulation completed!")
    
    # Main area for displaying results
    tab1, tab2, tab3, tab4 = st.tabs(["Circuit", "Measurement Results", "Quantum State", "Learn"])
    
    with tab1:
        st.header("Quantum Circuit")
        
        if 'quantum_engine' in st.session_state:
            engine = st.session_state.quantum_engine
            
            # Display circuit diagram
            try:
                circuit_drawing = engine.get_circuit_drawing(output="mpl")
                utils.display_circuit(circuit_drawing)
            except Exception as e:
                st.error(f"Error displaying circuit: {e}")
                # Fallback to text representation
                try:
                    circuit_text = engine.get_circuit_drawing(output="text")
                    st.text(circuit_text)
                except:
                    st.error("Could not display circuit in any format.")
    
    with tab2:
        st.header("Measurement Results")
        
        if 'counts' in st.session_state and st.session_state.counts is not None:
            # Display histogram
            try:
                histogram_figure = st.session_state.quantum_engine.get_histogram_figure(st.session_state.counts)
                utils.display_histogram(histogram_figure)
                
                # Display probabilities table
                utils.display_measurement_probabilities(st.session_state.counts, shots, "Measurement Probabilities")
            except Exception as e:
                st.error(f"Error displaying measurement results: {e}")
        else:
            st.info("Run a simulation to see measurement results.")
    
    with tab3:
        st.header("Quantum State")
        
        if 'statevector' in st.session_state and st.session_state.statevector is not None:
            # Create columns for different representations
            col1, col2 = st.columns(2)
            
            with col1:
                # Display statevector visualization
                try:
                    statevector_figure = st.session_state.quantum_engine.get_statevector_figure()
                    utils.display_statevector(statevector_figure)
                except Exception as e:
                    st.error(f"Error displaying statevector visualization: {e}")
            
            with col2:
                # Display Bloch sphere for small number of qubits
                if st.session_state.quantum_engine.num_qubits <= 5:
                    try:
                        bloch_figure = st.session_state.quantum_engine.get_bloch_multivector_figure()
                        utils.display_bloch_sphere(bloch_figure)
                    except Exception as e:
                        st.error(f"Error displaying Bloch sphere: {e}")
            
            # Display bra-ket notation
            try:
                bra_ket = st.session_state.quantum_engine.get_bra_ket_notation()
                utils.display_bra_ket_notation(bra_ket)
            except Exception as e:
                st.error(f"Error displaying bra-ket notation: {e}")
            
            # Display vector representation
            try:
                utils.display_statevector_as_vector(st.session_state.statevector)
            except Exception as e:
                st.error(f"Error displaying vector representation: {e}")
        else:
            st.info("Run a simulation to see the quantum state.")
    
    with tab4:
        st.header("Learn Quantum Computing")
        
        # Select a concept to learn about
        concept = st.selectbox(
            "Select a concept to learn about",
            ["Superposition", "Entanglement", "Measurement", "Interference"]
        )
        
        # Display the selected concept
        utils.display_quantum_concept(concept.lower())
        
        # Display gate information
        st.subheader("Quantum Gates Reference")
        gate_info = st.selectbox(
            "Select a gate to learn about",
            ["H", "X", "Y", "Z", "S", "T", "RX", "RY", "RZ", "CNOT", "CZ", "SWAP", "Toffoli"]
        )
        
        utils.display_gate_info(gate_info)

if __name__ == "__main__":
    main()