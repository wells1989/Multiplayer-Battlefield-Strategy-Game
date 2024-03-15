import pygame
import random
from globals.classes import Cell, Terrain, HQ, Player
from globals.constants import WHITE


# Main game function
def start_game(players, grid_window, screen_size, grid_size):
    for player in players:
        player.score = 500
        player.defeated = False
    grid, screen, cols, rows, cell_size = initialize_game(players, grid_window, screen_size, grid_size)

    running, current_player, clicked_cell, info_message, game_active = generate_round_variables(players)

    current_player.turns = 3

    return grid, screen, cols, rows, grid_size, running, current_player, clicked_cell, info_message, game_active , cell_size


# game initialization permanent variables
def generate_game_variables(player_count):

    water_cell_color = (0, 153, 255)
    desert_cell_color = (244, 164, 96)
    mountains_cell_color = (105, 105, 105)
    current_cell_color = (255, 153, 255)

    player1 = Player(name="P1", wins=0, color=(0, 0, 230))
    player2 = Player(name="P2", wins= 0, color=(230, 0, 0))
    player3 = Player(name="P3", wins= 0, color=(255, 0, 255))
    player4 = Player(name="P4", wins= 0, color=(255, 92, 51))

    if player_count == 2:
        players = [player1, player2]
    elif player_count == 3:
        players = [player1, player2, player3]
    else:
        players = [player1, player2, player3, player4]

    selected_attribute = "HP"  # Initial attribute selection
    attribute_values = {
        "HP": [1, 3, 250, 120], # min, max, upgrade_cost, downgrade_benefit
        "damage": [1, 3, 220, 90],
        "comms": [0, 2, 400, 180],
        "naval": [0, 1, 250, 100],
        "spec_ops": [0, 1, 250, 100],
        "air_attack": [1, 3, 250, 100],
        "air_defense": [1, 3, 250, 100],
    }

    sound_active = False

    return water_cell_color, desert_cell_color, mountains_cell_color, current_cell_color, player1, player2, player3, player4, players, selected_attribute, attribute_values, sound_active


# game initialization transient variables (between each game)
def generate_round_variables(players):

    running = True
    current_player = random.choice(players)
    clicked_cell = None
    info_message=""
    game_active = True

    return running, current_player, clicked_cell, info_message, game_active


# creating grid
def initialize_game(players, grid_window, screen_size, grid_size):
    pygame.init()

    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption("Battlefield Map")

    screen.fill(WHITE)

    cell_size = 145
    cols, rows = grid_window[0] // cell_size, grid_window[1] // cell_size

    starting_players = list(players)

    grid = []

    for row in range(rows):
        grid_row = []
        for col in range(cols):
            if (row == 0 and col == 0) or (row == rows - 1 and col == cols - 1) or (row == 0 and col == cols - 1) or (col == 0 and row == rows-1):
                if starting_players:
                    grid_row.append(HQ(resources=50, controlled_by=starting_players.pop(0).name))
                else:
                    grid_row.append(Cell(resources=random.randint(30, 100), HP=1, damage=1, comms=0, naval=0, spec_ops=0, air_attack=1, air_defense=1, controlled_by=""))
            else:
                terrain_type = random.random()
                if 0 < terrain_type < 0.1:
                    grid_row.append(Terrain(resources=random.randint(60, 180), controlled_by="", type="Water", color=(0, 153, 255), advantage=1.5))
                elif 0.1 < terrain_type < 0.2:
                    grid_row.append(Terrain(resources=random.randint(60, 180), controlled_by="", type="Mountains", color=(105, 105, 105), advantage=2))
                elif 0.2 < terrain_type < 0.25:
                    grid_row.append(Terrain(resources=random.randint(20, 50), controlled_by="", type="Desert", color=(244, 164, 96), advantage=0.5))
                else:
                    grid_row.append(Cell(resources=random.randint(30, 100), HP=1, damage=1, comms=0, naval=0, spec_ops=0, air_attack=1, air_defense=1, controlled_by=""))
        grid.append(grid_row)

    return grid, screen, cols, rows, cell_size


# function to reset game with new player count etc
def reset_game(game_choices):
    player_count, grid_window, screen_size, grid_size = game_choices()
    water_cell_color, desert_cell_color, mountains_cell_color, current_cell_color, player1, player2, player3, player4, players, selected_attribute, attribute_values, sound_active = generate_game_variables(player_count)
    grid, screen, cols, rows, grid_size, running, current_player, clicked_cell, info_message, game_active, cell_size = start_game(players, grid_window, screen_size, grid_size)
    
    return player_count, grid_window, screen_size, grid_size, water_cell_color, desert_cell_color, mountains_cell_color, current_cell_color, player1, player2, player3, player4, players, selected_attribute,attribute_values, sound_active, grid, screen, rows, cols, running, current_player, clicked_cell, info_message, game_active, cell_size
