import pygame
import random
import os

# Set up the paths to the sound files
current_directory = os.path.dirname(__file__)
effects_directory = os.path.join(current_directory, 'effects')
win_sound_path = os.path.join(effects_directory, 'win.mp3')
melody_sound_path = os.path.join(effects_directory, 'melody.mp3')
pop_sound_path = os.path.join(effects_directory, 'pop.mp3')
welcome_sound_path = os.path.join(effects_directory, 'welcome.mp3')
error_sound_path = os.path.join(effects_directory, 'error.mp3')


## GENERATING VARIABLES

# playing variables
def generate_playing_variables():
    player1_score = 0
    player2_score = 0
    player1_break_cards = 0
    player2_break_cards = 0

    chance_turn = random.randint(1,2)
    player1_turn = True if chance_turn == 1 else False
    warning_message = ""
    winning_message = ""
    extra_turn = False

    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    GRAY = (128, 128, 128)
    GREEN = (0, 128, 0)
    WHITE = (255, 255, 255)

    return player1_score, player2_score, player1_break_cards, player2_break_cards, chance_turn, player1_turn, warning_message, winning_message, BLACK, RED, BLUE, GRAY, GREEN, WHITE, extra_turn

# generating pyGame window
def generate_window():
    grid_size = 10
    cell_size = 35
    window_size = (grid_size * cell_size, grid_size * cell_size + 210)  # defines width then height of window, Increased height for the scores
    window = pygame.display.set_mode(window_size)
    pygame.display.set_caption("Chaser Game")

    return grid_size, cell_size, window_size, window

# Create the grid
def generate_grid(grid_size):
    grid = [[random.randint(1, 10) for _ in range(grid_size)] for _ in range(grid_size)] # generating random 2d grid, e.g. 10 row elements for each of the 10 column


    # random starting position on either x or x or y axis for player 1 / 2
    edge_positions = [(0, random.randint(0, grid_size - 1)), (random.randint(0, grid_size - 1), 0)]
    row, col = random.choice(edge_positions)
    grid[row][col] = "1C"

    edge_positions = [(grid_size - 1, random.randint(0, grid_size - 1)), (random.randint(0, grid_size - 1), grid_size - 1)]
    while True:
        row, col = random.choice(edge_positions)
        if grid[row][col] != "1C":
            grid[row][col] = "2C"
            break

    # generating bonus symbols and distributing them
    bonuses = []
    for i in range(grid_size-1):
        bonuses.append("*")
    
    for elem in bonuses:
        rand_x = random.randint(0, grid_size - 1)
        rand_y = random.randint(0, grid_size - 1)
        if not grid[rand_x][rand_y] in ["1C", "2C"]:
            grid[rand_x][rand_y] = "*"
            
    
    return grid

# generating round variables (i.e. which change per round)
def generate_round_variables():
    used_break = False
    extra_turn = False
    
    return used_break, extra_turn

# main generating variables function, utilising the above to get all game variables
def generate_game_variables():
    grid_size, cell_size, window_size, window= generate_window()
    grid = generate_grid(grid_size)
    player1_score, player2_score, player1_break_cards, player2_break_cards, chance_turn, player1_turn, warning_message, winning_message, BLACK, RED, BLUE, GRAY, GREEN, WHITE, extra_turn = generate_playing_variables()

    running = True
    game_active = True
    font = pygame.font.Font(None, 36)
    alt_font = pygame.font.Font(None, 24)
    menu_font = pygame.font.Font(None, 22)

    return grid_size, cell_size, window_size, grid, window, player1_score, player2_score, player1_break_cards, player2_break_cards, chance_turn, player1_turn, warning_message, winning_message, BLACK, RED, BLUE, GRAY, GREEN, WHITE, extra_turn ,running, game_active, font, alt_font, menu_font


## HELPER FUNCTIONS

