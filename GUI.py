import numpy as np
import random
import pygame
import sys
import os
import math
from engine import *
from collections import deque

score = [0, 0]  # Score for red and yellow players

# Colors
BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
LIGHT_GRAY = (200, 200, 200)
GRAY = (128, 128, 128)

ROW_COUNT = 6
COLUMN_COUNT = 7

PLAYER = 0
AI = 1

EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = 2

WINDOW_LENGTH = 4

SQUARESIZE = 100
MINI_SQUARESIZE = 17
MINI_RADIUS = int(MINI_SQUARESIZE/2)

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE
width_mini = COLUMN_COUNT * MINI_SQUARESIZE
height_mini = (ROW_COUNT+1) * MINI_SQUARESIZE
# height = (ROW_COUNT * SQUARESIZE) + SQUARESIZE * 2
size = (width, height)
screen = pygame.display.set_mode(size)
RADIUS = int(SQUARESIZE/2 - 5)

WIDTH_window = 1050
HEIGHT_window = 700
WINDOW_SIZE = (WIDTH_window, HEIGHT_window)
ROOT_VALUE=0
ELAPSED_TIME=0

def Expanded_nodes(root):
    count=0
    queue=deque([root])
    while queue:
        node= queue.popleft()
        count+=1
        if node.children:
            queue.extend(node.children)
    return count-1

def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):		
            if board[r][c] == PLAYER_PIECE:
                pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
            elif board[r][c] == AI_PIECE: 
                pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)

    draw_button()
    display_score()
    pygame.display.update()
     
     
    
def draw_button():
    # Draw the button rectangle
    pygame.draw.rect(screen, YELLOW, (0, height + SQUARESIZE//2, width//2, SQUARESIZE))
    # Draw the button text
    font = pygame.font.Font(None, 36)
    text = font.render("Click Me", True, WHITE)
    text_rect = text.get_rect(center=(width/2, height+SQUARESIZE/2))
    screen.blit(text, text_rect)

def display_score():
    # Draw the score text
    font = pygame.font.Font(None, 36)
    text = font.render("Score: 0", True, WHITE)  # Replace 0 with actual score value
    text_rect = text.get_rect(midtop=(width/2, height+SQUARESIZE-10))
    screen.blit(text, text_rect)






# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH = 600
HEIGHT = 400



# Font
FONT = pygame.font.SysFont(None, 30)

# Function to display text on the screen
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)

# Function to display menu
def display_menu(screen, algorithm, difficulty):
    # Draw Background Image
    background_image = pygame.image.load("background.jpg")  
    screen.blit(background_image, (0, -30))  # Blit the image onto the screen at the specified position
    #draw_text("Connect 4 Game", FONT, BLACK, screen, 200, 50)
    draw_text("Algorithm:", FONT, RED, screen, 20, 530)
    draw_text(algorithm, FONT, RED, screen, 130, 530)
    draw_text("Difficulty:", FONT, RED, screen, 20, 580)
    draw_text(str(difficulty), FONT, RED, screen, 130, 580)
    draw_text("Press Enter To Start", FONT, YELLOW, screen, 430, 640)

def game_sidebar(screen):
    draw_text("Your Score: ", FONT, WHITE, screen, 730, 300)
    draw_text("Ai Score: ", FONT, WHITE, screen, 730, 250)


def updateScorePlayer(screen, scoreplayer):
    draw_text(str(scoreplayer), FONT, WHITE, screen, 970, 300)
    #pygame.display.update()

def updateScoreAi(screen, scoreAi):
    draw_text(str(scoreAi), FONT, WHITE, screen, 970, 250)
    #pygame.display.update()

# Visualize tree Functions

def draw_miniboard(node,x_shift,y_shift):
    board=node.board
    board_boundaries = pygame.Rect(0, 0, 0, 0)  # Initialize boundaries
    value=node.utility_value
    draw_text(str("{:.2f}".format(value)), FONT, WHITE, screen, x_shift, y_shift)
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            rect = pygame.Rect(c * MINI_SQUARESIZE + x_shift, r * MINI_SQUARESIZE + MINI_SQUARESIZE + y_shift, MINI_SQUARESIZE, MINI_SQUARESIZE)
            pygame.draw.rect(screen, BLUE, rect)
            board_boundaries.union_ip(rect)  # Update boundaries

            circle_center = (int(c * MINI_SQUARESIZE + MINI_SQUARESIZE / 2 + x_shift), int(r * MINI_SQUARESIZE + MINI_SQUARESIZE + MINI_SQUARESIZE / 2 + y_shift))
            pygame.draw.circle(screen, BLACK, circle_center, MINI_RADIUS)

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):        
            if board[r][c] == PLAYER_PIECE:
                circle_center = (int(c * MINI_SQUARESIZE + MINI_SQUARESIZE / 2 + x_shift), height_mini - int(r * MINI_SQUARESIZE + MINI_SQUARESIZE / 2) + y_shift)
                pygame.draw.circle(screen, RED, circle_center, MINI_RADIUS)
                board_boundaries.union_ip(pygame.Rect(circle_center[0] - MINI_RADIUS, circle_center[1] - MINI_RADIUS, 2 * MINI_RADIUS, 2 * MINI_RADIUS))  # Update boundaries
            elif board[r][c] == AI_PIECE: 
                circle_center = (int(c * MINI_SQUARESIZE + MINI_SQUARESIZE / 2 + x_shift), height_mini - int(r * MINI_SQUARESIZE + MINI_SQUARESIZE / 2) + y_shift)
                pygame.draw.circle(screen, YELLOW, circle_center, MINI_RADIUS)
                board_boundaries.union_ip(pygame.Rect(circle_center[0] - MINI_RADIUS, circle_center[1] - MINI_RADIUS, 2 * MINI_RADIUS, 2 * MINI_RADIUS))  # Update boundaries

    draw_button()
    display_score()
    pygame.display.update()

    return board_boundaries  # Return the boundaries of the drawn board


