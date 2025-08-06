#!/usr/bin/env python
"""
launcher.py - Main launcher script for Quantum Computing Projects

This script provides a simple interface to launch any of the three quantum computing projects:
1. Quantum Circuit Simulator
2. Entanglement Visualizer
3. Quantum Tic Tac Toe

It's a convenience wrapper that ensures the applications are run properly with Streamlit.
It can also install required dependencies if they are missing.
"""

import os
import subprocess
import sys
import importlib.util
import pkg_resources

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Print the header for the launcher."""
    print("=" * 60)
    print("             QUANTUM COMPUTING PROJECTS LAUNCHER")
    print("=" * 60)
    print("\nThis launcher will help you run the quantum computing projects correctly.")
    print("Each project is a Streamlit application that needs to be run with the")
    print("'streamlit run' command, which this launcher will handle for you.\n")

def print_menu():
    """Print the menu of available projects."""
    print("Available Projects:")
    print("1. Quantum Circuit Simulator - Build and simulate quantum circuits")
    print("2. Entanglement Visualizer - Explore quantum entanglement")
    print("3. Quantum Tic Tac Toe - Play a quantum version of Tic Tac Toe")
    print("4. Exit")
    print("\nEnter the number of the project you want to launch:")

def check_package_installed(package_name):
    """
    Check if a Python package is installed.
    
    Args:
        package_name: Name of the package to check
        
    Returns:
        True if the package is installed, False otherwise
    """
    try:
        pkg_resources.get_distribution(package_name)
        return True
    except pkg_resources.DistributionNotFound:
        return False

def install_requirements(requirements_file):
    """
    Install packages from a requirements file.
    
    Args:
        requirements_file: Path to the requirements.txt file
        
    Returns:
        True if installation was successful, False otherwise
    """
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requirements_file])
        return True
    except subprocess.CalledProcessError:
        return False

def launch_project(project_dir, script_name):
    """
    Launch a project using Streamlit.
    
    Args:
        project_dir: Directory of the project
        script_name: Name of the script to run (main.py or app.py)
    """
    # Get the absolute path to the project directory
    base_dir = os.path.dirname(os.path.abspath(__file__))
    project_path = os.path.join(base_dir, project_dir)
    
    # Path to the script file
    script_file = os.path.join(project_path, script_name)
    
    # Path to the requirements file
    requirements_file = os.path.join(project_path, "requirements.txt")
    
    # Check if the script exists
    if not os.path.exists(script_file):
        print(f"Error: {script_file} not found.")
        return False
    
    # Check if streamlit is installed
    if not check_package_installed("streamlit"):
        print("Error: Streamlit not found. This application requires Streamlit to run.")
        
        # Ask user if they want to install dependencies
        install_choice = input("Would you like to install Streamlit and other required dependencies now? (y/n): ")
        
        if install_choice.lower() in ['y', 'yes']:
            print("Installing required dependencies...")
            if install_requirements(requirements_file):
                print("Dependencies installed successfully!")
            else:
                print("Failed to install dependencies. Please install them manually with:")
                print(f"pip install -r {requirements_file}")
                return False
        else:
            print("You can install the required dependencies manually with:")
            print(f"pip install -r {requirements_file}")
            return False
    
    # Build the streamlit run command using Python executable
    # This ensures streamlit is found even if it's not in the PATH
    cmd = [sys.executable, "-m", "streamlit", "run", script_file]
    
    try:
        # Run the streamlit command
        subprocess.run(cmd)
        return True
    except Exception as e:
        print(f"Error launching application: {e}")
        print(f"Command attempted: {' '.join(cmd)}")
        print("Make sure streamlit is installed correctly in your Python environment.")
        return False

def main():
    """Main function to run the launcher."""
    while True:
        clear_screen()
        print_header()
        print_menu()
        
        choice = input("> ").strip()
        
        if choice == "1":
            print("\nLaunching Quantum Circuit Simulator...")
            launch_project("quantum_simulator", "main.py")
        elif choice == "2":
            print("\nLaunching Entanglement Visualizer...")
            launch_project("entanglement_visualizer", "app.py")
        elif choice == "3":
            print("\nLaunching Quantum Tic Tac Toe...")
            launch_project("quantum_tictactoe", "app.py")
        elif choice == "4":
            print("\nExiting launcher. Goodbye!")
            break
        else:
            print("\nInvalid choice. Please enter a number between 1 and 4.")
            input("Press Enter to continue...")

if __name__ == "__main__":
    main()