# defining the rules popup option
def display_rules_popup():

    grid_size, cell_size, window_size, window = generate_window()
    window_size = (grid_size * cell_size, grid_size * cell_size + 210)
    rules_window = pygame.display.set_mode(window_size)
    rules_window.fill(WHITE)
    pygame.display.set_caption("Rules of the Game")

    rules_text = [
        "Welcome to the chaser game!",
        "BASICS:",
        "- You can move either horizontally or vertically",
        "- 1C / 2C show player 1 / 2's starting position",
        "- P1 / P2 show past moves for player 1 / 2",
        "HOW TO WIN:",
        "- The player with the most points wins",
        "- The game ends when a player cannot move",
        "BONUSES:",
         "- Symbols * give you bonuses ...",
         " - Extra point cards, between -5 and 20",
         " - Extra turn plus 5 points",
         " - Br cards can break P1 / P2 squares"
    ]

    i = 20
    for line in rules_text:
        if line[-1] in ("!", ":"):
            text = font.render(line, True, BLACK)
            text_rect = text.get_rect() # gets the width of the text_rectangle
            rules_window.blit(text, (10, i))
            
            pygame.draw.line(rules_window, BLACK, (10, i + text_rect.height), (10 + text_rect.width, i + text_rect.height), 2) # starting, ending coordinates of the line

        else:
            text = menu_font.render(line, True, GREEN)
            rules_window.blit(text, (10, i))
        i += 40

    rules_text = "Go to Game? ..."
    rules_message = font.render(f"{rules_text}", True, BLUE)
    window.blit(rules_message, (20, 530))

    pygame.display.flip()

    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting_for_input = False
                pygame.display.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                return_to_game_button = pygame.Rect(30, 530, 200, 300)
                if return_to_game_button.collidepoint(event.pos):
                    pygame.display.set_caption("Chaser Game")
                    waiting_for_input = False  # exit the loop and return to the game


# getting the values to either side / above or below a cell
def get_adjacent_values(row,col):
    
    adjacent_values = {
        "x-1": grid[row - 1][col] if row - 1 >= 0 else None,
        "x+1": grid[row + 1][col] if row + 1 < grid_size else None,
        "y-1": grid[row][col - 1] if col - 1 >= 0 else None,
        "y+1": grid[row][col + 1] if col + 1 < grid_size else None,
    }
    return adjacent_values


# returns True if the cell clicked on is next to, below or above the current P1 / P2 cell
def is_touching(row, col):
    code = "1C" if player1_turn else "2C"

    adjacent_values = get_adjacent_values(row, col)

    for key, value in adjacent_values.items():
        if value == code:
            return True
    else:
        return False
    

# returns True if there is no available move, i.e. all taken cells so cannot move
def no_move(row, col):
    adjacent_values = get_adjacent_values(row, col)

    for key, value in adjacent_values.items():
        if value and value not in ["P1", "P2", "1C", "2C"]:
            return False
    return True
        

# declaring winner logic
def determine_winner(player1_score, player2_score, player1_wins, player2_wins):
                if player1_score > player2_score:
                    player1_wins += 1
                    message = "winner, player 1 "
                elif player2_score > player1_score:
                    player2_wins += 1
                    message = "winner, player 2 "
                else:
                    message = "it's a draw!"
                winning_message = message
                game_active = False
                return player1_wins, player2_wins, winning_message, game_active


# returns True if the cell has already been clicked
def cell_clicked(row,col):
    if grid[row][col] in ["P1", "P2", "1C", "2C"]:
        return True


## GAME FUNCTIONALITY
pygame.init()
# key variable generation
grid_size, cell_size, window_size, grid, window, player1_score, player2_score, player1_break_cards, player2_break_cards, chance_turn, player1_turn, warning_message, winning_message, BLACK, RED, BLUE, GRAY, GREEN, WHITE, extra_turn, running, game_active, font, alt_font, menu_font = generate_game_variables()

player1_wins = 0 
player2_wins = 0
welcome = True
win = pygame.mixer.Sound(win_sound_path)
pop = pygame.mixer.Sound(pop_sound_path)
melody = pygame.mixer.Sound(melody_sound_path)
welcome = pygame.mixer.Sound(welcome_sound_path)
error = pygame.mixer.Sound(error_sound_path)

