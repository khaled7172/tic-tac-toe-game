import turtle
import time
import pygame  # Import pygame for sound
import random  # For AI move selection

# Initialize pygame mixer for sound
pygame.mixer.init()

# Load sound files
click_sound = pygame.mixer.Sound("click_sound.wav")  # Make sure you have a click_sound.wav file
win_sound = pygame.mixer.Sound("win_sound.wav")  # Make sure you have a win_sound.wav file

# Screen setup
screen = turtle.Screen()
screen.title("Tic Tac Toe")
screen.setup(width=600, height=600)
screen.tracer(0)

turtle.speed(0)
turtle.hideturtle()

# Game variables
board = [["" for _ in range(3)] for _ in range(3)]
player = "X"  # Default starting player
cell_size = 120  
symbol_size = 40  
game_over = False  
line_extension = 30  

# Score variables
score_x = 0
score_o = 0

# Variable to track who starts
starting_player = "O"  # "X" starts the first game

def draw_board():
    """Draws the Tic Tac Toe board with thick lines."""
    turtle.clear()
    turtle.pensize(5)
    offset = cell_size // 2
    for i in [-offset, offset]:
        turtle.penup()
        turtle.goto(i, cell_size * 1.5)
        turtle.pendown()
        turtle.goto(i, -cell_size * 1.5)
    for i in [-offset, offset]:
        turtle.penup()
        turtle.goto(-cell_size * 1.5, i)
        turtle.pendown()
        turtle.goto(cell_size * 1.5, i)
    
    draw_scores()  # Draw the current scores
    draw_reset_button()
    screen.update()
    turtle.hideturtle()

def draw_x(x, y):
    """Draws a red X."""
    turtle.pensize(5)
    turtle.color("red")
    turtle.penup()
    turtle.goto(x - symbol_size, y - symbol_size)
    turtle.pendown()
    turtle.goto(x + symbol_size, y + symbol_size)
    turtle.penup()
    turtle.goto(x + symbol_size, y - symbol_size)
    turtle.pendown()
    turtle.goto(x - symbol_size, y + symbol_size)
    turtle.color("black")  
    screen.update()
    turtle.hideturtle()

def draw_o(x, y):
    """Draws a blue O."""
    turtle.pensize(5)
    turtle.color("blue")
    turtle.penup()
    turtle.goto(x, y - symbol_size)
    turtle.pendown()
    turtle.circle(symbol_size)
    turtle.color("black")  
    screen.update()
    turtle.hideturtle()

