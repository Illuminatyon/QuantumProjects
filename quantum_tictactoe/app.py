"""
app.py - Streamlit interface for Quantum Tic Tac Toe

This is the main entry point for the Quantum Tic Tac Toe application.
It provides a user interface for playing the game with quantum superpositions.
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from game import QuantumTicTacToe, AIPlayer
from quantum_engine import QuantumMove
from typing import Dict, List, Tuple, Set, Optional, Any
import time
import random

# Set page configuration
st.set_page_config(
    page_title="Quantum Tic Tac Toe",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
def set_page_style():
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
    .board-cell {
        width: 100px;
        height: 100px;
        border: 2px solid #2c3e50;
        display: flex;
        justify-content: center;
        align-items: center;
        font-size: 24px;
        font-weight: bold;
        cursor: pointer;
        background-color: white;
    }
    .board-cell:hover {
        background-color: #eaf2f8;
    }
    .board-cell-selected {
        background-color: #d4e6f1;
    }
    .board-cell-collapsed-x {
        color: #e74c3c;
    }
    .board-cell-collapsed-o {
        color: #2980b9;
    }
    .board-cell-superposition {
        background-color: #f9e79f;
    }
    .board-row {
        display: flex;
    }
    .game-info {
        margin-top: 20px;
        padding: 10px;
        background-color: white;
        border-radius: 5px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    .move-history {
        max-height: 300px;
        overflow-y: auto;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
def init_session_state():
    if 'game' not in st.session_state:
        st.session_state.game = QuantumTicTacToe(board_size=3)
    
    if 'ai_player' not in st.session_state:
        st.session_state.ai_player = AIPlayer(difficulty="medium")
    
    if 'game_mode' not in st.session_state:
        st.session_state.game_mode = "human_vs_human"
    
    if 'show_entanglement' not in st.session_state:
        st.session_state.show_entanglement = True
    
    if 'show_superpositions' not in st.session_state:
        st.session_state.show_superpositions = True
    
    if 'ai_thinking' not in st.session_state:
        st.session_state.ai_thinking = False

# Reset the game
def reset_game():
    st.session_state.game.reset_game()
    st.session_state.ai_thinking = False

# Handle cell click
def handle_cell_click(row, col):
    if st.session_state.game.is_game_over():
        return
    
    # If it's AI's turn in human vs AI mode, don't allow clicks
    if (st.session_state.game_mode == "human_vs_ai" and 
        st.session_state.game.get_current_player() == "O"):
        return
    
    # Select the position
    st.session_state.game.select_position(row, col)
    
    # If it's AI's turn after the move, make AI move
    if (st.session_state.game_mode == "human_vs_ai" and 
        not st.session_state.game.is_game_over() and
        st.session_state.game.get_current_player() == "O"):
        st.session_state.ai_thinking = True
        st.rerun()

# Handle collapse click
def handle_collapse_click(move_index, position):
    if st.session_state.game.is_game_over():
        return
    
    # If it's AI's turn in human vs AI mode, don't allow clicks
    if (st.session_state.game_mode == "human_vs_ai" and 
        st.session_state.game.get_current_player() == "O"):
        return
    
    # Force the collapse
    st.session_state.game.force_collapse(move_index, position)
    
    # If it's AI's turn after the collapse, make AI move
    if (st.session_state.game_mode == "human_vs_ai" and 
        not st.session_state.game.is_game_over() and
        st.session_state.game.get_current_player() == "O"):
        st.session_state.ai_thinking = True
        st.rerun()

# Make AI move
def make_ai_move():
    if st.session_state.ai_thinking and not st.session_state.game.is_game_over():
        # Add a small delay to simulate thinking
        time.sleep(0.5)
        
        # Check if there are uncollapsed moves that need to be collapsed
        uncollapsed_moves = st.session_state.game.get_uncollapsed_moves()
        if uncollapsed_moves and random.random() < 0.3:  # 30% chance to collapse instead of making a new move
            move_index, position = st.session_state.ai_player.decide_collapse(st.session_state.game)
            st.session_state.game.force_collapse(move_index, position)
        else:
            # Make a new move
            pos1, pos2 = st.session_state.ai_player.make_move(st.session_state.game)
            st.session_state.game.make_move(pos1, pos2)
        
        st.session_state.ai_thinking = False

# Render the game board
def render_board():
    game = st.session_state.game
    board_size = game.get_board_size()
    
    # Get the quantum board state
    quantum_board = game.get_quantum_board()
    
    # Get the classical board state (collapsed moves)
    classical_board = game.get_classical_board()
    
    # Get the entanglement graph
    entanglement_graph = game.get_entanglement_graph() if st.session_state.show_entanglement else None
    
    # Get the current selected positions
    selected_positions = game.get_current_move_positions()
    
    # Create a container for the board
    board_container = st.container()
    
    with board_container:
        # Render the board
        for row in range(board_size):
            cols = st.columns(board_size)
            for col in range(board_size):
                position = (row, col)
                
                # Determine cell state and content
                cell_content = ""
                cell_class = "board-cell"
                
                # Check if the position has a collapsed move
                if classical_board[row][col] is not None:
                    cell_content = classical_board[row][col]
                    cell_class += f" board-cell-collapsed-{cell_content.lower()}"
                
                # Check if the position is in superposition
                elif position in quantum_board and st.session_state.show_superpositions:
                    moves_at_position = quantum_board[position]
                    if moves_at_position:
                        # Show superposition with player symbols and move numbers
                        superposition_content = []
                        for move in moves_at_position:
                            if not move.collapsed:
                                superposition_content.append(f"{move.player}{move.move_num}")
                        
                        if superposition_content:
                            cell_content = ",".join(superposition_content)
                            cell_class += " board-cell-superposition"
                
                # Check if the position is selected for the current move
                if position in selected_positions:
                    cell_class += " board-cell-selected"
                
                # Render the cell with a button
                with cols[col]:
                    if st.button(
                        cell_content if cell_content else " ",
                        key=f"cell_{row}_{col}",
                        on_click=handle_cell_click,
                        args=(row, col),
                        use_container_width=True,
                        disabled=st.session_state.ai_thinking
                    ):
                        pass
        
        # Render entanglement graph if enabled
        if entanglement_graph and any(connections for connections in entanglement_graph.values()):
            st.subheader("Quantum Entanglement")
            
            # Create a NetworkX graph
            G = nx.Graph()
            
            # Add nodes (positions)
            for row in range(board_size):
                for col in range(board_size):
                    G.add_node((row, col), pos=(col, -row))  # Position for visualization
            
            # Add edges (entanglements)
            for pos, connected_positions in entanglement_graph.items():
                for connected_pos in connected_positions:
                    G.add_edge(pos, connected_pos)
            
            # Get node positions for visualization
            pos = nx.get_node_attributes(G, 'pos')
            
            # Create a matplotlib figure
            fig, ax = plt.subplots(figsize=(5, 5))
            
            # Draw the graph
            nx.draw(
                G, pos, ax=ax,
                with_labels=True,
                node_color='lightblue',
                node_size=500,
                font_size=10,
                font_weight='bold',
                labels={node: f"({node[0]},{node[1]})" for node in G.nodes()},
                edge_color='blue',
                width=2,
                alpha=0.7
            )
            
            # Display the graph
            st.pyplot(fig)

# Render game info and controls
def render_game_info():
    game = st.session_state.game
    
    # Game status
    st.subheader("Game Status")
    
    # Current player
    current_player = game.get_current_player()
    st.write(f"Current Player: **{current_player}**")
    
    # Selected positions
    selected_positions = game.get_current_move_positions()
    if selected_positions:
        st.write(f"Selected Position: ({selected_positions[0][0]}, {selected_positions[0][1]})")
    
    # Game over status
    if game.is_game_over():
        winner = game.get_winner()
        if winner:
            st.success(f"Game Over! Player {winner} wins!")
        else:
            st.info("Game Over! It's a draw!")
    
    # Uncollapsed moves
    uncollapsed_moves = game.get_uncollapsed_moves()
    if uncollapsed_moves:
        st.subheader("Uncollapsed Quantum Moves")
        
        # Create a container for the uncollapsed moves
        moves_container = st.container()
        
        with moves_container:
            for i, move in enumerate(uncollapsed_moves):
                move_str = str(move)
                positions_str = ", ".join([f"({pos[0]}, {pos[1]})" for pos in move.positions])
                
                # Create a row for each move
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.write(f"**Move {i}**: Player {move.player}, Positions: {positions_str}")
                
                with col2:
                    # Add buttons to collapse to each position
                    for pos in move.positions:
                        if st.button(
                            f"Collapse to ({pos[0]}, {pos[1]})",
                            key=f"collapse_{i}_{pos[0]}_{pos[1]}",
                            on_click=handle_collapse_click,
                            args=(game.board.moves.index(move), pos),
                            disabled=st.session_state.ai_thinking
                        ):
                            pass
    
    # Move history
    st.subheader("Move History")
    history = game.get_history()
    
    if history:
        history_container = st.container()
        
        with history_container:
            for i, event in enumerate(history):
                if "move" in event:
                    pos1, pos2 = event["move"]
                    st.write(f"{i+1}. Player {event['player']} moved to ({pos1[0]}, {pos1[1]}) and ({pos2[0]}, {pos2[1]})")
                elif "collapse" in event:
                    move_index, position = event["collapse"]
                    st.write(f"{i+1}. Player {event['player']} collapsed move {move_index} to ({position[0]}, {position[1]})")
                
                if event["collapsed_moves"]:
                    st.write(f"   Collapsed moves: {', '.join(event['collapsed_moves'])}")
    else:
        st.write("No moves yet.")

# Render sidebar controls
def render_sidebar():
    st.sidebar.title("Quantum Tic Tac Toe")
    
    # Game mode selection
    st.sidebar.header("Game Mode")
    game_mode = st.sidebar.radio(
        "Select Game Mode",
        ["Human vs Human", "Human vs AI"],
        index=0 if st.session_state.game_mode == "human_vs_human" else 1
    )
    
    # Update game mode
    new_game_mode = "human_vs_human" if game_mode == "Human vs Human" else "human_vs_ai"
    if new_game_mode != st.session_state.game_mode:
        st.session_state.game_mode = new_game_mode
        reset_game()
    
    # AI difficulty (only shown in Human vs AI mode)
    if st.session_state.game_mode == "human_vs_ai":
        st.sidebar.header("AI Difficulty")
        ai_difficulty = st.sidebar.radio(
            "Select AI Difficulty",
            ["Easy", "Medium", "Hard"],
            index=1  # Default to Medium
        )
        
        # Update AI difficulty
        new_difficulty = ai_difficulty.lower()
        if new_difficulty != st.session_state.ai_player.difficulty:
            st.session_state.ai_player = AIPlayer(difficulty=new_difficulty)
    
    # Visualization options
    st.sidebar.header("Visualization Options")
    
    show_entanglement = st.sidebar.checkbox(
        "Show Entanglement Graph",
        value=st.session_state.show_entanglement
    )
    if show_entanglement != st.session_state.show_entanglement:
        st.session_state.show_entanglement = show_entanglement
    
    show_superpositions = st.sidebar.checkbox(
        "Show Superpositions",
        value=st.session_state.show_superpositions
    )
    if show_superpositions != st.session_state.show_superpositions:
        st.session_state.show_superpositions = show_superpositions
    
    # Reset game button
    if st.sidebar.button("Reset Game"):
        reset_game()
    
    # Quantum concepts explanation
    st.sidebar.header("Quantum Concepts")
    with st.sidebar.expander("Superposition"):
        st.write("""
        In Quantum Tic Tac Toe, each move exists in a **superposition** of two positions until it's measured (collapsed).
        
        This means a player's mark can be in two places at once, representing the quantum principle that particles can exist in multiple states simultaneously until observed.
        """)
    
    with st.sidebar.expander("Entanglement"):
        st.write("""
        When two quantum moves share a position, they become **entangled**. If one move collapses, it can force other entangled moves to collapse as well.
        
        This represents quantum entanglement, where the state of one particle is connected to the state of another, regardless of distance.
        """)
    
    with st.sidebar.expander("Measurement/Collapse"):
        st.write("""
        **Measurement** (or collapse) happens when:
        
        1. Two moves interfere at the same position
        2. A player chooses to force a collapse
        
        When a move collapses, it randomly chooses one of its superposition positions, following the probabilistic nature of quantum measurement.
        """)

# Main function
def main():
    # Initialize session state
    init_session_state()
    
    # Apply custom styling
    set_page_style()
    
    # Render sidebar
    render_sidebar()
    
    # Page title
    st.title("Quantum Tic Tac Toe")
    st.markdown("""
    Play Tic Tac Toe with a quantum twist! Each move exists in a superposition of two positions until it collapses.
    """)
    
    # Create a two-column layout for the game board and info
    col1, col2 = st.columns([3, 2])
    
    with col1:
        # Render the game board
        render_board()
    
    with col2:
        # Render game info and controls
        render_game_info()
    
    # Make AI move if it's AI's turn
    if st.session_state.ai_thinking:
        make_ai_move()
        st.rerun()

if __name__ == "__main__":
    main()