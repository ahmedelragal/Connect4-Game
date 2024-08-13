######################################################################################################################################################
# Importing needed libraries
import numpy as np
import pygame
import sys
import math
import random
######################################################################################################################################################
# Defining important variables
score = [0, 0]  
BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)
ROW_COUNT = 6
COLUMN_COUNT = 7
PLAYER = 0
AI = 1
EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = 2
WINDOW_LENGTH = 4
EXPANDED_NODES=0
######################################################################################################################################################
# Defining important functions for Board 
def create_board():
	board = np.zeros((ROW_COUNT,COLUMN_COUNT))
	return board

def drop_piece(board, row, col, piece):
	board[row][col] = piece

def is_valid_location(board, col):
	return board[ROW_COUNT-1][col] == 0

def get_next_open_row(board, col):
	for r in range(ROW_COUNT):
		if board[r][col] == 0:
			return r

def print_board(board):
	print(np.flip(board, 0))


def get_valid_locations(board):
	valid_locations = []
	for col in range(COLUMN_COUNT):
		if is_valid_location(board, col):
			valid_locations.append(col)
	# print(f"valid locations are {valid_locations}")
	return valid_locations


# Important functions for Minimax Implementation 
winning_moves  = set()
def check_is_winning_move(board , piece, col, row):
        count = 0
        def check_direction(dc, dr):
            nonlocal count
            for c in range(COLUMN_COUNT - 3):
                for r in range(ROW_COUNT - 3) if dr != -1 else range(3, ROW_COUNT):
                    if all(
                        board[r + i * dr][c + i * dc] == piece for i in range(4)
                    ):
                        count += (
                            1
                            if any(
                                c + i * dc == col and r + i * dr == row
                                for i in range(4)
                            )
                            else 0
                        )
 
        # Check horizontal
        for c in range(COLUMN_COUNT - 3): # msh mhtag a5r 3 col fl horizontal
            for r in range(ROW_COUNT):
                if all(board[r][c + i] == piece for i in range(4)):  # if all statisfy condition
                    # if all (5asa bel for loop l gwa) lazm kol el i's statisfy condition
                    count += ( # ana l3bt f col w row f bcheck en l 4 piece dol , el col w row mnhom
                        1 if any(c + i == col and r == row for i in range(4)) else 0
                    )
 
        # Check vertical
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT - 3):
                if all(board[r + i][c] == piece for i in range(4)):
                    count += (
                        1 if any(c == col and r + i == row for i in range(4)) else 0
                    )
 
        # Check positive slope diagonal
        check_direction(1, 1)
 
        # Check negative slope diagonal
        check_direction(1, -1)
 
        return count

# def evaluate_window(window, piece):
# 	score = 0	
# 	opp_piece = PLAYER_PIECE
# 	if piece == PLAYER_PIECE:
# 		opp_piece = AI_PIECE

# 	if window.count(piece) == 4:
# 		# print("100000")
# 		# score += 100000
# 		score +=  4
# 	elif window.count(piece) == 3 and window.count(EMPTY) == 1:
# 		# print("5000")
# 		# score += 5000
# 		score += 3
# 	elif window.count(piece) == 2 and window.count(EMPTY) == 2:
# 		# print("200")
# 		# score += 200
# 		score += 2 
# 	elif window.count(opp_piece) == 3 and window.count(EMPTY) == 1 : 
# 		score += 1 
# 	# elif window.count(piece) == 2  and window.count(EMPTY) > 2:
# 	# 		# print("20")
# 	# 		score += 10  # Encourage building connections
# 	if window.count(opp_piece) == 4 : 
# 		score -= 4
# 	elif window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
# 		# print("-2000")
# 		# score -= 4000
# 		score -= 3
# 	elif window.count(opp_piece) == 2 and window.count(EMPTY) == 2 :
# 		# print("-200")
# 		# score -=  100
# 		score -= 2
# 	# elif window.count(opp_piece) == 2 and window.count(EMPTY) > 2:
# 	# 	# print("-5")
# 	# 	# score -= 5  #
# 	# 	score -= 2
# 	elif window.count(opp_piece) == 3 and window.count(EMPTY) == 1 : 
# 		score -= 1 
# 			# Consider position in the board (center prioritization)
# 	# center_column = window[2] == piece
# 	# if center_column:
# 	# 	# print("15")
# 	# 	score +=  2  # Encourage occupying the center

# 	return score

def evaluate_window(window, piece):
    score = 0
    if piece == 2 :
        opponent_piece=1
    else:
        opponent_piece=2

    opponent_consecutive = window.count(opponent_piece)
    consecutive_pieces = window.count(piece)
    free_slots = window.count(0)
	
    if consecutive_pieces == 4:
        score += 2000 # Win condition
    elif consecutive_pieces == 3 and free_slots == 1:
        score += 6  # Strong winning opportunity
    elif consecutive_pieces == 2 and free_slots == 2:
        score += 1  # Potential winning connection
    elif opponent_consecutive == 3 and free_slots == 1:
        score += 11
    
    if opponent_consecutive == 4:
        score -= 1000  # Win oponent condition
  
    if opponent_consecutive == 2 and free_slots == 2:
        score -= 2

    return score