def DrawChildren(root):
    board_boundaries=[]
    root_center=(510, 285)
    x=40
    y=470
    root_boundary= draw_miniboard(root,450,165) 

    for child in root.children:
        boundary= draw_miniboard(child,x,y)
        pygame.draw.line(screen, YELLOW, root_center, (boundary.width-65,485))
        x+=140
        #print(boundary)
        board_boundaries.append(boundary)
        
    pygame.display.flip()
    return board_boundaries



def Draw_returnButton():
    return_button_rect = pygame.Rect(850, 100, 150, 40)
    return_button_color = YELLOW
    return_button_text = pygame.font.Font(None, 24).render("Return to Game", True, (255, 255, 255))
    pygame.draw.rect(screen, return_button_color, return_button_rect)
    screen.blit(return_button_text, (return_button_rect.x + 10, return_button_rect.y + 10))
    return return_button_rect

def Draw_backButton():
    back_button_rect = pygame.Rect(850, 200, 150, 40)
    back_button_color = RED
    back_button_text = pygame.font.Font(None, 22).render("Back To Parent", True, (255, 255, 255))
    pygame.draw.rect(screen, back_button_color, back_button_rect)
    screen.blit(back_button_text, (back_button_rect.x + 10, back_button_rect.y + 10))
    return back_button_rect

def draw_metrics(expanded_count):
    draw_text(str(f"Expanded Nodes: {expanded_count}"), FONT, WHITE, screen, 20, 130)
    draw_text(str(f"Elapsed Time: {ELAPSED_TIME}"), FONT, WHITE, screen, 20, 155)


