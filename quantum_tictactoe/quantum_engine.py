"""
quantum_engine.py - Quantum mechanics for the Quantum Tic Tac Toe game

This module provides the quantum mechanical functionality for the Quantum Tic Tac Toe game,
including superpositions, entanglement, and measurement.
"""

import numpy as np
from typing import Dict, List, Tuple, Set, Optional, Union, Any
import random


class QuantumMove:
    """
    Represents a quantum move in the Quantum Tic Tac Toe game.
    
    A quantum move is a superposition of two possible positions on the board.
    """
    
    def __init__(self, pos1: Tuple[int, int], pos2: Tuple[int, int], player: str, move_num: int):
        """
        Initialize a quantum move.
        
        Args:
            pos1: First position (row, col) in the superposition
            pos2: Second position (row, col) in the superposition
            player: Player making the move ('X' or 'O')
            move_num: Move number (used for tracking move order)
        """
        self.positions = [pos1, pos2]
        self.player = player
        self.move_num = move_num
        self.collapsed = False
        self.collapsed_position = None
    
    def __str__(self) -> str:
        """String representation of the quantum move."""
        if self.collapsed:
            return f"{self.player}{self.move_num}@{self.collapsed_position}"
        else:
            return f"{self.player}{self.move_num}@({self.positions[0]},{self.positions[1]})"
    
    def collapse_to(self, position: Tuple[int, int]):
        """
        Collapse the quantum move to a specific position.
        
        Args:
            position: Position to collapse to (must be one of the superposition positions)
        """
        if position not in self.positions:
            raise ValueError(f"Cannot collapse to {position}, not in superposition {self.positions}")
        
        self.collapsed = True
        self.collapsed_position = position
    
    def get_positions(self) -> List[Tuple[int, int]]:
        """Get the positions in the superposition (or the collapsed position if collapsed)."""
        if self.collapsed:
            return [self.collapsed_position]
        else:
            return self.positions
    
    def is_in_superposition(self, position: Tuple[int, int]) -> bool:
        """Check if a position is part of this quantum move's superposition."""
        return position in self.positions and not self.collapsed
    
    def is_collapsed_at(self, position: Tuple[int, int]) -> bool:
        """Check if this quantum move has collapsed at the given position."""
        return self.collapsed and self.collapsed_position == position