def score_position(board, piece):
	score = 0
	# print(piece)

	## Score center column
	# center_array = [int(i) for i in list(board[:, COLUMN_COUNT//2])]
	# center_count = center_array.count(piece)
	# score += center_count * 6
	# print("Hello score ")

	## Score Horizontal
	for r in range(ROW_COUNT):
		row_array = [int(i) for i in list(board[r,:])]
		for c in range(COLUMN_COUNT-3):
			
			window = row_array[c:c+WINDOW_LENGTH]
			score += evaluate_window(window, piece)

	## Score Vertical
	for c in range(COLUMN_COUNT):
		col_array = [int(i) for i in list(board[:,c])]
		for r in range(ROW_COUNT-3):
			window = col_array[r:r+WINDOW_LENGTH]
			score += evaluate_window(window, piece)

	## Score posiive sloped diagonal
	for r in range(ROW_COUNT-3):
		for c in range(COLUMN_COUNT-3):
			window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
			score += evaluate_window(window, piece)

	for r in range(ROW_COUNT-3):
		for c in range(COLUMN_COUNT-3):
			window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
			score += evaluate_window(window, piece)

	return score





def is_terminal_node(board):
	return  len(get_valid_locations(board)) == 0

class Node (): 
	def __init__(self ,  column , children , utility_value , board = None , parent  = None):
		self.column  = column 
		self.children  = children  
		self.utility_value  = utility_value
		self.board = board
		self.parent = parent

######################################################################################################################################################
#Minimax 3 Implementations


def minimax_with_pruning(board, depth, alpha, beta, maximizingPlayer, current_depth  , newnode  , piece ):
#   global root 
  valid_locations = get_valid_locations(board)
  is_terminal = is_terminal_node(board)

  if depth == 0 or is_terminal:
  # return Node(None, None, score_position(board, AI_PIECE), board)  # Leaf node
    return None  , score_position(board, piece)
  best_child = None
  if maximizingPlayer:
    value = -math.inf
    children = []
    for col in valid_locations:
      row = get_next_open_row(board, col)
      b_copy = board.copy()
      drop_piece(b_copy, row, col, AI_PIECE)
      node = Node(col, [], 0 , b_copy  )  # Set parent based on current depth

      returned_node , val  = minimax_with_pruning(b_copy, depth - 1, alpha, beta, False, current_depth + 1 , node ,   piece % 2 + 1)
    #   print("1")
      node.utility_value = val
      newnode.children.append(node)
      children.append(node)
      value = max(value, val)
      alpha = max(alpha, value)
      if value == val:  # Update best child if value has improved
        best_child = node
      if alpha >= beta:
        break
  # No need to set root.children here, children are appended within the loop

  else:  # Minimizing player
    value = math.inf
    children = []
    for col in valid_locations:
      row = get_next_open_row(board, col)
      b_copy = board.copy()
      drop_piece(b_copy, row, col, PLAYER_PIECE)
      node = Node(col, [], 0 , b_copy  )  # Set parent based on current depth

      returned_node , val = minimax_with_pruning(b_copy, depth - 1, alpha, beta, True, current_depth + 1 , node , piece % 2 + 1 )
    #   node = Node(col, returned_node.children, returned_node.utility_value, b_copy, parent=root if current_depth == 0 else root.children[current_depth - 1])  # Set parent based on current depth
      children.append(node)
      node.utility_value = val
      newnode.children.append(node)
      value = min(value, val)
      beta = min(beta, value)
      if value == val:  # Update best child if value has improved
        best_child = node
      if alpha >= beta:
        break
  # No need to set root.children here, children are appended within the loop

  return best_child, value 





def minimax(board, depth,  maximizingPlayer, current_depth  , newnode  , piece ):
#   global root 
  valid_locations = get_valid_locations(board)
  is_terminal = is_terminal_node(board)

  if depth == 0 or is_terminal:
  # return Node(None, None, score_position(board, AI_PIECE), board)  # Leaf node
    return None  , score_position(board, piece )
  best_child = None 
  if maximizingPlayer:
    value = -math.inf
    children = []
    for col in valid_locations:
      row = get_next_open_row(board, col)
      b_copy = board.copy()
      drop_piece(b_copy, row, col, AI_PIECE)
      node = Node(col, [], 0 , b_copy  )  # Set parent based on current depth

      returned_node , val  = minimax(b_copy, depth - 1,  False, current_depth + 1 , node ,  piece % 2 + 1 )
    #   print("1")
      node.utility_value = val
    #   print(node.utility_value)
    #   print(node.board)
      newnode.children.append(node)
      children.append(node)
      value = max(value, val)
      if value == val:  # Update best child if value has improved
        best_child = node

  # No need to set root.children here, children are appended within the loop

  else:  # Minimizing player
    value = math.inf
    children = []
    for col in valid_locations:
      row = get_next_open_row(board, col)
      b_copy = board.copy()
      drop_piece(b_copy, row, col, PLAYER_PIECE)
      node = Node(col, [], 0 , b_copy  )  # Set parent based on current depth

      returned_node , val = minimax(b_copy, depth - 1,  True, current_depth + 1 , node  ,  piece % 2 + 1)
    #   node = Node(col, returned_node.children, returned_node.utility_value, b_copy, parent=root if current_depth == 0 else root.children[current_depth - 1])  # Set parent based on current depth
      children.append(node)
      node.utility_value = val
      newnode.children.append(node)
      value = min(value, val)
      if value == val: 
        best_child = node

  return  best_child, value 




