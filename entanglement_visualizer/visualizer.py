"""
visualizer.py - Functions for visualizing quantum entanglement and correlations

This module provides visualization tools for quantum entanglement, including
correlation matrices, Bloch sphere representations, and interactive plots.
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from typing import Dict, List, Tuple, Optional, Union, Any
import pandas as pd


def plot_correlation_matrix(correlation_matrix: np.ndarray, bases: List[str] = ['X', 'Y', 'Z']) -> go.Figure:
    """
    Create a heatmap visualization of the correlation matrix.
    
    Args:
        correlation_matrix: NumPy array containing correlation values
        bases: List of measurement bases
        
    Returns:
        Plotly figure object
    """
    # Create a heatmap
    fig = go.Figure(data=go.Heatmap(
        z=correlation_matrix,
        x=bases,
        y=bases,
        colorscale='RdBu',
        zmid=0,  # Center the color scale at zero
        colorbar=dict(
            title="Correlation",
            titleside="right"
        )
    ))
    
    # Update layout
    fig.update_layout(
        title="Correlation Matrix",
        xaxis=dict(title="Qubit 1 Measurement Basis"),
        yaxis=dict(title="Qubit 0 Measurement Basis"),
        width=500,
        height=500
    )
    
    return fig


def plot_measurement_results(counts: Dict[str, int], shots: int) -> go.Figure:
    """
    Create a bar chart of measurement results.
    
    Args:
        counts: Dictionary mapping measurement outcomes to counts
        shots: Total number of shots
        
    Returns:
        Plotly figure object
    """
    # Calculate probabilities
    probabilities = {state: count / shots for state, count in counts.items()}
    
    # Sort by state
    sorted_items = sorted(probabilities.items(), key=lambda x: x[0])
    states = [item[0] for item in sorted_items]
    probs = [item[1] for item in sorted_items]
    
    # Create a bar chart
    fig = go.Figure(data=go.Bar(
        x=states,
        y=probs,
        marker_color='royalblue',
        text=[f"{p:.3f}" for p in probs],
        textposition='auto'
    ))
    
    # Update layout
    fig.update_layout(
        title="Measurement Probabilities",
        xaxis=dict(title="State"),
        yaxis=dict(title="Probability"),
        width=600,
        height=400
    )
    
    return fig


def plot_bloch_sphere(x: float, y: float, z: float, title: str = "Bloch Sphere") -> go.Figure:
    """
    Create an interactive 3D Bloch sphere visualization with a state vector.
    
    Args:
        x, y, z: Coordinates of the state vector on the Bloch sphere
        title: Title for the plot
        
    Returns:
        Plotly figure object
    """
    # Create a figure with a 3D scene
    fig = go.Figure()
    
    # Add the Bloch sphere (a unit sphere)
    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi, 100)
    
    x_sphere = np.outer(np.cos(u), np.sin(v))
    y_sphere = np.outer(np.sin(u), np.sin(v))
    z_sphere = np.outer(np.ones(np.size(u)), np.cos(v))
    
    fig.add_trace(go.Surface(
        x=x_sphere, y=y_sphere, z=z_sphere,
        opacity=0.3,
        colorscale=[[0, 'rgb(200, 200, 200)'], [1, 'rgb(240, 240, 240)']],
        showscale=False
    ))
    
    # Add the state vector
    fig.add_trace(go.Scatter3d(
        x=[0, x],
        y=[0, y],
        z=[0, z],
        mode='lines+markers',
        line=dict(color='red', width=5),
        marker=dict(size=[0, 8], color='red')
    ))
    
    # Add axis lines
    axis_length = 1.2
    
    # X-axis (red)
    fig.add_trace(go.Scatter3d(
        x=[-axis_length, axis_length],
        y=[0, 0],
        z=[0, 0],
        mode='lines',
        line=dict(color='red', width=3),
        name='X-axis'
    ))
    
    # Y-axis (green)
    fig.add_trace(go.Scatter3d(
        x=[0, 0],
        y=[-axis_length, axis_length],
        z=[0, 0],
        mode='lines',
        line=dict(color='green', width=3),
        name='Y-axis'
    ))
    
    # Z-axis (blue)
    fig.add_trace(go.Scatter3d(
        x=[0, 0],
        y=[0, 0],
        z=[-axis_length, axis_length],
        mode='lines',
        line=dict(color='blue', width=3),
        name='Z-axis'
    ))
    
    # Add labels for the poles
    fig.add_trace(go.Scatter3d(
        x=[0, 0],
        y=[0, 0],
        z=[1.1, -1.1],
        mode='text',
        text=['|0⟩', '|1⟩'],
        textposition='top center',
        textfont=dict(size=14),
        showlegend=False
    ))
    
    # Update layout
    fig.update_layout(
        title=title,
        scene=dict(
            xaxis=dict(range=[-1.2, 1.2], showticklabels=False),
            yaxis=dict(range=[-1.2, 1.2], showticklabels=False),
            zaxis=dict(range=[-1.2, 1.2], showticklabels=False),
            aspectmode='cube'
        ),
        width=500,
        height=500,
        margin=dict(l=0, r=0, b=0, t=40)
    )
    
    return fig


def plot_dual_bloch_spheres(bloch1: Tuple[float, float, float], bloch2: Tuple[float, float, float]) -> go.Figure:
    """
    Create a side-by-side visualization of two Bloch spheres.
    
    Args:
        bloch1: (x, y, z) coordinates for the first Bloch vector
        bloch2: (x, y, z) coordinates for the second Bloch vector
        
    Returns:
        Plotly figure object
    """
    # Create a subplot with two 3D scenes
    fig = make_subplots(
        rows=1, cols=2,
        specs=[[{'type': 'scene'}, {'type': 'scene'}]],
        subplot_titles=("Qubit 0", "Qubit 1")
    )
    
    # Add Bloch spheres and vectors
    for i, (x, y, z) in enumerate([(bloch1), (bloch2)], 1):
        # Add the Bloch sphere (a unit sphere)
        u = np.linspace(0, 2 * np.pi, 50)
        v = np.linspace(0, np.pi, 50)
        
        x_sphere = np.outer(np.cos(u), np.sin(v))
        y_sphere = np.outer(np.sin(u), np.sin(v))
        z_sphere = np.outer(np.ones(np.size(u)), np.cos(v))
        
        fig.add_trace(go.Surface(
            x=x_sphere, y=y_sphere, z=z_sphere,
            opacity=0.3,
            colorscale=[[0, 'rgb(200, 200, 200)'], [1, 'rgb(240, 240, 240)']],
            showscale=False
        ), row=1, col=i)
        
        # Add the state vector
        fig.add_trace(go.Scatter3d(
            x=[0, x],
            y=[0, y],
            z=[0, z],
            mode='lines+markers',
            line=dict(color='red', width=5),
            marker=dict(size=[0, 8], color='red'),
            showlegend=False
        ), row=1, col=i)
        
        # Add axis lines
        axis_length = 1.2
        
        # X-axis (red)
        fig.add_trace(go.Scatter3d(
            x=[-axis_length, axis_length],
            y=[0, 0],
            z=[0, 0],
            mode='lines',
            line=dict(color='red', width=3),
            name='X-axis' if i == 1 else None,
            showlegend=i == 1
        ), row=1, col=i)
        
        # Y-axis (green)
        fig.add_trace(go.Scatter3d(
            x=[0, 0],
            y=[-axis_length, axis_length],
            z=[0, 0],
            mode='lines',
            line=dict(color='green', width=3),
            name='Y-axis' if i == 1 else None,
            showlegend=i == 1
        ), row=1, col=i)
        
        # Z-axis (blue)
        fig.add_trace(go.Scatter3d(
            x=[0, 0],
            y=[0, 0],
            z=[-axis_length, axis_length],
            mode='lines',
            line=dict(color='blue', width=3),
            name='Z-axis' if i == 1 else None,
            showlegend=i == 1
        ), row=1, col=i)
        
        # Add labels for the poles
        fig.add_trace(go.Scatter3d(
            x=[0, 0],
            y=[0, 0],
            z=[1.1, -1.1],
            mode='text',
            text=['|0⟩', '|1⟩'],
            textposition='top center',
            textfont=dict(size=14),
            showlegend=False
        ), row=1, col=i)
    
    # Update layout
    fig.update_layout(
        title="Bloch Sphere Representation",
        scene=dict(
            xaxis=dict(range=[-1.2, 1.2], showticklabels=False),
            yaxis=dict(range=[-1.2, 1.2], showticklabels=False),
            zaxis=dict(range=[-1.2, 1.2], showticklabels=False),
            aspectmode='cube'
        ),
        scene2=dict(
            xaxis=dict(range=[-1.2, 1.2], showticklabels=False),
            yaxis=dict(range=[-1.2, 1.2], showticklabels=False),
            zaxis=dict(range=[-1.2, 1.2], showticklabels=False),
            aspectmode='cube'
        ),
        width=1000,
        height=500,
        margin=dict(l=0, r=0, b=0, t=40)
    )
    
    return fig


def plot_bell_inequality(chsh_value: float) -> go.Figure:
    """
    Create a gauge chart showing the CHSH Bell inequality value.
    
    Args:
        chsh_value: The calculated CHSH value
        
    Returns:
        Plotly figure object
    """
    # Create a gauge chart
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=chsh_value,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "CHSH Bell Inequality Value"},
        gauge={
            'axis': {'range': [0, 4], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "darkblue"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 2], 'color': 'lightgray'},
                {'range': [2, 2.82], 'color': 'royalblue'},
                {'range': [2.82, 4], 'color': 'red'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 2.82
            }
        }
    ))
    
    # Add annotations
    fig.add_annotation(
        x=0.5,
        y=0.1,
        text="Classical Limit: 2.0",
        showarrow=False
    )
    
    fig.add_annotation(
        x=0.5,
        y=0.2,
        text="Quantum Limit: 2√2 ≈ 2.82",
        showarrow=False
    )
    
    # Update layout
    fig.update_layout(
        width=500,
        height=400,
        margin=dict(l=40, r=40, t=60, b=40)
    )
    
    return fig


def plot_measurement_angles(theta: float, phi: float) -> go.Figure:
    """
    Create a visualization of measurement angles on the Bloch sphere.
    
    Args:
        theta: Polar angle (0 to π)
        phi: Azimuthal angle (0 to 2π)
        
    Returns:
        Plotly figure object
    """
    # Convert spherical coordinates to Cartesian
    x = np.sin(theta) * np.cos(phi)
    y = np.sin(theta) * np.sin(phi)
    z = np.cos(theta)
    
    # Create a Bloch sphere with the measurement direction
    fig = plot_bloch_sphere(x, y, z, title="Measurement Direction")
    
    # Add annotations
    fig.add_annotation(
        x=0.5,
        y=0,
        text=f"θ = {theta:.2f} rad, φ = {phi:.2f} rad",
        showarrow=False,
        xref="paper",
        yref="paper"
    )
    
    return fig


def plot_density_matrix(density_matrix: np.ndarray, title: str = "Density Matrix") -> go.Figure:
    """
    Create a 3D bar plot visualization of a density matrix.
    
    Args:
        density_matrix: Complex NumPy array representing the density matrix
        title: Title for the plot
        
    Returns:
        Plotly figure object
    """
    # Get dimensions
    n = density_matrix.shape[0]
    basis_size = int(np.log2(n))
    
    # Create basis labels
    basis_labels = [format(i, f'0{basis_size}b') for i in range(n)]
    
    # Extract real and imaginary parts
    real_part = density_matrix.real
    imag_part = density_matrix.imag
    
    # Create meshgrid for x and y coordinates
    x, y = np.meshgrid(range(n), range(n))
    x = x.flatten()
    y = y.flatten()
    
    # Create figure with two subplots
    fig = make_subplots(
        rows=1, cols=2,
        specs=[[{'type': 'surface'}, {'type': 'surface'}]],
        subplot_titles=("Real Part", "Imaginary Part")
    )
    
    # Add real part
    fig.add_trace(
        go.Surface(
            z=real_part,
            colorscale='Blues',
            showscale=False
        ),
        row=1, col=1
    )
    
    # Add imaginary part
    fig.add_trace(
        go.Surface(
            z=imag_part,
            colorscale='Reds',
            showscale=False
        ),
        row=1, col=2
    )
    
    # Update layout
    fig.update_layout(
        title=title,
        scene=dict(
            xaxis=dict(title="", tickvals=list(range(n)), ticktext=basis_labels),
            yaxis=dict(title="", tickvals=list(range(n)), ticktext=basis_labels),
            zaxis=dict(title="Value")
        ),
        scene2=dict(
            xaxis=dict(title="", tickvals=list(range(n)), ticktext=basis_labels),
            yaxis=dict(title="", tickvals=list(range(n)), ticktext=basis_labels),
            zaxis=dict(title="Value")
        ),
        width=1000,
        height=500
    )
    
    return fig


def plot_measurement_correlations(results: Dict[str, int], shots: int) -> go.Figure:
    """
    Create a visualization of correlations in measurement results.
    
    Args:
        results: Dictionary mapping measurement outcomes to counts
        shots: Total number of shots
        
    Returns:
        Plotly figure object
    """
    # Check if we have a two-qubit state
    if all(len(state) == 2 for state in results.keys()):
        # Extract individual qubit results
        q0_0_count = sum(results.get(f"0{b}", 0) for b in ["0", "1"])
        q0_1_count = sum(results.get(f"1{b}", 0) for b in ["0", "1"])
        q1_0_count = sum(results.get(f"{a}0", 0) for a in ["0", "1"])
        q1_1_count = sum(results.get(f"{a}1", 0) for a in ["0", "1"])
        
        # Calculate joint probabilities
        p00 = results.get("00", 0) / shots
        p01 = results.get("01", 0) / shots
        p10 = results.get("10", 0) / shots
        p11 = results.get("11", 0) / shots
        
        # Calculate marginal probabilities
        p0_0 = q0_0_count / shots
        p0_1 = q0_1_count / shots
        p1_0 = q1_0_count / shots
        p1_1 = q1_1_count / shots
        
        # Calculate expected joint probabilities (if independent)
        e00 = p0_0 * p1_0
        e01 = p0_0 * p1_1
        e10 = p0_1 * p1_0
        e11 = p0_1 * p1_1
        
        # Calculate correlation
        correlation = p00 + p11 - p01 - p10
        
        # Create a dataframe for the heatmap
        joint_probs = pd.DataFrame([
            {"Qubit 0": "0", "Qubit 1": "0", "Actual": p00, "Expected": e00, "Difference": p00 - e00},
            {"Qubit 0": "0", "Qubit 1": "1", "Actual": p01, "Expected": e01, "Difference": p01 - e01},
            {"Qubit 0": "1", "Qubit 1": "0", "Actual": p10, "Expected": e10, "Difference": p10 - e10},
            {"Qubit 0": "1", "Qubit 1": "1", "Actual": p11, "Expected": e11, "Difference": p11 - e11}
        ])
        
        # Create a figure with subplots
        fig = make_subplots(
            rows=1, cols=3,
            specs=[[{"type": "heatmap"}, {"type": "heatmap"}, {"type": "heatmap"}]],
            subplot_titles=("Actual Joint Probabilities", "Expected (Independent)", "Difference")
        )
        
        # Add heatmaps
        fig.add_trace(
            go.Heatmap(
                z=[[p00, p01], [p10, p11]],
                x=["0", "1"],
                y=["0", "1"],
                colorscale="Blues",
                showscale=False
            ),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Heatmap(
                z=[[e00, e01], [e10, e11]],
                x=["0", "1"],
                y=["0", "1"],
                colorscale="Greens",
                showscale=False
            ),
            row=1, col=2
        )
        
        fig.add_trace(
            go.Heatmap(
                z=[[p00 - e00, p01 - e01], [p10 - e10, p11 - e11]],
                x=["0", "1"],
                y=["0", "1"],
                colorscale="RdBu",
                zmid=0,
                showscale=True
            ),
            row=1, col=3
        )
        
        # Update layout
        fig.update_layout(
            title=f"Measurement Correlations (Correlation = {correlation:.3f})",
            xaxis=dict(title="Qubit 1"),
            yaxis=dict(title="Qubit 0"),
            xaxis2=dict(title="Qubit 1"),
            yaxis2=dict(title="Qubit 0"),
            xaxis3=dict(title="Qubit 1"),
            yaxis3=dict(title="Qubit 0"),
            width=1000,
            height=400
        )
        
        return fig
    else:
        # For non-two-qubit states, return a simple bar chart
        return plot_measurement_results(results, shots)


def display_quantum_state(state_str: str):
    """
    Display a quantum state in Streamlit.
    
    Args:
        state_str: String representation of the quantum state
    """
    st.subheader("Quantum State")
    
    # Convert to LaTeX format
    latex_state = state_str.replace('|', r'\left|').replace('⟩', r'\right\rangle')
    
    # Display using LaTeX
    st.latex(latex_state)


def display_entanglement_explanation():
    """Display an explanation of quantum entanglement in Streamlit."""
    st.markdown("""
    ## Quantum Entanglement
    
    Quantum entanglement is a phenomenon where two or more quantum particles become correlated in such a way that the quantum state of each particle cannot be described independently of the others, regardless of the distance separating them.
    
    ### Key Properties:
    
    1. **Non-local correlations**: Measuring one entangled particle instantly affects the state of its entangled partners, regardless of distance.
    
    2. **Bell's inequality violation**: Entangled systems can exhibit correlations stronger than what's possible in classical physics.
    
    3. **No-cloning theorem**: It's impossible to create an identical copy of an unknown quantum state.
    
    ### Bell States
    
    The four maximally entangled two-qubit states are called Bell states:
    
    - $|\Phi^+\\rangle = \\frac{1}{\\sqrt{2}}(|00\\rangle + |11\\rangle)$
    - $|\Phi^-\\rangle = \\frac{1}{\\sqrt{2}}(|00\\rangle - |11\\rangle)$
    - $|\Psi^+\\rangle = \\frac{1}{\\sqrt{2}}(|01\\rangle + |10\\rangle)$
    - $|\Psi^-\\rangle = \\frac{1}{\\sqrt{2}}(|01\\rangle - |10\\rangle)$
    
    ### Applications
    
    - Quantum teleportation
    - Superdense coding
    - Quantum cryptography
    - Quantum computing algorithms
    """)


def display_bell_inequality_explanation():
    """Display an explanation of Bell's inequality in Streamlit."""
    st.markdown("""
    ## Bell's Inequality
    
    Bell's inequality is a mathematical constraint on the results of experiments on systems that satisfy certain locality and reality conditions. Quantum mechanics predicts that entangled particles can violate this inequality.
    
    ### CHSH Inequality
    
    The CHSH (Clauser-Horne-Shimony-Holt) version of Bell's inequality states that for any local hidden variable theory:
    
    $|E(A,B) - E(A,B') + E(A',B) + E(A',B')| \leq 2$
    
    where $E(X,Y)$ is the correlation between measurements $X$ and $Y$.
    
    ### Quantum Mechanics Prediction
    
    Quantum mechanics predicts that entangled particles can violate this inequality, with a maximum value of $2\\sqrt{2} \\approx 2.82$.
    
    ### Significance
    
    - Values ≤ 2: Compatible with classical physics (local realism)
    - Values > 2: Only possible with quantum entanglement
    - Values approaching 2.82: Maximum quantum entanglement
    
    Experimental violations of Bell's inequality have confirmed the non-local nature of quantum mechanics.
    """)


def set_page_style():
    """Set the page style for the Streamlit app."""
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