# Quantum Computing Projects

This repository contains three interactive quantum computing projects that demonstrate fundamental quantum concepts through visual and interactive interfaces.

## Overview

The three projects are:

1. **Quantum Circuit Simulator**: Build, visualize, and simulate quantum circuits with a user-friendly interface.
2. **Entanglement Visualizer**: Explore quantum entanglement and observe the effects of measurement on entangled qubits.
3. **Quantum Tic Tac Toe**: Play a quantum version of Tic Tac Toe where moves exist in superposition until they collapse.

## Requirements

All projects require Python 3.10+ and the following common dependencies:
- Qiskit
- Streamlit
- NumPy
- Matplotlib/Plotly

Each project has its own `requirements.txt` file with specific dependencies.

## Installation

There are two ways to install the required dependencies:

### Option 1: Using the Launcher Scripts (Recommended)

The launcher scripts now include automatic dependency detection and installation:

1. Clone this repository:
```bash
git clone <repository-url>
cd <repository-directory>
```

2. Create a virtual environment (optional but recommended):
```bash
python -m venv .venv
# On Windows
.venv\Scripts\activate
# On macOS/Linux
source .venv/bin/activate
```

3. Run any of the launcher scripts:
```bash
python launcher.py
# Or for a specific project
python quantum_simulator/launcher.py
```

4. If Streamlit or other dependencies are missing, the launcher will:
   - Detect the missing dependencies
   - Ask if you want to install them automatically
   - Install all required dependencies from the project's requirements.txt file

This is the easiest way to get started, as the launcher handles all dependency management for you.

### Option 2: Manual Installation

If you prefer to install dependencies manually:

1. Clone this repository:
```bash
git clone <repository-url>
cd <repository-directory>
```

2. Create a virtual environment (optional but recommended):
```bash
python -m venv .venv
# On Windows
.venv\Scripts\activate
# On macOS/Linux
source .venv/bin/activate
```

3. Install the dependencies for the project you want to run:
```bash
# For Quantum Circuit Simulator
pip install -r quantum_simulator/requirements.txt

# For Entanglement Visualizer
pip install -r entanglement_visualizer/requirements.txt

# For Quantum Tic Tac Toe
pip install -r quantum_tictactoe/requirements.txt
```

## Running the Projects

There are two ways to run the projects: using the launcher scripts or directly with Streamlit.

### Using the Launcher Scripts (Recommended)

The easiest way to run the projects is to use the launcher scripts, which will:
- Automatically use the correct Streamlit command
- Check if required dependencies are installed
- Offer to install missing dependencies automatically
- Provide clear feedback during the installation process
- Work reliably on all operating systems, including Windows with spaces in the path

#### Main Launcher

To choose which project to run from a menu:

```bash
python launcher.py
```

This will display a menu where you can select which project to launch.

#### Individual Project Launchers

Each project also has its own launcher script:

```bash
# For Quantum Circuit Simulator
python quantum_simulator/launcher.py

# For Entanglement Visualizer
python entanglement_visualizer/launcher.py

# For Quantum Tic Tac Toe
python quantum_tictactoe/launcher.py
```

If Streamlit or other dependencies are missing when you run a launcher script, you'll be prompted to install them automatically. This makes it easy to get started without having to manually install dependencies.

### Using Streamlit Directly

If you prefer, you can also run the projects directly with Streamlit:

#### Quantum Circuit Simulator

```bash
cd quantum_simulator
streamlit run main.py
```

This will open a web interface where you can:
- Add quantum gates to qubits
- Visualize the circuit
- Run simulations
- View measurement results and quantum states

#### Entanglement Visualizer

```bash
cd entanglement_visualizer
streamlit run app.py
```

This will open a web interface where you can:
- Create different entangled states (Bell states, GHZ states, W states)
- Choose measurement bases
- Visualize correlations between entangled qubits
- Explore Bell's inequality

#### Quantum Tic Tac Toe