def expect_minimax(board, depth,  maximizingPlayer, current_depth  , newnode  , piece ):
	#   global root 
	column_value = {}
	column_value_minimizing ={}

	valid_locations = get_valid_locations(board)
	is_terminal = is_terminal_node(board)

	if depth == 0 or is_terminal:
	# return Node(None, None, score_position(board, AI_PIECE), board)  # Leaf node
		return None  , score_position(board, piece )
	best_child = None 
	if maximizingPlayer:
		value = -math.inf
		children = []
		for col in valid_locations:
			row = get_next_open_row(board, col)
			b_copy = board.copy()
			drop_piece(b_copy, row, col, AI_PIECE)
			node = Node(col, [], 0 , b_copy  )  # Set parent based on current depth

			returned_node , val  = expect_minimax(b_copy, depth - 1,  False, current_depth + 1 , node ,  piece % 2 + 1 ) 
			column_value[col] = val
		#   print("1")
			node.utility_value = val
		#   print(node.utility_value)
		#   print(node.board)
			newnode.children.append(node)
			children.append(node)
			value = max(value, val)
			if value == val:  # Update best child if value has improved
				best_child = node

	# No need to set root.children here, children are appended within the loop
			#  0 1 2 4  -->  10 12 14 16
		max_value =  - math.inf 
		best_col = 0  
		#  column_value.keys() index out of bunds problem
#   1 2 5 6
		l = len(column_value_minimizing)
		i = 0 
		for    (col ,value) in column_value.items() :
      		# i += 1
        #     12356
			if column_value.get(col-1 , 0 )   ==  0 : 
				val = (0.6 * value) + (0.4 * column_value.get(col+1 , 0 ))
				if val > max_value : 
					max_value  = val  
					best_col = col
			elif column_value.get(col + 1 , 0 )   ==  0 : 
				val = (0.6 * value) + (0.4 * column_value.get(col-1 , 0 ))
				if val > max_value : 
					max_value  = val  
					best_col = col
			else : 
				val = (0.6 * value) + (0.2 * column_value.get(col-1 , 0 )  ) + (0.2 * column_value.get(col+1 , 0 ))
				if val > max_value : 
					max_value  = val  
					best_col = col
				
    
	else:  # Minimizing player
		value = math.inf
		children = []
		for col in valid_locations:
			row = get_next_open_row(board, col)
			b_copy = board.copy()
			drop_piece(b_copy, row, col, PLAYER_PIECE)
			node = Node(col, [], 0 , b_copy  )  # Set parent based on current depth

			returned_node , val = expect_minimax(b_copy, depth - 1,  True, current_depth + 1 , node  ,  piece % 2 + 1)
			column_value_minimizing[col] = val

			#   node = Node(col, returned_node.children, returned_node.utility_value, b_copy, parent=root if current_depth == 0 else root.children[current_depth - 1])  # Set parent based on current depth
			children.append(node)
			node.utility_value = val
			newnode.children.append(node)
			value = min(value, val)
			if value == val: 
				best_child = node

		max_value =  math.inf 
		best_col = 0  
		#  column_value.keys() index out of bunds problem
#   1 2 5 6
		l = len(column_value_minimizing)
		i = 0 
		for    (col ,value) in column_value_minimizing.items() :
      		# i += 1
        # 12356
			if column_value_minimizing.get(col-1 , 0 )   ==  0 : 
				val = (0.6 * value) + (0.4 * column_value_minimizing.get(col+1 , 0 ))
				if val < max_value : 
					max_value  = val  
					best_col = col
			elif column_value_minimizing.get(col + 1 , 0 )   ==  0 : 
				val = (0.6 * value) + (0.4 * column_value_minimizing.get(col-1 , 0 ))
				if val < max_value : 
					max_value  = val  
					best_col = col
			else : 
				val = (0.6 * value) + (0.2 * column_value_minimizing.get(col-1 , 0 )  ) + (0.2 * column_value_minimizing.get(col+1 , 0 ))
				if val < max_value : 
					max_value  = val  
					best_col = col
					

	return  best_col, max_value 


