from zona_yoshi import (
    get_knight_moves,
    apply_move,
    evaluate_board,
    GREEN,
    RED,
    YOSHI_GREEN,
    YOSHI_RED,
    is_terminal,
    in_bounds,
    SPECIAL_ZONES
)
import numpy as np

def minimax(board, green_pos, red_pos, depth, is_maximizing, alpha, beta, max_depth):
    # Verificar que los Yoshis existen en el tablero actual
    green_positions = np.argwhere(board == YOSHI_GREEN)
    red_positions = np.argwhere(board == YOSHI_RED)
    
    if green_positions.size == 0 or red_positions.size == 0:
        return evaluate_board(board), None
    
    # Actualizar posiciones por si cambiaron
    current_green_pos = tuple(green_positions[0])
    current_red_pos = tuple(red_positions[0])
    
    if depth == max_depth or is_terminal(board):
        return evaluate_board(board), None

    if is_maximizing:  # Turno del Yoshi verde
        best_value = float('-inf')
        best_move = None
        possible_moves = get_knight_moves(board, current_green_pos)
        
        if not possible_moves:
            return evaluate_board(board), None
            
        for move in possible_moves:
            new_board, new_green_pos = apply_move(board, current_green_pos, move, GREEN)
            
            # Verificar que el Yoshi verde sigue en el tablero
            if np.sum(new_board == YOSHI_GREEN) == 0:
                continue
                
            value, _ = minimax(new_board, new_green_pos, current_red_pos, depth+1, False, alpha, beta, max_depth)
            
            if value > best_value:
                best_value = value
                best_move = move
            alpha = max(alpha, best_value)
            if beta <= alpha:
                break
                
        return best_value, best_move if best_move is not None else (evaluate_board(board), None)
    else:  # Turno del Yoshi rojo
        best_value = float('inf')
        best_move = None
        possible_moves = get_knight_moves(board, current_red_pos)
        
        if not possible_moves:
            return evaluate_board(board), None
            
        for move in possible_moves:
            new_board, new_red_pos = apply_move(board, current_red_pos, move, RED)
            
            # Verificar que el Yoshi rojo sigue en el tablero
            if np.sum(new_board == YOSHI_RED) == 0:
                continue
                
            value, _ = minimax(new_board, current_green_pos, new_red_pos, depth+1, True, alpha, beta, max_depth)
            
            if value < best_value:
                best_value = value
                best_move = move
            beta = min(beta, best_value)
            if beta <= alpha:
                break
                
        return best_value, best_move if best_move is not None else (evaluate_board(board), None)