def get_cell(x, y):
    """Gets the row and column index from the click coordinates."""
    row = int(2 - (y + cell_size * 1.5) // cell_size)
    col = int((x + cell_size * 1.5) // cell_size)
    return row, col

def check_winner():
    """Checks for a winner."""
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != "":
            return board[i][0], [(i, 0), (i, 1), (i, 2)]  
        if board[0][i] == board[1][i] == board[2][i] != "":
            return board[0][i], [(0, i), (1, i), (2, i)]  

    if board[0][0] == board[1][1] == board[2][2] != "":
        return board[0][0], [(0, 0), (1, 1), (2, 2)]
    if board[0][2] == board[1][1] == board[2][0] != "":
        return board[0][2], [(0, 2), (1, 1), (2, 0)]

    return None, []  

def draw_winning_line(sequence, winner):
    """Draws a winning line with the color of the winner."""
    turtle.pensize(7)
    turtle.color("red" if winner == "X" else "blue")  # Winner's color

    row1, col1 = sequence[0]
    row2, col2 = sequence[2]

    x1, y1 = -cell_size + col1 * cell_size, cell_size - row1 * cell_size
    x2, y2 = -cell_size + col2 * cell_size, cell_size - row2 * cell_size

    if row1 == row2:  
        x1 -= line_extension
        x2 += line_extension
    elif col1 == col2:  
        y1 += line_extension
        y2 -= line_extension
    else:  
        if row1 == 0 and col1 == 0:  
            x1 -= line_extension
            y1 += line_extension
            x2 += line_extension
            y2 -= line_extension
        else:  
            x1 += line_extension
            y1 += line_extension
            x2 -= line_extension
            y2 -= line_extension

    turtle.penup()
    turtle.goto(x1, y1)
    turtle.pendown()
    turtle.goto(x2, y2)
    turtle.penup()

    turtle.color("black")
    screen.update()
    turtle.hideturtle()

def display_winner(winner):
    """Displays the winner and resets after 2 seconds."""
    global score_x, score_o

    if winner == "X":
        score_x += 1
    elif winner == "O":
        score_o += 1

    turtle.penup()
    turtle.goto(-50, 220)
    turtle.color("red" if winner == "X" else "blue")
    turtle.write(f"{winner} Wins!", font=("Arial", 16, "bold"))
    turtle.color("black")
    turtle.hideturtle()
    screen.update()

    # Play win sound
    win_sound.play()

    # Alternate the starting player for the next game after a win

    screen.ontimer(reset_game, 2000)

def click_handler(x, y):
    """Handles clicks and game logic."""
    global player, game_over
    if game_over:
        return

    if -40 <= x <= 40 and -250 <= y <= -220:  
        reset_game()
        return

    row, col = get_cell(x, y)
    if 0 <= row < 3 and 0 <= col < 3 and board[row][col] == "":
        board[row][col] = player
        draw_x(-cell_size + col * cell_size, cell_size - row * cell_size) if player == "X" else draw_o(-cell_size + col * cell_size, cell_size - row * cell_size)

        winner, sequence = check_winner()
        if winner:
            draw_winning_line(sequence, winner)
            display_winner(winner)
            game_over = True
            return

        # Switch to AI's turn
        player = "O" if player == "X" else "X"

        # Play click sound when a move is made
        click_sound.play()

        # Trigger AI move if it's AI's turn
        if player == "O":  # Assuming AI is always "O"
            ai_move()

def draw_reset_button():
    """Draws the Clear button with more space below the board."""
    turtle.penup()
    turtle.goto(-40, -215)  
    turtle.pendown()    
    turtle.color("black")  # Set color to black for the border
    turtle.goto(40, -215)
    turtle.goto(40, -250)  
    turtle.goto(-40, -250)
    turtle.goto(-40, -215)
    turtle.penup()
    turtle.goto(-20, -243)  
    turtle.color("black")  # Set color to red for player X
    turtle.write("Clear", font=("Arial", 12, "bold"))
    turtle.hideturtle()

def draw_scores():
    """Draws the current scores of X and O players and underlines the current player's score."""
    turtle.penup()
    turtle.goto(-200, 250)
    turtle.color("red")  # Set color to red for player X

    # Write X's score
    turtle.write(f"X: {score_x}", font=("Arial", 16, "bold"), align="center")
    
    # Underline X's score if it's X's turn
    if player == "X":
        turtle.goto(-200 - len(f"X: {score_x}") * 4, 245)  # Adjust to the left of X's score
        turtle.pendown()
        turtle.goto(-200 + len(f"X: {score_x}") * 4, 245)  # Draw line under X's score
        turtle.penup()

    turtle.goto(100, 250)
    turtle.color("blue")  # Set color to blue for player O

    # Write O's score
    turtle.write(f"O: {score_o}", font=("Arial", 16, "bold"), align="center")
    
    # Underline O's score if it's O's turn
    if player == "O":
        turtle.goto(100 - len(f"O: {score_o}") * 4, 245)  # Adjust to the left of O's score
        turtle.pendown()
        turtle.goto(100 + len(f"O: {score_o}") * 4, 245)  # Draw line under O's score
        turtle.penup()

    turtle.hideturtle()

def reset_game():
    """Clears the board and resets everything, alternating the starting player."""
    global board, player, game_over, starting_player
    board = [["" for _ in range(3)] for _ in range(3)]
    player = starting_player  # Set the current player to the starting player
    game_over = False

    # Alternate the starting player for the next game
    starting_player = "O" if starting_player == "X" else "X"

    draw_board()

def minimax(board, depth, is_maximizing):
    """Minimax algorithm to calculate the best move for the AI."""
    winner, _ = check_winner()
    if winner == "O":  # AI wins
        return 10 - depth
    elif winner == "X":  # Player wins
        return depth - 10
    elif all(board[row][col] != "" for row in range(3) for col in range(3)):  # Tie
        return 0

    if is_maximizing:
        best_score = -float("inf")
        for row in range(3):
            for col in range(3):
                if board[row][col] == "":
                    board[row][col] = "O"
                    score = minimax(board, depth + 1, False)
                    board[row][col] = ""
                    best_score = max(best_score, score)
        return best_score
    else:
        best_score = float("inf")
        for row in range(3):
            for col in range(3):
                if board[row][col] == "":
                    board[row][col] = "X"
                    score = minimax(board, depth + 1, True)
                    board[row][col] = ""
                    best_score = min(best_score, score)
        return best_score

def ai_move():
    """Calculates and makes the AI's move using the minimax algorithm."""
    global player, game_over

    if game_over:
        return

    best_score = -float("inf")
    best_move = None

    for row in range(3):
        for col in range(3):
            if board[row][col] == "":
                board[row][col] = "O"
                score = minimax(board, 0, False)
                board[row][col] = ""
                if score > best_score:
                    best_score = score
                    best_move = (row, col)

    if best_move:
        row, col = best_move
        board[row][col] = "O"
        draw_o(-cell_size + col * cell_size, cell_size - row * cell_size)

        # Check if AI wins
        winner, sequence = check_winner()
        if winner:
            draw_winning_line(sequence, winner)
            display_winner(winner)
            game_over = True
            return

        # Switch back to the human player
        player = "X"

draw_board()
screen.onclick(click_handler)
screen.listen()
screen.mainloop()

