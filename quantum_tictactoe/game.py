"""
game.py - Game logic for Quantum Tic Tac Toe

This module provides the game logic for Quantum Tic Tac Toe, including
game state management, move validation, and AI opponent functionality.
"""

from quantum_engine import QuantumBoard, QuantumMove
from typing import Dict, List, Tuple, Set, Optional, Union, Any
import random


class QuantumTicTacToe:
    """
    Main game class for Quantum Tic Tac Toe.
    
    This class manages the game state, handles player moves,
    and provides an interface for the UI.
    """
    
    def __init__(self, board_size: int = 3):
        """
        Initialize a new game of Quantum Tic Tac Toe.
        
        Args:
            board_size: Size of the board (default: 3x3)
        """
        self.board = QuantumBoard(size=board_size)
        self.history: List[Dict[str, Any]] = []
        self.current_move_positions: List[Tuple[int, int]] = []
    
    def get_board_size(self) -> int:
        """Get the size of the board."""
        return self.board.size
    
    def get_current_player(self) -> str:
        """Get the current player ('X' or 'O')."""
        return self.board.current_player
    
    def is_game_over(self) -> bool:
        """Check if the game is over."""
        return self.board.game_over
    
    def get_winner(self) -> Optional[str]:
        """Get the winner of the game ('X', 'O', or None for a draw or ongoing game)."""
        return self.board.winner
    
    def select_position(self, row: int, col: int) -> bool:
        """
        Select a position for the current quantum move.
        
        A quantum move consists of two positions. This method adds a position
        to the current move. When two positions are selected, the move is made.
        
        Args:
            row: Row index
            pos: Column index
            
        Returns:
            True if the position was successfully selected, False otherwise
        """
        position = (row, col)
        
        # Check if the position is valid
        if not self._is_valid_position(position):
            return False
        
        # Add the position to the current move
        self.current_move_positions.append(position)
        
        # If we have two positions, make the move
        if len(self.current_move_positions) == 2:
            pos1, pos2 = self.current_move_positions
            success = self.make_move(pos1, pos2)
            self.current_move_positions = []
            return success
        
        return True
    
    def _is_valid_position(self, position: Tuple[int, int]) -> bool:
        """
        Check if a position is valid for selection.
        
        A position is valid if:
        1. It's on the board
        2. It doesn't have a collapsed move
        3. It's not already selected for the current move
        
        Args:
            position: Position to check
            
        Returns:
            True if the position is valid, False otherwise
        """
        row, col = position
        
        # Check if the position is on the board
        if not (0 <= row < self.board.size and 0 <= col < self.board.size):
            return False
        
        # Check if the position already has a collapsed move
        for move in self.board.moves:
            if move.is_collapsed_at(position):
                return False
        
        # Check if the position is already selected for the current move
        if position in self.current_move_positions:
            return False
        
        return True
    
    def make_move(self, pos1: Tuple[int, int], pos2: Tuple[int, int]) -> bool:
        """
        Make a quantum move with the specified positions.
        
        Args:
            pos1: First position in the superposition
            pos2: Second position in the superposition
            
        Returns:
            True if the move was successfully made, False otherwise
        """
        # Check if the move is valid
        if not self.board.is_valid_move(pos1, pos2):
            return False
        
        # Record the game state before the move
        prev_state = self._get_game_state()
        
        # Make the move
        collapsed_moves = self.board.make_move(pos1, pos2)
        
        # Record the move in the history
        self.history.append({
            "player": prev_state["current_player"],
            "move": (pos1, pos2),
            "collapsed_moves": [str(move) for move in collapsed_moves],
            "prev_state": prev_state,
            "new_state": self._get_game_state()
        })
        
        return True
    
    def force_collapse(self, move_index: int, position: Tuple[int, int]) -> bool:
        """
        Force a specific move to collapse to a specific position.
        
        Args:
            move_index: Index of the move to collapse
            position: Position to collapse to
            
        Returns:
            True if the collapse was successful, False otherwise
        """
        # Check if the move exists and can be collapsed
        move = self.board.get_move_by_index(move_index)
        if move is None or move.collapsed or position not in move.positions:
            return False
        
        # Record the game state before the collapse
        prev_state = self._get_game_state()
        
        # Force the collapse
        collapsed_moves = self.board.force_collapse(move_index, position)
        
        # Record the collapse in the history
        self.history.append({
            "player": prev_state["current_player"],
            "collapse": (move_index, position),
            "collapsed_moves": [str(move) for move in collapsed_moves],
            "prev_state": prev_state,
            "new_state": self._get_game_state()
        })
        
        return True
    
    def _get_game_state(self) -> Dict[str, Any]:
        """
        Get a snapshot of the current game state.
        
        Returns:
            Dictionary containing the game state
        """
        return {
            "current_player": self.board.current_player,
            "game_over": self.board.game_over,
            "winner": self.board.winner,
            "classical_board": self.board.get_classical_board(),
            "uncollapsed_moves": [str(move) for move in self.board.get_uncollapsed_moves()],
            "collapsed_moves": [str(move) for move in self.board.get_collapsed_moves()]
        }
    
    def get_classical_board(self) -> List[List[Optional[str]]]:
        """
        Get the classical board state (only collapsed moves).
        
        Returns:
            2D list representing the board, with each cell containing 'X', 'O', or None
        """
        return self.board.get_classical_board()
    
    def get_quantum_board(self) -> Dict[Tuple[int, int], List[QuantumMove]]:
        """
        Get the quantum board state (all moves, collapsed and uncollapsed).
        
        Returns:
            Dictionary mapping positions to lists of quantum moves at those positions
        """
        return self.board.get_quantum_board()
    
    def get_uncollapsed_moves(self) -> List[QuantumMove]:
        """
        Get all uncollapsed moves.
        
        Returns:
            List of uncollapsed moves
        """
        return self.board.get_uncollapsed_moves()
    
    def get_collapsed_moves(self) -> List[QuantumMove]:
        """
        Get all collapsed moves.
        
        Returns:
            List of collapsed moves
        """
        return self.board.get_collapsed_moves()
    
    def get_entanglement_graph(self) -> Dict[Tuple[int, int], Set[Tuple[int, int]]]:
        """
        Get the entanglement graph of the board.
        
        Returns:
            Dictionary mapping positions to sets of entangled positions
        """
        return self.board.get_entanglement_graph()
    
    def get_superposition_count(self, position: Tuple[int, int]) -> int:
        """
        Get the number of uncollapsed moves that include a position in their superposition.
        
        Args:
            position: Position to check
            
        Returns:
            Number of uncollapsed moves at the position
        """
        return self.board.get_superposition_count(position)
    
    def get_move_at(self, position: Tuple[int, int]) -> List[QuantumMove]:
        """
        Get all moves (collapsed or in superposition) at a specific position.
        
        Args:
            position: Position to check
            
        Returns:
            List of moves at the position
        """
        return self.board.get_move_at(position)
    
    def get_valid_moves(self) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
        """
        Get all valid quantum moves.
        
        Returns:
            List of valid moves, each represented as a pair of positions
        """
        return self.board.get_valid_moves()
    
    def get_move_by_index(self, index: int) -> Optional[QuantumMove]:
        """
        Get a move by its index.
        
        Args:
            index: Index of the move
            
        Returns:
            The move, or None if the index is invalid
        """
        return self.board.get_move_by_index(index)
    
    def get_history(self) -> List[Dict[str, Any]]:
        """
        Get the game history.
        
        Returns:
            List of dictionaries representing the game history
        """
        return self.history
    
    def get_current_move_positions(self) -> List[Tuple[int, int]]:
        """
        Get the positions selected for the current move.
        
        Returns:
            List of selected positions (0, 1, or 2 positions)
        """
        return self.current_move_positions
    
    def clear_selected_positions(self):
        """Clear the positions selected for the current move."""
        self.current_move_positions = []
    
    def reset_game(self):
        """Reset the game to its initial state."""
        board_size = self.board.size
        self.board = QuantumBoard(size=board_size)
        self.history = []
        self.current_move_positions = []