```bash
cd quantum_tictactoe
streamlit run app.py
```

This will open a web interface where you can:
- Play Tic Tac Toe with quantum moves (superpositions)
- Observe entanglement between positions
- Force quantum collapses
- Play against an AI opponent

> **Note:** It's important to use the `streamlit run` command when running the applications directly, not `python`. The launcher scripts handle this automatically for you.

## Quantum Concepts

### Superposition

In quantum computing, qubits can exist in multiple states simultaneously, unlike classical bits that can only be 0 or 1. This is called superposition.

For example, a qubit can be in a state that is a combination of |0⟩ and |1⟩:
|ψ⟩ = α|0⟩ + β|1⟩

where α and β are complex numbers such that |α|² + |β|² = 1.

### Entanglement

Entanglement is a quantum phenomenon where two or more qubits become correlated in such a way that the quantum state of each qubit cannot be described independently of the others.

The Bell states are the simplest examples of entangled states:
- |Φ⁺⟩ = (|00⟩ + |11⟩)/√2
- |Φ⁻⟩ = (|00⟩ - |11⟩)/√2
- |Ψ⁺⟩ = (|01⟩ + |10⟩)/√2
- |Ψ⁻⟩ = (|01⟩ - |10⟩)/√2

### Measurement

When we measure a qubit in superposition, it collapses to one of its basis states with a probability determined by the amplitudes of the quantum state.

For a qubit in state |ψ⟩ = α|0⟩ + β|1⟩:
- The probability of measuring 0 is |α|²
- The probability of measuring 1 is |β|²

## Project Details

### Quantum Circuit Simulator

The Quantum Circuit Simulator allows you to:
- Add various quantum gates (Hadamard, Pauli-X/Y/Z, CNOT, etc.)
- Visualize the circuit diagram
- Run simulations with multiple shots
- View the measurement probabilities
- Explore the quantum state in different representations (statevector, Bloch sphere)

### Entanglement Visualizer

The Entanglement Visualizer allows you to:
- Create different types of entangled states
- Measure qubits in different bases
- Visualize the correlations between measurements
- Test Bell's inequality
- Explore the density matrix and reduced density matrices

### Quantum Tic Tac Toe

Quantum Tic Tac Toe introduces quantum mechanics to the classic game:
- Each move is a superposition of two positions
- Moves collapse when they interfere with other moves
- Players can force collapses strategically
- The game visualizes quantum entanglement between positions
- You can play against an AI with different difficulty levels

## Troubleshooting

### Common Issues

#### "Error launching application: [WinError 2] The specified file was not found"
This error can occur on Windows systems, especially when the project path contains spaces. The launcher scripts have been updated to handle this issue. If you still encounter this error:
- Make sure Streamlit is properly installed in your Python environment
- Try running the launcher script with administrator privileges
- Ensure your Python environment is activated if you're using a virtual environment

#### "ImportError: cannot import name 'Aer' from 'qiskit'"
This error occurs because in newer versions of Qiskit, the Aer module has been moved to a separate package. To fix this:
- Make sure you have the qiskit-aer package installed: `pip install qiskit-aer`
- The launcher scripts should detect and install this dependency automatically

#### "Session state does not function when running a script without `streamlit run`"
This warning appears when trying to run a Streamlit app directly with Python instead of using the `streamlit run` command. Always use the launcher scripts or the `streamlit run` command to run the applications.

## Credits

These projects were created to demonstrate quantum computing concepts in an interactive and visual way. They use the following open-source libraries:
- [Qiskit](https://qiskit.org/) - IBM's open-source quantum computing framework
- [Streamlit](https://streamlit.io/) - Framework for creating web applications
- [NumPy](https://numpy.org/) - Numerical computing library
- [Matplotlib](https://matplotlib.org/) and [Plotly](https://plotly.com/) - Data visualization libraries
- [NetworkX](https://networkx.org/) - Network analysis library