def VisualizeTree(root):
    screen.fill(BLACK)
    return_button_rect=Draw_returnButton()
    x=40
    expanded_count = Expanded_nodes(root)
    draw_metrics(expanded_count)
    pygame.display.flip()
    #root_boundary= DrawRoot(root)
    boundaries=DrawChildren(root)
    back_stack=[]
    back_index=0
    back_button_rect=Draw_backButton()
    parent_stack=[]
    parent_stack.append(root)
    playing = False

    while not playing:
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button_rect.collidepoint(event.pos):
                    # print(root.parent)
                    if len(parent_stack)!=0: 
                        # print("sui3")
                        screen.fill(BLACK)
                        draw_metrics(expanded_count)
                        Draw_returnButton()
                        Draw_backButton()
                        root=parent_stack.pop()
                        DrawChildren(root)
                    
                
                        
                elif return_button_rect.collidepoint(event.pos):
                    screen.fill(BLACK)
                    # print("suii")
                    playing=True
                    return
                
                elif boundaries[0].collidepoint(event.pos) and root.children:
                    # print("sui1")
                    screen.fill(BLACK)
                    draw_metrics(expanded_count)
                    Draw_returnButton()
                    Draw_backButton()
                    DrawChildren(root.children[0])
                    parent_stack.append(root)
                    root=root.children[0]
                
                elif boundaries[1].collidepoint(event.pos) and root.children:
                    screen.fill(BLACK)
                    draw_metrics(expanded_count)
                    Draw_returnButton()
                    Draw_backButton()
                    DrawChildren(root.children[1])
                    parent_stack.append(root)
                    root=root.children[1]
                
                elif boundaries[2].collidepoint(event.pos) and root.children:
                    screen.fill(BLACK)
                    draw_metrics(expanded_count)
                    Draw_returnButton()
                    Draw_backButton()
                    DrawChildren(root.children[2])
                    parent_stack.append(root)
                    root=root.children[2]
                
                elif boundaries[3].collidepoint(event.pos) and root.children:
                    screen.fill(BLACK)
                    draw_metrics(expanded_count)
                    Draw_returnButton()
                    Draw_backButton()
                    DrawChildren(root.children[3])
                    parent_stack.append(root)
                    root=root.children[3]
                
                elif boundaries[4].collidepoint(event.pos) and root.children:
                    screen.fill(BLACK)
                    draw_metrics(expanded_count)
                    Draw_returnButton()
                    Draw_backButton()
                    DrawChildren(root.children[4])
                    parent_stack.append(root)
                    root=root.children[4]
                
                elif boundaries[5].collidepoint(event.pos) and root.children:
                    screen.fill(BLACK)
                    draw_metrics(expanded_count)
                    Draw_returnButton()
                    Draw_backButton()
                    DrawChildren(root.children[5])
                    parent_stack.append(root)
                    root=root.children[5]
                
                elif boundaries[6].collidepoint(event.pos) and root.children:
                    screen.fill(BLACK)
                    draw_metrics(expanded_count)
                    Draw_returnButton()
                    Draw_backButton()
                    DrawChildren(root.children[6])
                    parent_stack.append(root)
                    root=root.children[6]

def Draw_Result(result):
    Result_rect = pygame.Rect(750, 400, 250, 200)
    Result_rect_color = RED
    Result_rect_text = pygame.font.Font(None, 24).render(str(result), True, (255, 255, 255))
    pygame.draw.rect(screen, Result_rect_color, Result_rect)
    screen.blit(Result_rect_text, (Result_rect.x + 10, Result_rect.y + 90))
    return Result_rect
