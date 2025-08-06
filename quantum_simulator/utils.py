"""
utils.py - Utility functions for displaying quantum circuit information in Streamlit

This module provides helper functions for formatting and displaying quantum circuit
information, including circuit diagrams, measurement results, and quantum states.
"""

import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
from typing import Dict, List, Tuple, Optional, Any
import base64
from PIL import Image

def display_circuit(circuit_drawing: Any, title: str = "Quantum Circuit"):
    """
    Display a quantum circuit diagram in Streamlit.
    
    Args:
        circuit_drawing: Circuit drawing from QuantumEngine.get_circuit_drawing()
        title: Title to display above the circuit
    """
    st.subheader(title)
    
    # If the circuit drawing is a matplotlib figure
    if isinstance(circuit_drawing, plt.Figure):
        st.pyplot(circuit_drawing)
    # If it's a text representation
    elif isinstance(circuit_drawing, str):
        st.text(circuit_drawing)
    # For other formats, we'll need to handle them specifically
    else:
        st.warning("Unsupported circuit drawing format")

def display_histogram(histogram_figure: plt.Figure, title: str = "Measurement Results"):
    """
    Display a histogram of measurement results in Streamlit.
    
    Args:
        histogram_figure: Histogram figure from QuantumEngine.get_histogram_figure()
        title: Title to display above the histogram
    """
    st.subheader(title)
    st.pyplot(histogram_figure)

def display_statevector(statevector_figure: plt.Figure, title: str = "Quantum State Visualization"):
    """
    Display a visualization of the statevector in Streamlit.
    
    Args:
        statevector_figure: Statevector figure from QuantumEngine.get_statevector_figure()
        title: Title to display above the visualization
    """
    st.subheader(title)
    st.pyplot(statevector_figure)

def display_bloch_sphere(bloch_figure: plt.Figure, title: str = "Bloch Sphere Representation"):
    """
    Display a Bloch sphere representation in Streamlit.
    
    Args:
        bloch_figure: Bloch sphere figure from QuantumEngine.get_bloch_multivector_figure()
        title: Title to display above the Bloch sphere
    """
    st.subheader(title)
    st.pyplot(bloch_figure)

def display_bra_ket_notation(bra_ket: str, title: str = "Quantum State (Bra-Ket Notation)"):
    """
    Display the quantum state in bra-ket notation in Streamlit.
    
    Args:
        bra_ket: Bra-ket notation string from QuantumEngine.get_bra_ket_notation()
        title: Title to display above the notation
    """
    st.subheader(title)
    st.latex(bra_ket.replace('|', r'\left|').replace('⟩', r'\right\rangle'))

def display_statevector_as_vector(statevector: np.ndarray, title: str = "Quantum State (Vector Representation)"):
    """
    Display the statevector as a complex vector in Streamlit.
    
    Args:
        statevector: NumPy array representing the quantum state
        title: Title to display above the vector
    """
    st.subheader(title)
    
    # Format the statevector as a column vector for LaTeX
    latex_vector = r"\begin{pmatrix}"
    for amplitude in statevector:
        # Format the complex number
        if amplitude.real == 0 and amplitude.imag == 0:
            latex_vector += "0 \\\\"
        elif amplitude.real == 0:
            latex_vector += f"{amplitude.imag:.4f}j \\\\"
        elif amplitude.imag == 0:
            latex_vector += f"{amplitude.real:.4f} \\\\"
        else:
            latex_vector += f"{amplitude.real:.4f}{'+' if amplitude.imag > 0 else ''}{amplitude.imag:.4f}j \\\\"
    
    latex_vector += r"\end{pmatrix}"
    
    st.latex(latex_vector)

def display_measurement_probabilities(counts: Dict[str, int], shots: int, title: str = "Measurement Probabilities"):
    """
    Display the measurement probabilities in Streamlit.
    
    Args:
        counts: Dictionary of measurement results from QuantumEngine.simulate()
        shots: Number of shots used in the simulation
        title: Title to display above the probabilities
    """
    st.subheader(title)
    
    # Calculate probabilities
    probabilities = {state: count / shots for state, count in counts.items()}
    
    # Sort by state
    sorted_probs = sorted(probabilities.items(), key=lambda x: x[0])
    
    # Display as a table
    data = {"State": [], "Probability": [], "Count": []}
    for state, prob in sorted_probs:
        data["State"].append(state)
        data["Probability"].append(f"{prob:.4f}")
        data["Count"].append(counts[state])
    
    st.table(data)

