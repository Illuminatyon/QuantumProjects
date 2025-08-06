"""
app.py - Streamlit interface for the entanglement visualizer

This is the main entry point for the entanglement visualizer application.
It provides a user interface for creating, visualizing, and exploring quantum entanglement.
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from quantum_generator import EntanglementGenerator
import visualizer
from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
import os

# Set page configuration
st.set_page_config(
    page_title="Quantum Entanglement Visualizer",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom styling
visualizer.set_page_style()

def main():
    # Page header
    st.title("Quantum Entanglement Visualizer")
    st.markdown("""
    Explore the fascinating phenomenon of quantum entanglement.
    Create entangled states, measure them in different bases, and visualize the correlations.
    """)
    
    # Initialize session state
    if 'entanglement_generator' not in st.session_state:
        st.session_state.entanglement_generator = EntanglementGenerator()
        st.session_state.bell_type = 'phi_plus'
        st.session_state.measurement_basis = 'Z'
        st.session_state.custom_theta = np.pi / 2
        st.session_state.custom_phi = 0.0
        st.session_state.measured_results = None
        st.session_state.correlation_matrix = None
        st.session_state.bell_value = None
    
    # Sidebar for state generation and measurement
    with st.sidebar:
        st.header("Quantum State Generation")
        
        # State type selection
        state_type = st.selectbox(
            "Select State Type",
            ["Bell State", "GHZ State", "W State"]
        )
        
        if state_type == "Bell State":
            # Bell state selection
            bell_type = st.selectbox(
                "Select Bell State",
                [
                    "Phi+ (|00⟩ + |11⟩)/√2",
                    "Phi- (|00⟩ - |11⟩)/√2",
                    "Psi+ (|01⟩ + |10⟩)/√2",
                    "Psi- (|01⟩ - |10⟩)/√2"
                ]
            )
            
            # Map selection to bell_type parameter
            bell_type_map = {
                "Phi+ (|00⟩ + |11⟩)/√2": "phi_plus",
                "Phi- (|00⟩ - |11⟩)/√2": "phi_minus",
                "Psi+ (|01⟩ + |10⟩)/√2": "psi_plus",
                "Psi- (|01⟩ - |10⟩)/√2": "psi_minus"
            }
            
            st.session_state.bell_type = bell_type_map[bell_type]
            
            # Button to generate Bell state
            if st.button("Generate Bell State"):
                with st.spinner("Generating Bell state..."):
                    st.session_state.entanglement_generator.create_bell_state(st.session_state.bell_type)
                    # Reset measurements
                    st.session_state.measured_results = None
                    st.session_state.correlation_matrix = None
                    st.session_state.bell_value = None
                st.success(f"Generated Bell state: {bell_type}")
        
        elif state_type == "GHZ State":
            # GHZ state configuration
            num_qubits = st.slider("Number of Qubits", min_value=3, max_value=5, value=3)
            
            # Button to generate GHZ state
            if st.button("Generate GHZ State"):
                with st.spinner("Generating GHZ state..."):
                    st.session_state.entanglement_generator.create_ghz_state(num_qubits)
                    # Reset measurements
                    st.session_state.measured_results = None
                    st.session_state.correlation_matrix = None
                    st.session_state.bell_value = None
                st.success(f"Generated GHZ state with {num_qubits} qubits")
        
        elif state_type == "W State":
            # W state is currently only implemented for 3 qubits
            st.info("W state is currently only implemented for 3 qubits")
            
            # Button to generate W state
            if st.button("Generate W State"):
                with st.spinner("Generating W state..."):
                    try:
                        st.session_state.entanglement_generator.create_w_state()
                        # Reset measurements
                        st.session_state.measured_results = None
                        st.session_state.correlation_matrix = None
                        st.session_state.bell_value = None
                        st.success("Generated W state with 3 qubits")
                    except Exception as e:
                        st.error(f"Error generating W state: {e}")
        
        # Measurement section
        st.header("Measurement")
        
        # Measurement basis selection
        measurement_type = st.radio(
            "Measurement Type",
            ["Standard Basis (X, Y, Z)", "Custom Basis (θ, φ)"]
        )
        
        if measurement_type == "Standard Basis (X, Y, Z)":
            st.session_state.measurement_basis = st.selectbox(
                "Select Measurement Basis",
                ["Z (Computational)", "X (Hadamard)", "Y"]
            ).split()[0]  # Extract just the first character
        else:
            # Custom basis with angles
            st.session_state.custom_theta = st.slider(
                "θ (Polar Angle)",
                min_value=0.0,
                max_value=np.pi,
                value=st.session_state.custom_theta,
                format="%.2f"
            )
            
            st.session_state.custom_phi = st.slider(
                "φ (Azimuthal Angle)",
                min_value=0.0,
                max_value=2*np.pi,
                value=st.session_state.custom_phi,
                format="%.2f"
            )
        
        # Button to perform measurement
        if st.button("Perform Measurement"):
            if st.session_state.entanglement_generator.circuit is None:
                st.error("Please generate a quantum state first")
            else:
                with st.spinner("Performing measurement..."):
                    try:
                        if measurement_type == "Standard Basis (X, Y, Z)":
                            st.session_state.measured_results = st.session_state.entanglement_generator.measure_in_basis(
                                basis=st.session_state.measurement_basis
                            )
                        else:
                            st.session_state.measured_results = st.session_state.entanglement_generator.measure_in_custom_basis(
                                theta=st.session_state.custom_theta,
                                phi=st.session_state.custom_phi
                            )
                        st.success("Measurement completed")
                    except Exception as e:
                        st.error(f"Error performing measurement: {e}")
        
        # Button to calculate correlation matrix (for Bell states)
        if st.button("Calculate Correlation Matrix"):
            if st.session_state.entanglement_generator.statevector is None:
                st.error("Please generate a quantum state first")
            else:
                with st.spinner("Calculating correlation matrix..."):
                    try:
                        st.session_state.correlation_matrix = st.session_state.entanglement_generator.get_correlation_matrix()
                        st.success("Correlation matrix calculated")
                    except Exception as e:
                        st.error(f"Error calculating correlation matrix: {e}")
        
        # Button to calculate Bell inequality value (for Bell states)
        if st.button("Calculate Bell Inequality Value"):
            if st.session_state.entanglement_generator.statevector is None:
                st.error("Please generate a quantum state first")
            else:
                with st.spinner("Calculating Bell inequality value..."):
                    try:
                        st.session_state.bell_value = st.session_state.entanglement_generator.get_bell_inequality_value()
                        st.success(f"Bell inequality value: {st.session_state.bell_value:.4f}")
                    except Exception as e:
                        st.error(f"Error calculating Bell inequality value: {e}")
    
    # Main area with tabs for different visualizations
    tab1, tab2, tab3, tab4 = st.tabs(["Quantum State", "Measurement Results", "Entanglement Analysis", "Learn"])
    
    with tab1:
        st.header("Quantum State Visualization")
        
        if st.session_state.entanglement_generator.circuit is not None:
            # Display circuit
            try:
                circuit_drawing = st.session_state.entanglement_generator.get_circuit_drawing(output="mpl")
                st.subheader("Quantum Circuit")
                st.pyplot(circuit_drawing)
            except Exception as e:
                st.error(f"Error displaying circuit: {e}")
                # Fallback to text representation
                try:
                    circuit_text = st.session_state.entanglement_generator.get_circuit_drawing(output="text")
                    st.text(circuit_text)
                except:
                    st.error("Could not display circuit in any format.")
            
            # Display state vector representation
            try:
                state_str = st.session_state.entanglement_generator.get_state_vector_representation()
                visualizer.display_quantum_state(state_str)
            except Exception as e:
                st.error(f"Error displaying state vector: {e}")
            
            # Display Bloch sphere representation for small number of qubits
            try:
                if st.session_state.entanglement_generator.statevector is not None:
                    num_qubits = int(np.log2(len(st.session_state.entanglement_generator.statevector)))
                    
                    if num_qubits == 1:
                        # Single qubit state
                        bloch_vector = st.session_state.entanglement_generator.get_bloch_vector(0)
                        fig = visualizer.plot_bloch_sphere(*bloch_vector)
                        st.plotly_chart(fig)
                    elif num_qubits == 2:
                        # Two-qubit state, show reduced density matrices
                        try:
                            # Get reduced density matrices
                            rho_0 = st.session_state.entanglement_generator.get_reduced_density_matrix([0])
                            rho_1 = st.session_state.entanglement_generator.get_reduced_density_matrix([1])
                            
                            # Calculate Bloch vectors from reduced density matrices
                            bloch_0 = (
                                np.real(rho_0[0, 1] + rho_0[1, 0]),  # x
                                np.imag(rho_0[1, 0] - rho_0[0, 1]),  # y
                                np.real(rho_0[0, 0] - rho_0[1, 1])   # z
                            )
                            
                            bloch_1 = (
                                np.real(rho_1[0, 1] + rho_1[1, 0]),  # x
                                np.imag(rho_1[1, 0] - rho_1[0, 1]),  # y
                                np.real(rho_1[0, 0] - rho_1[1, 1])   # z
                            )
                            
                            # Plot dual Bloch spheres
                            fig = visualizer.plot_dual_bloch_spheres(bloch_0, bloch_1)
                            st.plotly_chart(fig)
                            
                            # Display concurrence (measure of entanglement)
                            try:
                                concurrence = st.session_state.entanglement_generator.get_concurrence()
                                st.metric("Concurrence (Entanglement Measure)", f"{concurrence:.4f}")
                                st.info("Concurrence ranges from 0 (separable state) to 1 (maximally entangled state).")
                            except Exception as e:
                                st.error(f"Error calculating concurrence: {e}")
                            
                        except Exception as e:
                            st.error(f"Error displaying Bloch spheres: {e}")
                    else:
                        st.info(f"Bloch sphere visualization not shown for {num_qubits} qubits (too many dimensions).")
            except Exception as e:
                st.error(f"Error with Bloch sphere visualization: {e}")
        else:
            st.info("Generate a quantum state to see its visualization.")
    
    with tab2:
        st.header("Measurement Results")
        
        if st.session_state.measured_results is not None:
            # Display measurement results
            try:
                # Show the measurement basis used
                if st.session_state.measurement_basis in ['X', 'Y', 'Z']:
                    st.subheader(f"Measurement in {st.session_state.measurement_basis} Basis")
                else:
                    st.subheader(f"Measurement in Custom Basis (θ={st.session_state.custom_theta:.2f}, φ={st.session_state.custom_phi:.2f})")
                    # Show the measurement direction on Bloch sphere
                    fig = visualizer.plot_measurement_angles(st.session_state.custom_theta, st.session_state.custom_phi)
                    st.plotly_chart(fig)
                
                # Plot measurement results
                fig = visualizer.plot_measurement_results(st.session_state.measured_results, shots=1024)
                st.plotly_chart(fig)
                
                # For two-qubit states, show correlation visualization
                try:
                    if all(len(state) == 2 for state in st.session_state.measured_results.keys()):
                        fig = visualizer.plot_measurement_correlations(st.session_state.measured_results, shots=1024)
                        st.plotly_chart(fig)
                except Exception as e:
                    st.error(f"Error displaying correlation visualization: {e}")
                
            except Exception as e:
                st.error(f"Error displaying measurement results: {e}")
        else:
            st.info("Perform a measurement to see the results.")
    
    with tab3:
        st.header("Entanglement Analysis")
        
        # Display correlation matrix if available
        if st.session_state.correlation_matrix is not None:
            try:
                st.subheader("Correlation Matrix")
                fig = visualizer.plot_correlation_matrix(st.session_state.correlation_matrix)
                st.plotly_chart(fig)
                
                st.markdown("""
                The correlation matrix shows the expected values of Pauli operator products between qubits.
                For example, the (X, Z) entry shows the correlation between measuring the first qubit in the X basis
                and the second qubit in the Z basis.
                """)
            except Exception as e:
                st.error(f"Error displaying correlation matrix: {e}")
        
        # Display Bell inequality value if available
        if st.session_state.bell_value is not None:
            try:
                st.subheader("Bell Inequality Test")
                fig = visualizer.plot_bell_inequality(st.session_state.bell_value)
                st.plotly_chart(fig)
                
                # Interpretation of the Bell value
                if st.session_state.bell_value <= 2.0:
                    st.info("The state satisfies Bell's inequality and could be explained by classical physics.")
                elif st.session_state.bell_value > 2.0 and st.session_state.bell_value < 2.7:
                    st.success("The state violates Bell's inequality, demonstrating quantum entanglement!")
                else:
                    st.success("The state strongly violates Bell's inequality, showing significant quantum entanglement!")
            except Exception as e:
                st.error(f"Error displaying Bell inequality value: {e}")
        
        # Display density matrix if a state is available
        if st.session_state.entanglement_generator.statevector is not None:
            try:
                st.subheader("Density Matrix")
                density_matrix = st.session_state.entanglement_generator.get_density_matrix()
                fig = visualizer.plot_density_matrix(density_matrix)
                st.plotly_chart(fig)
            except Exception as e:
                st.error(f"Error displaying density matrix: {e}")
        
        if st.session_state.correlation_matrix is None and st.session_state.bell_value is None:
            st.info("Calculate the correlation matrix or Bell inequality value to see the analysis.")
    
    with tab4:
        st.header("Learn About Quantum Entanglement")
        
        # Display explanation of quantum entanglement
        visualizer.display_entanglement_explanation()
        
        # Display explanation of Bell's inequality
        visualizer.display_bell_inequality_explanation()

if __name__ == "__main__":
    main()