#!/usr/bin/env python
"""
launcher.py - Launcher script for the Quantum Tic Tac Toe

This script launches the Quantum Tic Tac Toe game using the correct Streamlit command.
It's a convenience wrapper that ensures the application is run properly.
It can also install required dependencies if they are missing.
"""

import os
import subprocess
import sys
import importlib.util
import pkg_resources

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

def main():
    """
    Launch the Quantum Tic Tac Toe game using Streamlit.
    """
    print("Launching Quantum Tic Tac Toe...")
    
    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Path to the app.py file
    app_file = os.path.join(script_dir, "app.py")
    
    # Path to the requirements.txt file
    requirements_file = os.path.join(script_dir, "requirements.txt")
    
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
                sys.exit(1)
        else:
            print("You can install the required dependencies manually with:")
            print(f"pip install -r {requirements_file}")
            sys.exit(1)
    
    # Build the streamlit run command using Python executable
    # This ensures streamlit is found even if it's not in the PATH
    cmd = [sys.executable, "-m", "streamlit", "run", app_file]
    
    # Add any additional arguments
    if len(sys.argv) > 1:
        cmd.extend(sys.argv[1:])
    
    try:
        # Run the streamlit command
        subprocess.run(cmd)
    except Exception as e:
        print(f"Error launching application: {e}")
        print(f"Command attempted: {' '.join(cmd)}")
        print("Make sure streamlit is installed correctly in your Python environment.")
        sys.exit(1)

if __name__ == "__main__":
    main()