def format_complex_number(z: complex) -> str:
    """
    Format a complex number for display.
    
    Args:
        z: Complex number
        
    Returns:
        Formatted string representation
    """
    if z.real == 0 and z.imag == 0:
        return "0"
    elif z.real == 0:
        return f"{z.imag:.4f}j"
    elif z.imag == 0:
        return f"{z.real:.4f}"
    else:
        return f"{z.real:.4f}{'+' if z.imag > 0 else ''}{z.imag:.4f}j"

def get_gate_description(gate_name: str) -> str:
    """
    Get a description of a quantum gate.
    
    Args:
        gate_name: Name of the gate
        
    Returns:
        Description of the gate
    """
    descriptions = {
        "h": "Hadamard gate - Creates superposition by putting a qubit in an equal superposition of |0⟩ and |1⟩.",
        "x": "Pauli-X gate - Quantum equivalent of the NOT gate, flips the state of a qubit.",
        "y": "Pauli-Y gate - Rotates the qubit state around the Y-axis of the Bloch sphere.",
        "z": "Pauli-Z gate - Rotates the qubit state around the Z-axis of the Bloch sphere.",
        "s": "S gate - Phase gate that rotates the qubit state by 90 degrees around the Z-axis.",
        "t": "T gate - Phase gate that rotates the qubit state by 45 degrees around the Z-axis.",
        "rx": "RX gate - Rotation around the X-axis of the Bloch sphere by a specified angle.",
        "ry": "RY gate - Rotation around the Y-axis of the Bloch sphere by a specified angle.",
        "rz": "RZ gate - Rotation around the Z-axis of the Bloch sphere by a specified angle.",
        "cx": "CNOT gate - Controlled-X gate that flips the target qubit if the control qubit is |1⟩.",
        "cz": "CZ gate - Controlled-Z gate that applies a Z gate to the target qubit if the control qubit is |1⟩.",
        "swap": "SWAP gate - Exchanges the states of two qubits.",
        "ccx": "Toffoli gate - Controlled-Controlled-X gate, flips the target qubit if both control qubits are |1⟩."
    }
    
    return descriptions.get(gate_name.lower(), "No description available for this gate.")

def get_gate_matrix(gate_name: str) -> str:
    """
    Get the matrix representation of a quantum gate in LaTeX format.
    
    Args:
        gate_name: Name of the gate
        
    Returns:
        LaTeX string representing the gate matrix
    """
    matrices = {
        "h": r"\frac{1}{\sqrt{2}} \begin{pmatrix} 1 & 1 \\ 1 & -1 \end{pmatrix}",
        "x": r"\begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix}",
        "y": r"\begin{pmatrix} 0 & -i \\ i & 0 \end{pmatrix}",
        "z": r"\begin{pmatrix} 1 & 0 \\ 0 & -1 \end{pmatrix}",
        "s": r"\begin{pmatrix} 1 & 0 \\ 0 & i \end{pmatrix}",
        "t": r"\begin{pmatrix} 1 & 0 \\ 0 & e^{i\pi/4} \end{pmatrix}",
        "rx": r"\begin{pmatrix} \cos(\theta/2) & -i\sin(\theta/2) \\ -i\sin(\theta/2) & \cos(\theta/2) \end{pmatrix}",
        "ry": r"\begin{pmatrix} \cos(\theta/2) & -\sin(\theta/2) \\ \sin(\theta/2) & \cos(\theta/2) \end{pmatrix}",
        "rz": r"\begin{pmatrix} e^{-i\theta/2} & 0 \\ 0 & e^{i\theta/2} \end{pmatrix}",
    }
    
    return matrices.get(gate_name.lower(), "Matrix representation not available.")

def display_gate_info(gate_name: str):
    """
    Display information about a quantum gate in Streamlit.
    
    Args:
        gate_name: Name of the gate
    """
    st.subheader(f"{gate_name.upper()} Gate Information")
    
    # Display description
    description = get_gate_description(gate_name)
    st.write(description)
    
    # Display matrix representation for single-qubit gates
    if gate_name.lower() in ["h", "x", "y", "z", "s", "t", "rx", "ry", "rz"]:
        st.subheader("Matrix Representation")
        matrix = get_gate_matrix(gate_name)
        st.latex(matrix)