class QuantumBoard:
    """
    Represents the quantum state of the Tic Tac Toe board.
    
    The quantum board tracks all quantum moves and their superpositions,
    handles collapses due to interference, and determines the game state.
    """
    
    def __init__(self, size: int = 3):
        """
        Initialize a quantum board.
        
        Args:
            size: Size of the board (default: 3x3)
        """
        self.size = size
        self.moves: List[QuantumMove] = []
        self.move_count = 0
        self.current_player = 'X'  # X goes first
        self.game_over = False
        self.winner = None
    
    def make_move(self, pos1: Tuple[int, int], pos2: Tuple[int, int]) -> List[QuantumMove]:
        """
        Make a quantum move on the board.
        
        Args:
            pos1: First position (row, col) in the superposition
            pos2: Second position (row, col) in the superposition
            
        Returns:
            List of moves that collapsed due to this move
        """
        # Validate positions
        for pos in [pos1, pos2]:
            row, col = pos
            if not (0 <= row < self.size and 0 <= col < self.size):
                raise ValueError(f"Position {pos} is outside the board")
        
        # Create the new move
        self.move_count += 1
        new_move = QuantumMove(pos1, pos2, self.current_player, self.move_count)
        self.moves.append(new_move)
        
        # Check for collapses due to interference
        collapsed_moves = self._check_for_collapses()
        
        # Switch player
        self.current_player = 'O' if self.current_player == 'X' else 'X'
        
        # Check if the game is over
        self._check_game_state()
        
        return collapsed_moves
    
    def _check_for_collapses(self) -> List[QuantumMove]:
        """
        Check if any moves need to collapse due to interference.
        
        Returns:
            List of moves that collapsed
        """
        # Keep track of which moves collapsed
        collapsed_moves = []
        
        # Build a map of positions to uncollapsed moves
        position_to_moves: Dict[Tuple[int, int], List[QuantumMove]] = {}
        for move in self.moves:
            if not move.collapsed:
                for pos in move.positions:
                    if pos not in position_to_moves:
                        position_to_moves[pos] = []
                    position_to_moves[pos].append(move)
        
        # Check for positions with multiple moves (interference)
        for pos, moves in position_to_moves.items():
            if len(moves) > 1:
                # There's interference at this position
                self._resolve_interference(pos, moves)
                collapsed_moves.extend(moves)
        
        return collapsed_moves
    
    def _resolve_interference(self, position: Tuple[int, int], moves: List[QuantumMove]):
        """
        Resolve interference between quantum moves at a position.
        
        When multiple moves interfere, they all collapse, with each move
        randomly collapsing to one of its superposition positions.
        
        Args:
            position: Position where interference occurs
            moves: List of moves that are interfering
        """
        # For each move, decide whether it collapses to this position or its alternative
        for move in moves:
            # If the move has only this position in its superposition, it must collapse here
            if len(move.get_positions()) == 1:
                move.collapse_to(position)
                continue
            
            # Otherwise, randomly decide where it collapses
            # 50% chance to collapse to this position, 50% to the other position
            if random.random() < 0.5:
                move.collapse_to(position)
            else:
                # Collapse to the other position in the superposition
                other_pos = move.positions[0] if move.positions[1] == position else move.positions[1]
                move.collapse_to(other_pos)
        
        # After resolving interference, check if new interferences were created
        self._check_for_collapses()
    
    def force_collapse(self, move_index: int, position: Tuple[int, int]) -> List[QuantumMove]:
        """
        Force a specific move to collapse to a specific position.
        
        Args:
            move_index: Index of the move to collapse
            position: Position to collapse to
            
        Returns:
            List of moves that collapsed as a result
        """
        if move_index < 0 or move_index >= len(self.moves):
            raise ValueError(f"Invalid move index: {move_index}")
        
        move = self.moves[move_index]
        if move.collapsed:
            raise ValueError(f"Move {move_index} is already collapsed")
        
        if position not in move.positions:
            raise ValueError(f"Position {position} is not in the superposition of move {move_index}")
        
        # Collapse the move
        move.collapse_to(position)
        
        # Check for cascading collapses
        collapsed_moves = self._check_for_collapses()
        collapsed_moves.append(move)
        
        # Check if the game is over
        self._check_game_state()
        
        return collapsed_moves
    
    def _check_game_state(self):
        """Check if the game is over (win or draw)."""
        # Get the classical board state (only considering collapsed moves)
        board = self.get_classical_board()
        
        # Check for a win
        winner = self._check_winner(board)
        if winner:
            self.game_over = True
            self.winner = winner
            return
        
        # Check for a draw (all cells filled with collapsed moves)
        if all(cell is not None for row in board for cell in row):
            self.game_over = True
            self.winner = None  # Draw
            return
        
        # Check if all moves are collapsed and there's no winner
        if all(move.collapsed for move in self.moves) and not self.winner:
            self.game_over = True
            self.winner = None  # Draw
    
    def _check_winner(self, board: List[List[Optional[str]]]) -> Optional[str]:
        """
        Check if there's a winner on the board.
        
        Args:
            board: Classical board state
            
        Returns:
            Winner ('X' or 'O') or None if no winner
        """
        # Check rows
        for row in board:
            if row[0] is not None and all(cell == row[0] for cell in row):
                return row[0]
        
        # Check columns
        for col in range(self.size):
            if board[0][col] is not None and all(board[row][col] == board[0][col] for row in range(self.size)):
                return board[0][col]
        
        # Check diagonals
        if board[0][0] is not None and all(board[i][i] == board[0][0] for i in range(self.size)):
            return board[0][0]
        
        if board[0][self.size-1] is not None and all(board[i][self.size-1-i] == board[0][self.size-1] for i in range(self.size)):
            return board[0][self.size-1]
        
        return None
    
    def get_classical_board(self) -> List[List[Optional[str]]]:
        """
        Get the classical board state, considering only collapsed moves.
        
        Returns:
            2D list representing the board, with each cell containing 'X', 'O', or None
        """
        # Initialize empty board
        board = [[None for _ in range(self.size)] for _ in range(self.size)]
        
        # Fill in collapsed moves
        for move in self.moves:
            if move.collapsed:
                row, col = move.collapsed_position
                board[row][col] = move.player
        
        return board
    
    def get_quantum_board(self) -> Dict[Tuple[int, int], List[QuantumMove]]:
        """
        Get the quantum board state, including all superpositions.
        
        Returns:
            Dictionary mapping positions to lists of quantum moves at those positions
        """
        # Initialize empty board
        quantum_board: Dict[Tuple[int, int], List[QuantumMove]] = {}
        
        # Add all moves (collapsed and uncollapsed)
        for move in self.moves:
            positions = move.get_positions()
            for pos in positions:
                if pos not in quantum_board:
                    quantum_board[pos] = []
                quantum_board[pos].append(move)
        
        return quantum_board
    
    def get_move_at(self, position: Tuple[int, int]) -> List[QuantumMove]:
        """
        Get all moves (collapsed or in superposition) at a specific position.
        
        Args:
            position: Position to check
            
        Returns:
            List of moves at the position
        """
        moves_at_position = []
        for move in self.moves:
            if move.collapsed and move.collapsed_position == position:
                moves_at_position.append(move)
            elif not move.collapsed and position in move.positions:
                moves_at_position.append(move)
        
        return moves_at_position
    
    def is_valid_move(self, pos1: Tuple[int, int], pos2: Tuple[int, int]) -> bool:
        """
        Check if a quantum move is valid.
        
        A move is valid if:
        1. Both positions are on the board
        2. The positions are different
        3. Neither position has a collapsed move
        
        Args:
            pos1: First position in the superposition
            pos2: Second position in the superposition
            
        Returns:
            True if the move is valid, False otherwise
        """
        # Check if positions are on the board
        for pos in [pos1, pos2]:
            row, col = pos
            if not (0 <= row < self.size and 0 <= col < self.size):
                return False
        
        # Check if positions are different
        if pos1 == pos2:
            return False
        
        # Check if either position has a collapsed move
        for pos in [pos1, pos2]:
            for move in self.moves:
                if move.is_collapsed_at(pos):
                    return False
        
        return True
    
    def get_valid_moves(self) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
        """
        Get all valid quantum moves.
        
        Returns:
            List of valid moves, each represented as a pair of positions
        """
        valid_moves = []
        
        # Get positions that already have collapsed moves
        occupied_positions = set()
        for move in self.moves:
            if move.collapsed:
                occupied_positions.add(move.collapsed_position)
        
        # Generate all possible pairs of positions
        for row1 in range(self.size):
            for col1 in range(self.size):
                pos1 = (row1, col1)
                if pos1 in occupied_positions:
                    continue
                
                for row2 in range(self.size):
                    for col2 in range(self.size):
                        pos2 = (row2, col2)
                        if pos2 in occupied_positions or pos1 == pos2:
                            continue
                        
                        valid_moves.append((pos1, pos2))
        
        return valid_moves
    
    def get_entanglement_graph(self) -> Dict[Tuple[int, int], Set[Tuple[int, int]]]:
        """
        Get the entanglement graph of the board.
        
        The entanglement graph shows which positions are entangled through
        quantum superpositions.
        
        Returns:
            Dictionary mapping positions to sets of entangled positions
        """
        entanglement_graph: Dict[Tuple[int, int], Set[Tuple[int, int]]] = {}
        
        # Initialize the graph with all positions
        for row in range(self.size):
            for col in range(self.size):
                entanglement_graph[(row, col)] = set()
        
        # Add entanglement edges from uncollapsed moves
        for move in self.moves:
            if not move.collapsed and len(move.positions) > 1:
                pos1, pos2 = move.positions
                entanglement_graph[pos1].add(pos2)
                entanglement_graph[pos2].add(pos1)
        
        return entanglement_graph
    
    def get_move_by_index(self, index: int) -> Optional[QuantumMove]:
        """
        Get a move by its index.
        
        Args:
            index: Index of the move
            
        Returns:
            The move, or None if the index is invalid
        """
        if 0 <= index < len(self.moves):
            return self.moves[index]
        return None
    
    def get_uncollapsed_moves(self) -> List[QuantumMove]:
        """
        Get all uncollapsed moves.
        
        Returns:
            List of uncollapsed moves
        """
        return [move for move in self.moves if not move.collapsed]
    
    def get_collapsed_moves(self) -> List[QuantumMove]:
        """
        Get all collapsed moves.
        
        Returns:
            List of collapsed moves
        """
        return [move for move in self.moves if move.collapsed]
    
    def get_superposition_count(self, position: Tuple[int, int]) -> int:
        """
        Get the number of uncollapsed moves that include a position in their superposition.
        
        Args:
            position: Position to check
            
        Returns:
            Number of uncollapsed moves at the position
        """
        count = 0
        for move in self.moves:
            if not move.collapsed and position in move.positions:
                count += 1
        return count