class AIPlayer:
    """
    AI player for Quantum Tic Tac Toe.
    
    This class provides different AI strategies for playing Quantum Tic Tac Toe.
    """
    
    def __init__(self, difficulty: str = "medium"):
        """
        Initialize an AI player.
        
        Args:
            difficulty: Difficulty level ('easy', 'medium', or 'hard')
        """
        self.difficulty = difficulty
    
    def make_move(self, game: QuantumTicTacToe) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        """
        Make a move in the game.
        
        Args:
            game: The current game state
            
        Returns:
            A pair of positions representing the AI's move
        """
        if self.difficulty == "easy":
            return self._make_random_move(game)
        elif self.difficulty == "medium":
            return self._make_medium_move(game)
        else:  # hard
            return self._make_strategic_move(game)
    
    def _make_random_move(self, game: QuantumTicTacToe) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        """
        Make a random valid move.
        
        Args:
            game: The current game state
            
        Returns:
            A pair of positions representing the AI's move
        """
        valid_moves = game.get_valid_moves()
        if not valid_moves:
            raise ValueError("No valid moves available")
        
        return random.choice(valid_moves)
    
    def _make_medium_move(self, game: QuantumTicTacToe) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        """
        Make a move with some strategy, but not optimal.
        
        This AI will:
        1. Try to create interference with opponent's uncollapsed moves
        2. Otherwise, make a random move
        
        Args:
            game: The current game state
            
        Returns:
            A pair of positions representing the AI's move
        """
        # Get all valid moves
        valid_moves = game.get_valid_moves()
        if not valid_moves:
            raise ValueError("No valid moves available")
        
        # Get opponent's uncollapsed moves
        opponent_moves = [move for move in game.get_uncollapsed_moves() 
                         if move.player != game.get_current_player()]
        
        # Try to create interference with opponent's moves
        if opponent_moves:
            # Get positions from opponent's uncollapsed moves
            opponent_positions = set()
            for move in opponent_moves:
                opponent_positions.update(move.positions)
            
            # Find moves that interfere with opponent's positions
            interfering_moves = []
            for move in valid_moves:
                pos1, pos2 = move
                if pos1 in opponent_positions or pos2 in opponent_positions:
                    interfering_moves.append(move)
            
            # If we found interfering moves, choose one randomly
            if interfering_moves:
                return random.choice(interfering_moves)
        
        # If no interfering moves, make a random move
        return random.choice(valid_moves)
    
    def _make_strategic_move(self, game: QuantumTicTacToe) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        """
        Make a strategic move.
        
        This AI will:
        1. Try to win if possible
        2. Try to block opponent from winning
        3. Try to create interference with opponent's uncollapsed moves
        4. Try to set up potential winning moves
        5. Otherwise, make a random move
        
        Args:
            game: The current game state
            
        Returns:
            A pair of positions representing the AI's move
        """
        # Get all valid moves
        valid_moves = game.get_valid_moves()
        if not valid_moves:
            raise ValueError("No valid moves available")
        
        # Get the classical board
        board = game.get_classical_board()
        size = game.get_board_size()
        player = game.get_current_player()
        opponent = 'O' if player == 'X' else 'X'
        
        # Check for winning moves
        for pos1, pos2 in valid_moves:
            # Try both positions to see if either leads to a win
            for pos in [pos1, pos2]:
                row, col = pos
                
                # Check if this position would complete a row
                row_count = sum(1 for c in range(size) if board[row][c] == player or (c == col))
                if row_count == size:
                    return (pos1, pos2)
                
                # Check if this position would complete a column
                col_count = sum(1 for r in range(size) if board[r][col] == player or (r == row))
                if col_count == size:
                    return (pos1, pos2)
                
                # Check if this position would complete a diagonal
                if row == col:  # Main diagonal
                    diag_count = sum(1 for i in range(size) if board[i][i] == player or (i == row and i == col))
                    if diag_count == size:
                        return (pos1, pos2)
                
                if row + col == size - 1:  # Anti-diagonal
                    anti_diag_count = sum(1 for i in range(size) if board[i][size-1-i] == player or (i == row and size-1-i == col))
                    if anti_diag_count == size:
                        return (pos1, pos2)
        
        # Check for blocking moves (same logic, but for opponent)
        for pos1, pos2 in valid_moves:
            for pos in [pos1, pos2]:
                row, col = pos
                
                # Check if this position would block a row
                row_count = sum(1 for c in range(size) if board[row][c] == opponent or (c == col))
                if row_count == size:
                    return (pos1, pos2)
                
                # Check if this position would block a column
                col_count = sum(1 for r in range(size) if board[r][col] == opponent or (r == row))
                if col_count == size:
                    return (pos1, pos2)
                
                # Check if this position would block a diagonal
                if row == col:  # Main diagonal
                    diag_count = sum(1 for i in range(size) if board[i][i] == opponent or (i == row and i == col))
                    if diag_count == size:
                        return (pos1, pos2)
                
                if row + col == size - 1:  # Anti-diagonal
                    anti_diag_count = sum(1 for i in range(size) if board[i][size-1-i] == opponent or (i == row and size-1-i == col))
                    if anti_diag_count == size:
                        return (pos1, pos2)
        
        # Get opponent's uncollapsed moves
        opponent_moves = [move for move in game.get_uncollapsed_moves() 
                         if move.player != player]
        
        # Try to create interference with opponent's moves
        if opponent_moves:
            # Get positions from opponent's uncollapsed moves
            opponent_positions = set()
            for move in opponent_moves:
                opponent_positions.update(move.positions)
            
            # Find moves that interfere with opponent's positions
            interfering_moves = []
            for move in valid_moves:
                pos1, pos2 = move
                if pos1 in opponent_positions or pos2 in opponent_positions:
                    interfering_moves.append(move)
            
            # If we found interfering moves, choose one randomly
            if interfering_moves:
                return random.choice(interfering_moves)
        
        # Try to set up potential winning moves
        strategic_moves = []
        for pos1, pos2 in valid_moves:
            # Prioritize moves that include center position
            center = size // 2
            if (center, center) in [pos1, pos2]:
                strategic_moves.append((pos1, pos2))
                continue
            
            # Prioritize moves that include corner positions
            corners = [(0, 0), (0, size-1), (size-1, 0), (size-1, size-1)]
            if pos1 in corners or pos2 in corners:
                strategic_moves.append((pos1, pos2))
                continue
        
        # If we found strategic moves, choose one randomly
        if strategic_moves:
            return random.choice(strategic_moves)
        
        # If no strategic moves, make a random move
        return random.choice(valid_moves)
    
    def decide_collapse(self, game: QuantumTicTacToe) -> Tuple[int, Tuple[int, int]]:
        """
        Decide which move to collapse and to which position.
        
        Args:
            game: The current game state
            
        Returns:
            Tuple of (move_index, position) representing the collapse decision
        """
        # Get uncollapsed moves
        uncollapsed_moves = game.get_uncollapsed_moves()
        if not uncollapsed_moves:
            raise ValueError("No uncollapsed moves available")
        
        # For easy difficulty, make a random choice
        if self.difficulty == "easy":
            move = random.choice(uncollapsed_moves)
            move_index = game.board.moves.index(move)
            position = random.choice(move.positions)
            return (move_index, position)
        
        # For medium and hard difficulties, be more strategic
        player = game.get_current_player()
        
        # Prioritize collapsing opponent's moves
        opponent_moves = [move for move in uncollapsed_moves if move.player != player]
        if opponent_moves:
            move = random.choice(opponent_moves)
            move_index = game.board.moves.index(move)
            
            # Try to collapse in a way that blocks the opponent
            board = game.get_classical_board()
            size = game.get_board_size()
            
            for pos in move.positions:
                row, col = pos
                
                # Check if collapsing here would block a win
                # (Similar logic to _make_strategic_move, but for blocking)
                
                # For hard difficulty, do a more thorough analysis
                if self.difficulty == "hard":
                    # TODO: Implement more sophisticated collapse strategy
                    pass
            
            # If no strategic collapse found, choose randomly
            position = random.choice(move.positions)
            return (move_index, position)
        
        # If no opponent moves, collapse own moves strategically
        move = random.choice(uncollapsed_moves)
        move_index = game.board.moves.index(move)
        
        # For hard difficulty, try to collapse to create winning opportunities
        if self.difficulty == "hard":
            # TODO: Implement more sophisticated collapse strategy
            pass
        
        # If no strategic collapse found, choose randomly
        position = random.choice(move.positions)
        return (move_index, position)