def load_image(image_path: str):
    """
    Load an image from a file path.
    
    Args:
        image_path: Path to the image file
        
    Returns:
        PIL Image object
    """
    try:
        return Image.open(image_path)
    except Exception as e:
        st.error(f"Error loading image: {e}")
        return None

def get_image_base64(image_path: str) -> Optional[str]:
    """
    Convert an image to a base64 string for embedding in HTML/CSS.
    
    Args:
        image_path: Path to the image file
        
    Returns:
        Base64 encoded string of the image
    """
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except Exception as e:
        st.error(f"Error encoding image: {e}")
        return None

def set_page_style():
    """
    Set the page style for the Streamlit app.
    """
    st.markdown("""
    <style>
    .main {
        background-color: #f5f5f5;
    }
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    h1, h2, h3 {
        color: #2c3e50;
    }
    .stButton button {
        background-color: #3498db;
        color: white;
    }
    .stButton button:hover {
        background-color: #2980b9;
    }
    </style>
    """, unsafe_allow_html=True)

def display_quantum_concept(concept: str):
    """
    Display an explanation of a quantum computing concept.
    
    Args:
        concept: Name of the concept
    """
    concepts = {
        "superposition": """
        ## Superposition
        
        Superposition is a fundamental principle of quantum mechanics where quantum systems can exist in multiple states simultaneously.
        
        In classical computing, a bit can be either 0 or 1. In quantum computing, a qubit can exist in a superposition of both 0 and 1 states.
        
        Mathematically, a qubit in superposition is represented as:
        
        $|\psi\\rangle = \\alpha|0\\rangle + \\beta|1\\rangle$
        
        where $\\alpha$ and $\\beta$ are complex numbers such that $|\\alpha|^2 + |\\beta|^2 = 1$.
        
        The Hadamard gate (H) is commonly used to create superposition from the $|0\\rangle$ state:
        
        $H|0\\rangle = \\frac{1}{\\sqrt{2}}(|0\\rangle + |1\\rangle)$
        """,
        
        "entanglement": """
        ## Entanglement
        
        Entanglement is a quantum phenomenon where two or more qubits become correlated in such a way that the quantum state of each qubit cannot be described independently of the others.
        
        When qubits are entangled, measuring one qubit instantly affects the state of the other, regardless of the distance between them.
        
        The Bell states are the simplest examples of entangled states:
        
        $|\\Phi^+\\rangle = \\frac{1}{\\sqrt{2}}(|00\\rangle + |11\\rangle)$
        
        $|\\Phi^-\\rangle = \\frac{1}{\\sqrt{2}}(|00\\rangle - |11\\rangle)$
        
        $|\\Psi^+\\rangle = \\frac{1}{\\sqrt{2}}(|01\\rangle + |10\\rangle)$
        
        $|\\Psi^-\\rangle = \\frac{1}{\\sqrt{2}}(|01\\rangle - |10\\rangle)$
        
        To create an entangled state, we typically apply a Hadamard gate to one qubit and then a CNOT gate with that qubit as the control.
        """,
        
        "measurement": """
        ## Quantum Measurement
        
        Measurement in quantum computing causes the quantum state to collapse to one of its basis states.
        
        When we measure a qubit in superposition, we get either 0 or 1 with probabilities determined by the amplitudes of the quantum state.
        
        For a qubit in state $|\\psi\\rangle = \\alpha|0\\rangle + \\beta|1\\rangle$:
        - The probability of measuring 0 is $|\\alpha|^2$
        - The probability of measuring 1 is $|\\beta|^2$
        
        After measurement, the qubit's state collapses to the measured value, losing its superposition.
        
        This probabilistic nature of quantum measurement is a key difference from classical computing.
        """,
        
        "interference": """
        ## Quantum Interference
        
        Quantum interference is a phenomenon where the amplitudes of quantum states can combine constructively or destructively, affecting the probabilities of measurement outcomes.
        
        It's similar to wave interference in physics, where waves can reinforce or cancel each other out.
        
        In quantum algorithms, interference is deliberately used to amplify correct answers and suppress incorrect ones.
        
        For example, in the Deutsch-Jozsa algorithm, interference allows us to determine if a function is constant or balanced with just one query, which would be impossible classically.
        
        The Hadamard gate is often used to create interference by putting qubits in superposition and then allowing them to interfere with each other.
        """
    }
    
    if concept in concepts:
        st.markdown(concepts[concept])
    else:
        st.warning(f"No explanation available for concept: {concept}")