# Main function
def main():
    Score_pos_ai= pygame.Rect(970, 250, 100, 100)
    Score_pos_player= pygame.Rect(970, 300, 100, 100)
    screen = pygame.display.set_mode((WIDTH_window, HEIGHT_window))
    pygame.display.set_caption("Connect 4")
    solve_tree_button_rect = pygame.Rect(800, 150, 150, 50)
    solve_tree_button_color = (0, 255, 0)
    solve_tree_button_text = pygame.font.Font(None, 36).render("Solve Tree", True, (255, 255, 255))
    algorithm = "Minimax without pruning"
    difficulty = 1
    running = True
    options=["Minimax without pruning","Minimax with pruning","ExpectiMinimax"]
    i=1
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    i+=1
                    i=i%3
                    algorithm=options[i]
                if event.key == pygame.K_UP:
                    i-=1
                    i=i%3
                    algorithm=options[i]
                elif event.key == pygame.K_RIGHT:
                    if difficulty < 10:
                        difficulty += 1
                elif event.key == pygame.K_LEFT:
                    if difficulty > 1:
                        difficulty -= 1
                elif event.key == pygame.K_RETURN:
                    running = False

        display_menu(screen, algorithm, difficulty)
        pygame.display.flip()

    # print("Algorithm:", algorithm)
    # print("Difficulty:", difficulty)
    
    board = create_board()
    # print_board(board)
    game_over = False

    pygame.init()
    #screen = pygame.display.set_mode(size)
    screen = pygame.display.set_mode((WIDTH_window, HEIGHT_window))
    game_sidebar(screen)
    updateScorePlayer(screen,score[PLAYER])
    updateScoreAi(screen,score[AI])
    draw_board(board)
    pygame.display.update()
    pygame.draw.rect(screen, solve_tree_button_color, solve_tree_button_rect)
    screen.blit(solve_tree_button_text, (solve_tree_button_rect.x + 10, solve_tree_button_rect.y + 10))

    pygame.display.flip()
    myfont = pygame.font.SysFont("monospace", 75)

    # turn = random.randint(PLAYER, AI)
    turn  = PLAYER
    playing=1
    first_played=0
    while not game_over:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEMOTION and playing==1:
                
                pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
                posx = min(max(event.pos[0], RADIUS), width - RADIUS)  # Limiting posx within a range
                #print(event.pos)
                if turn == PLAYER:
                    pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)

            pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN and playing==1:
                
                screen.fill(BLACK, Score_pos_ai)
                screen.fill(BLACK, Score_pos_player)
                updateScorePlayer(screen,score[PLAYER])
                updateScoreAi(screen,score[AI])
                if solve_tree_button_rect.collidepoint(event.pos) and first_played==1:  # Check if the mouse click is within the button rectangle
                    playing=0
                    VisualizeTree(root)
                    draw_board(board)
                    pygame.draw.rect(screen, solve_tree_button_color, solve_tree_button_rect)
                    screen.blit(solve_tree_button_text, (solve_tree_button_rect.x + 10, solve_tree_button_rect.y + 10))
                    game_sidebar(screen)
                    screen.fill(BLACK, Score_pos_ai)
                    screen.fill(BLACK, Score_pos_player)
                    updateScorePlayer(screen,score[PLAYER])
                    updateScoreAi(screen,score[AI])
                    playing=1
                # print(event.pos)
                # Ask for Player 1 Input
                if turn == PLAYER and event.pos[0] <= 700:
                    posx = min(max(event.pos[0], RADIUS), width - RADIUS)  # Limiting posx within a range
                    col = int(math.floor(posx/SQUARESIZE))

                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, PLAYER_PIECE)
                        x= check_is_winning_move(board, PLAYER_PIECE,col,row)
                        if x:
                            score[PLAYER] += x 
                            # print(score)
                            screen.fill(BLACK, Score_pos_ai)
                            screen.fill(BLACK, Score_pos_player)
                            updateScorePlayer(screen,score[PLAYER])
                            updateScoreAi(screen,score[AI])
                        turn += 1
                        turn = turn % 2
                
                        draw_board(board)
        import time
        # # Ask for Player 2 Input
        if turn == AI and not game_over:		
            
            root = Node(None, [], 0 , board= board)
            # Traversing the children  
            if algorithm == "Minimax without pruning":
                # print(difficulty)
                start=time.time()
                col, ROOT_VALUE   = minimax(board,  difficulty , True , 0 , root, AI_PIECE)
                end=time.time()
                first_played=1
                global ELAPSED_TIME
                ELAPSED_TIME="{:.6f}".format(end-start)
                col = col.column
            elif algorithm == "Minimax with pruning":
                #modify later -------------------------------------------
                start=time.time()
                col, ROOT_VALUE  = minimax_with_pruning(board,  difficulty , -math.inf , math.inf , True , 0 , root , piece=  AI_PIECE)
                end=time.time()
                first_played=1
                ELAPSED_TIME="{:.6f}".format(end-start)
                col=col.column
            else:
                start=time.time()
                col, ROOT_VALUE   = expect_minimax(board , difficulty, True , 0  , root , piece = AI_PIECE)
                end=time.time()
                first_played=1
                ELAPSED_TIME="{:.6f}".format(end-start)
            

            #print(root.board) 
            root.utility_value=ROOT_VALUE

            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, AI_PIECE)
                z=check_is_winning_move(board, AI_PIECE,col,row)
                if z:
                    score[AI] +=z 
                    screen.fill(BLACK, Score_pos_ai)
                    screen.fill(BLACK, Score_pos_player)
                    updateScorePlayer(screen,score[PLAYER])
                    updateScoreAi(screen,score[AI])
                    # print(score)

                draw_board(board)

                turn += 1
                turn = turn % 2

        if is_terminal_node(board):
            #print(score)
            screen.fill(BLACK, Score_pos_ai)
            screen.fill(BLACK, Score_pos_player)
            updateScorePlayer(screen,score[PLAYER])
            updateScoreAi(screen,score[AI])
            playing=0
            #game_over=True
            if score[AI]>score[PLAYER]:
                text=f"AI Wins With Score: {score[AI]}"
                Draw_Result(text)
            elif score[AI]<score[PLAYER]:
                text=f"PLAYER Wins With Score: {score[PLAYER]}"
                Draw_Result(text)
            else:
                text=f"DRAW"
                Draw_Result(text)
            
            #pygame.time.wait(3000) # This line is added after the 2 last print functions


if __name__ == "__main__":
    main()