# Game Loop
while running:
    for event in pygame.event.get():
        if welcome:
            welcome.play()
            display_rules_popup()
            welcome = False
            continue
        
        # Game round variables
        used_break, extra_turn = generate_round_variables()

        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # i.e. if left button was pressed (1 = left)
            row = event.pos[1] // cell_size 
            col = event.pos[0] // cell_size
            # above: event.pos gives you a tuple representing the x and y coordinates of the mouse when the event occurred. [1] retrieves the y-coordinatesand the // floor division rounds down, so gets the row number by calculating how many times the cell size fits into the y-coordinates of the mouse click, giving you the row index of the cell that was clicked
            # and same for event.pos[0] gets the x coordinates, and divides them by cell-size, i.e. how many times it fits into the x-coordinates, thus giving the column index of the clicked cell

            if winning_message:
                play_again_button_rect = pygame.Rect(10, grid_size * cell_size + 90, window_size[0]-20, 30)
                if play_again_button_rect.collidepoint(event.pos):
                    grid_size, cell_size, window_size, grid, window, player1_score, player2_score, player1_break_cards, player2_break_cards, chance_turn, player1_turn, warning_message, winning_message, BLACK, RED, BLUE, GRAY, GREEN, WHITE, extra_turn, running, game_active, font, alt_font, menu_font = generate_game_variables() 
                    continue
            else:
                restart_button = pygame.Rect(grid_size * cell_size // 2 + 10, grid_size * cell_size + 170, 155, 34)
                if restart_button.collidepoint(event.pos):
                    grid_size, cell_size, window_size, grid, window, player1_score, player2_score, player1_break_cards, player2_break_cards, chance_turn, player1_turn, warning_message, winning_message, BLACK, RED, BLUE, GRAY, GREEN, WHITE, extra_turn, running, game_active, font, alt_font, menu_font = generate_game_variables() 
                    continue
            
            show_rules_button = pygame.Rect(10, grid_size * cell_size + 170, 155, 34)
            if show_rules_button.collidepoint(event.pos):
                display_rules_popup()
                continue

            # Skip the rest of the loop if the game is not active (i.e. by the determine_winner function)
            if not game_active:
                continue 

            # warning messages
            warning_message = ""

            # if trying to click outside grid limits
            if not (0 <= row < grid_size and 0 <= col < grid_size):
                message = f"Clicked outside grid parameters."
                warning_message = message
                error.play()
                continue
            
            # if clicking a cell that has already been clicked (unless using break ability)
            if cell_clicked(row, col):
                if player1_turn and player1_break_cards > 0 and grid[row][col] not in ["1C", "2C"]:
                    player1_break_cards -= 1
                    message = "player 1 using break ability"
                    warning_message = message
                    used_break = True
                elif not player1_turn and player2_break_cards > 0 and grid[row][col] not in ["1C", "2C"]:
                    player2_break_cards -= 1
                    message = "player 2 using break ability"
                    warning_message = message
                    used_break = True
                else:
                    message = "Warning! Cell has already been clicked."
                    warning_message = message
                    error.play()
                    continue
            
            # if clicking a cell that is not touching your current position(horizontally or vertically)
            if not is_touching(row, col):
                message = "horizontal / diagonal moves only!"
                warning_message = message
                error.play()
                continue
            
            if used_break:
                value = 0
            else:
                value = grid[row][col]

            # * cells generate a random bonus round
            if grid[row][col] == "*":
                rand_chance = random.randint(1,3)

                if rand_chance == 1:
                    value = random.randint(-5, 20)
                    message = f'Random bonus gives {value}'
                elif rand_chance == 2:
                    value = random.randint(0, 5)
                    message = f'You win {value} and gain a break card!'
                    if player1_turn:
                        player1_break_cards += 1
                    else:
                        player2_break_cards += 1
                else:
                    value = random.randint(0, 20)
                    extra_turn = True
                    message = f'You win {value} and gain a turn'
                
                warning_message = message

            # Updating scores and grid, also checking for winning_position (no_move function) and determining the winner if no_move is True (else switching the turn)
            if player1_turn:
                player1_score += value
                for r in range(grid_size):
                    for c in range(grid_size):
                        if grid[r][c] == "1C":
                            grid[r][c] = "P1"
                        if grid[r][c] == "2C":
                            player2_current = (r, c)
                grid[row][col] = "1C"
                player1_current = (row, col)
                
                if no_move(player2_current[0], player2_current[1]) and player2_break_cards == 0 or no_move(row, col) and player1_turn and player1_break_cards == 0 or no_move(row, col) and not player1_turn and player2_break_cards == 0:
                    player1_wins, player2_wins, winning_message, game_active = determine_winner(player1_score, player2_score, player1_wins, player2_wins)
                    win.play()

                if extra_turn:
                    player1_turn = True
                else:
                    player1_turn = False
                
            else:
                player2_score += value
                for r in range(grid_size):
                    for c in range(grid_size):
                        if grid[r][c] == "2C":
                            grid[r][c] = "P2"
                        if grid[r][c] == "1C":
                            player1_current = (r, c)
                grid[row][col] = "2C"
                player2_current = (row, col)

                if no_move(player1_current[0], player1_current[1]) and player1_break_cards == 0 or no_move(row, col) and player1_turn and player1_break_cards == 0 or no_move(row, col) and not player1_turn and player2_break_cards == 0:
                    player1_wins, player2_wins, winning_message, game_active = determine_winner(player1_score, player2_score, player1_wins, player2_wins)
                    win.play()

                if extra_turn:
                    player1_turn = False
                else:
                    player1_turn = True

            if not warning_message and not winning_message:
                pop.play()


    # Updating the window
    window.fill(BLACK)

    for row in range(grid_size):
        for col in range(grid_size):
            value = grid[row][col]
            pygame.draw.rect(window, BLACK, (col * cell_size, row * cell_size, cell_size, cell_size), 2)
        
            
            # changing cell values and colors based on P1 or P2 clicking on them
            if value == "P1":
                color = RED
            elif value == "P2":
                color = BLUE
            elif value == "1C" or value == "2C":
                color = GREEN
            else:
                color = GRAY
            pygame.draw.rect(window, color, (col * cell_size + 2, row * cell_size + 2, cell_size - 4, cell_size - 4))


            text = font.render(str(value), True, BLACK)
            text_rect = text.get_rect(center=(col * cell_size + cell_size // 2, row * cell_size + cell_size // 2))
            window.blit(text, text_rect)
    

    # Drawing player scores below the grid
    if player1_turn:
        player1_text = font.render(f"P1 Score: {player1_score}, wins {player1_wins}, br {player1_break_cards}", True, RED)
        pygame.draw.rect(window, WHITE, (10, grid_size * cell_size + 10, grid_size * cell_size-10, 30))
        window.blit(player1_text, (10, grid_size * cell_size + 10))

        player2_text = font.render(f"P2 Score: {player2_score}, wins {player2_wins}, br {player2_break_cards}", True, BLUE)
        window.blit(player2_text, (10, grid_size * cell_size + 50))
    else:
        player2_text = font.render(f"P2 Score: {player2_score}, wins {player2_wins}, br {player2_break_cards}", True, BLUE)
        pygame.draw.rect(window, WHITE, (10, grid_size * cell_size + 50, grid_size * cell_size-10 ,30))
        window.blit(player2_text, (10, grid_size * cell_size + 50))

        player1_text = font.render(f"P1 Score: {player1_score}, wins {player1_wins}, br {player1_break_cards}", True, RED)
        window.blit(player1_text, (10, grid_size * cell_size + 10))

    # Displaying a message showing whose turn it it
    pygame.draw.rect(window, WHITE, (10, grid_size * cell_size + 90, grid_size * cell_size-10, 30))
    turn_text = "Player 1's turn!" if player1_turn else "Player 2's turn!"
    color = RED if player1_turn else BLUE
    turn_message = font.render(f"{turn_text}", True, color)
    window.blit(turn_message, (15, grid_size * cell_size + 90))

    # displaying warning messages (or if player using special ability e.g. using a bonus break card or extra turn)
    if warning_message:
        if warning_message in ["Warning! Cell has already been clicked.", "horizontal / diagonal moves only!", "Clicked outside grid parameters."]:
            pygame.draw.rect(window, RED, (10, grid_size * cell_size + 130, grid_size * cell_size-10, 30))
            warning_text = alt_font.render(f"{warning_message}", True, BLACK)
            window.blit(warning_text, (15, grid_size * cell_size + 135))
        else:
            pygame.draw.rect(window, GREEN, (10, grid_size * cell_size + 130, grid_size * cell_size-10, 30))
            warning_text = alt_font.render(f"{warning_message}", True, BLACK)
            window.blit(warning_text, (15, grid_size * cell_size + 135))

    # displaying the winning message and play again button
    if winning_message:
        pygame.draw.rect(window, WHITE, (10, grid_size * cell_size + 130, grid_size * cell_size-10, 30))
        color = RED if player1_score > player2_score  else BLUE
        winning_text = alt_font.render(f"{winning_message}", True, color)
        window.blit(winning_text, (15, grid_size * cell_size + 135))

        pygame.draw.rect(window, GREEN, (10, grid_size * cell_size + 90, grid_size * cell_size-10, 30))
        play_again_text = "Play Again?"
        play_again_message = font.render(f"{play_again_text}", True, BLACK)
        window.blit(play_again_message, (15, grid_size * cell_size + 95))

    # button to link to showing rules screen
    rules_text = "Show Rules?"
    rules_message = font.render(f"{rules_text}", True, BLACK)
    rules_text_rect = rules_message.get_rect()
    pygame.draw.rect(window, GREEN, (10, grid_size * cell_size + 170, rules_text_rect.width, rules_text_rect.height + 10))

    window.blit(rules_message, (10 , grid_size * cell_size + 175))

    # restart button if there is no winning_message (i.e. mid-game)
    if not winning_message:
        restart_text = "Restart"
        restart_message = font.render(f"{restart_text}", True, BLACK)
        restart_text_rect = restart_message.get_rect()
        pygame.draw.rect(window, BLUE, (grid_size * cell_size // 2 + 10, grid_size * cell_size + 170, rules_text_rect.width, restart_text_rect.height + 10))

        window.blit(restart_message, (grid_size * cell_size // 2 + 30 , grid_size * cell_size + 175))

    pygame.display.flip()

pygame.quit()
