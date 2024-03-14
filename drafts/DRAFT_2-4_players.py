import pygame
from pygame.locals import *
import sys
import random

## media files

## loading icons
                
resources_symbol = pygame.image.load("media/images/resources_icon.png")
hp_symbol = pygame.image.load("media/images/hp_icon.png")
damage_symbol = pygame.image.load("media/images/damage_icon.png")
comms_symbol = pygame.image.load("media/images/comms_icon.png")
naval_symbol = pygame.image.load("media/images/navy_icon.png")
spec_ops_symbol = pygame.image.load("media/images/spec_ops_icon.png")
air_attack_symbol = pygame.image.load("media/images/air_attack_icon.png")
air_defense_symbol = pygame.image.load("media/images/air_defense_icon.png")
plus_symbol_icon = pygame.image.load("media/images/plus_symbol.png")

mute_icon = pygame.image.load("media/images/muted_icon.png")
unmute_icon = pygame.image.load("media/images/unmuted_icon.png")

icons = {
    "Resources": resources_symbol,
    "HP": hp_symbol,
    "damage": damage_symbol,
    "comms": comms_symbol,
    "naval": naval_symbol,
    "spec_ops": spec_ops_symbol,
    "air_attack": air_attack_symbol,
    "air_defense": air_defense_symbol,
    "Upgrade": plus_symbol_icon,
    "mute": mute_icon,
    "un_mute": unmute_icon,
}

# loading sounds
import os
pygame.mixer.init()

# Set up the paths to the sound files (e.g. effects_directory would be root directory i.e. chaser.effects

# then win_sound_path would be chaser.effects.win
current_directory = os.path.dirname(__file__)
effects_directory = os.path.join(current_directory, 'media', 'sounds')
pop_sound_path = os.path.join(effects_directory, 'pop.mp3')
battle_sound_path = os.path.join(effects_directory, 'battle.mp3')
HQ_down_sound_path = os.path.join(effects_directory, 'HQ_down.mp3')
info_sound_path = os.path.join(effects_directory, 'info.mp3')

#sounds 
sounds = {
    "pop": pygame.mixer.Sound(pop_sound_path),
    "battle": pygame.mixer.Sound(battle_sound_path),
    "HQ_down": pygame.mixer.Sound(HQ_down_sound_path),
    "info": pygame.mixer.Sound(info_sound_path)
}

## Global variables (colors and fonts)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
LIGHT_GRAY = (235, 235, 224)

pygame.init()
title_font = pygame.font.Font(None, 24)
font = pygame.font.Font(None, 20)

## CLASSES
# cell, HQ and terrain classes
class Cell:
    def __init__(self, resources, HP, damage, comms, naval, spec_ops, air_attack, air_defense, controlled_by):
        self.resources = resources
        self.HP = HP
        self.damage = damage
        self.comms = comms
        self.naval = naval
        self.spec_ops = spec_ops
        self.air_attack = air_attack
        self.air_defense = air_defense
        self.controlled_by = controlled_by

    def __str__(self):
        return f'Cell: R: {self.resources}, HP: {self.HP}, damage: {self.damage}, comms: {self.comms}, naval: {self.naval}, spec_ops: {self.spec_ops}, air_attack: {self.air_attack}, air_defense = {self.air_defense}, controlled by: {self.controlled_by}'
    
    
class HQ (Cell):
    def __init__(self, resources, controlled_by, captured=False):
        super().__init__(resources, HP=3, damage=3, comms=0, naval=0, spec_ops=0, air_attack=0, air_defense=3, controlled_by=controlled_by) 
        self.captured = captured

    def __str__(self):
        return f'HQ: captured: {self.captured} R: {self.resources}, HP: {self.HP}, damage: {self.damage}, comms: {self.comms}, naval: {self.naval}, spec_ops: {self.spec_ops}, air_attack: {self.air_attack}, air_defense = {self.air_defense}, controlled by: {self.controlled_by}'
    

class Terrain (Cell):
    def __init__(self, resources, controlled_by, type, color, advantage):
        super().__init__(resources, HP=1, damage=1, comms=0, naval=1, spec_ops=1, air_attack=1, air_defense=1, controlled_by=controlled_by)
        self.type = type
        self.color = color
        self.advantage = advantage
    
    def __str__(self):
        return f'Terrain: type: {self.type} advantage: {self.advantage} R: {self.resources}, HP: {self.HP}, damage: {self.damage}, comms: {self.comms}, naval: {self.naval}, spec_ops: {self.spec_ops}, air_attack: {self.air_attack}, air_defense = {self.air_defense}, controlled by: {self.controlled_by}'
    

# player classes
class Player:
    def __init__(self, name, color, wins, score=500, turns=3):
        self.name = name
        self.wins = wins
        self.color = color
        self.score = score
        self.turns = turns
        self.defeated = False
    
    def turn(self):
        if self.turns == 0:
            pass
        else:
            self.turns -= 1

## HELPER FUNCTIONS
            
## game setup
# game initialization variables
def generate_game_variables(player_count):

    water_cell_color = (0, 153, 255)
    desert_cell_color = (244, 164, 96)
    mountains_cell_color = (105, 105, 105)
    current_cell_color = (255, 153, 255)

    """
player1_cell_color = (0, 0, 230)
player2_cell_color = (230, 0, 0)
player3_cell_color = (255, 0, 255)
player4_cell_color = (255, 92, 51)"""

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

def generate_round_variables(players):

    running = True
    current_player = random.choice(players)
    clicked_cell = None
    info_message=""
    print(f'current player: {current_player.name}')
    game_active = True

    return running, current_player, clicked_cell, info_message, game_active

            
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

# Main game function
def start_game(players, grid_window, screen_size, grid_size):
    for player in players:
        player.score = 500
    grid, screen, cols, rows, cell_size = initialize_game(players, grid_window, screen_size, grid_size)

    running, current_player, clicked_cell, info_message, game_active = generate_round_variables(players)

    current_player.turns = 3

    return grid, screen, cols, rows, grid_size, running, current_player, clicked_cell, info_message, game_active , cell_size

## game helper functions

def get_surrounding_cells(row, col, grid):
    surrounding_values = {
        "Top": grid[row - 1][col] if row - 1 >= 0 else None,
        "Bottom": grid[row + 1][col] if row + 1 < grid_size else None,
        "Left": grid[row][col - 1] if col - 1 >= 0 else None,
        "Right": grid[row][col + 1] if col + 1 < grid_size else None,

        "Top-Left": grid[row - 1 ][col - 1] if row -1 >= 0 and col -1 >= 0 else None,
        "Top-Right": grid[row - 1][col + 1] if row - 1 >= 0 and col + 1 < grid_size else None,
        "Bottom-Left": grid[row + 1][col -1] if row + 1 < grid_size and col - 1 >= 0 else None,
        "Bottom-Right": grid[row + 1][col + 1] if row + 1 < grid_size and col + 1 < grid_size else None,
    }
    return surrounding_values

def is_touching(row, col, player, grid):
    surrounding_cells = get_surrounding_cells(row, col, grid)

    for direction, cell in surrounding_cells.items():
        if cell is not None and player.name == cell.controlled_by:
            return True
        
    return False

def ability_checker(row, col, player, ability, grid):
    surrounding_cells = get_surrounding_cells(row, col, grid)

    for cell in surrounding_cells.values():
        if cell is not None and cell.controlled_by == player.name and getattr(cell, ability) > 0:
            return True
    
    return False

def switch_player(players, old_current_player):

    index = players.index(old_current_player)

    new_index = (index + 1) % len(players)
    current_player = players[new_index]

    current_player.turns = 3

    return current_player


def take_turn(players, current_player):
    current_player.turn()

    if current_player.turns == 0:
        current_player = switch_player(players, current_player)

        while current_player.defeated:
            current_player = switch_player(players, current_player)
        return current_player
    
    return current_player

def battle(grid, row, col, attacking_player, players):
    defending_cell = grid[row][col]
    defending_player = next((player for player in players if player.name == defending_cell.controlled_by), None)

    defending_cell_power = defending_cell.HP + defending_cell.air_defense
    if isinstance(defending_cell, Terrain):
        defending_cell_power *= defending_cell.advantage

    surrounding_cells = get_surrounding_cells(row, col, grid)

    attacking_power_totals = []
    
    attacking_cells = 1
    total_power = 0

    for direction, cell in surrounding_cells.items():
        if cell is not None and cell.controlled_by == attacking_player.name:
            total = cell.damage + cell.air_attack
            if isinstance(cell, Terrain):
                total *= cell.advantage
            attacking_power_totals.append(total)

        if cell is not None and cell.comms > 0:
            attacking_cells += cell.comms

    print(f' Number of attacking_cells: {attacking_cells}')
    attacking_power_totals.sort()

    if attacking_cells == 1:
        total_power = attacking_power_totals[-1]
        print(f'attacking cell with single power: {total_power} vs defending cell: {defending_cell_power}')

    else:
        while attacking_power_totals and attacking_cells > 0:
            print("popping cell with value", attacking_power_totals[-1])
            total_power += attacking_power_totals.pop()
            attacking_cells -= 1

        print(f'attacking cell with combined power: {total_power} vs defending cell: {defending_cell_power}')

    if total_power > defending_cell_power:
        if isinstance(defending_cell, HQ):
            defending_player.defeated = True
            print(f'HQ captured: player{defending_player.name} : defeated? {defending_player.defeated}')
            takeover(attacking_player, defending_player)
        return "attacker won"
    elif total_power == defending_cell_power:
        return "stalemate, new round"
    else:
        return "defender won, new round"

def takeover(attacking_player, defending_player):
    for row in range(rows):
        for col in range(cols):
            cell = grid[row][col]
            if cell.controlled_by == defending_player.name:
                cell.controlled_by = attacking_player.name

def last_survivor(current_player, players):
    active_players = [player for player in players if player.name != current_player.name and player.defeated == False]

    return False if active_players else True

def update_scores(grid, rows, cols, current_player):
    for row in range(rows):
        for col in range(cols):
            cell= grid[row][col]
            if cell.controlled_by == current_player.name:
                current_player.score += cell.resources

def check_sound(sounds, sound):
    return sounds[sound].play() if sound_active else None

def update_info_message(info_message, string):
    info_message = string
    if info_message:
        check_sound(sounds, "info")
    return info_message

## drawing grid functions
# drawing the table from the icons and selected_attributes
def draw_attribute_table(screen, icons):
    pygame.draw.rect(screen, LIGHT_GRAY, (grid_size * cell_size + 5, 0, cell_size * 2 - 10, cell_size * 2))

    header = title_font.render("Upgrades Table", True, BLACK)
    max_height = title_font.get_height()
    screen.blit(header, (grid_size * cell_size + 45, 10))

    sub_header = font.render("Min  |  Max  |  Improve  |  Downgrade", True, BLUE)
    screen.blit(sub_header, (grid_size * cell_size + 45, 40))

    y = 70
    for attribute, values in attribute_values.items():
        icon = icons.get(attribute, None)
        if icon:
            if icon.get_height() > max_height:
                icon = pygame.transform.scale(icon, (int(icon.get_width() * max_height / icon.get_height()), max_height))
            screen.blit(icon, (grid_size * cell_size + 10, y))

            for i, value in enumerate(values):
                x_offset = 50 if i < len(values) - 1 else 70
                text = font.render(str(value), True, BLACK)
                screen.blit(text, (grid_size * cell_size + x_offset + i * 50, y + 5))

            y += 30

def game_choices():
    pygame.init()
    screen = pygame.display.set_mode((600, 400))

    pygame.display.set_caption("Welcome!")
    screen.fill(LIGHT_GRAY)

    welcome_text = [
        "Welcome to the battlefield strategy game!",
        "You win by eliminating enemy HQs!",
        "You gain resources for power ups by controlling positions",
        "Choose 2-4 player options ..."
    ]

    y = 20
    for line in welcome_text:
        text = title_font.render(line, True, BLACK)
        screen.blit(text, (10, y))
        y += 40

    # choosing player count options
    buttons = []

    x = 85
    for i in range(2, 5):
        option_text = f'{i} Players'
        options_message = title_font.render(f"{option_text}", True, BLUE)
        text_rect = options_message.get_rect()
        # tect_rect.height = 17, width = 71

        button_rect = pygame.draw.rect(screen, WHITE, (x, y + 50, text_rect.width + 20, text_rect.height + 20))
        buttons.append((button_rect, i))
        screen.blit(options_message, (x + 10, y + 60))
        x += 170

    player_count = None
    """ (3 or 4 / 2 players)
    grid_window = (750, 750) / (600, 600)
    screen = pygame.display.set_mode((1020, 785)) / (870, 640)
    pygame.display.set_caption("Battlefield Map")

    screen.fill(WHITE)

    cell_size = 145 ""
    cols, rows = grid_window[0] // cell_size, grid_window[1] // cell_size ""
    grid_size = 5 / 4
    """

    pygame.display.flip()

    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting_for_input = False
                pygame.display.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for button_rect, count in buttons:
                    if button_rect.collidepoint(event.pos):
                        player_count = count
                        if player_count == 2:
                            grid_window = (600, 600)
                            screen_size = (870, 640)
                            grid_size = 4
                        elif player_count in [3,4]:
                            grid_window = (750, 750)
                            screen_size = (1020, 785)
                            grid_size = 5

                if player_count:
                    start_text = f'start game with {player_count} players'
                    start_message = title_font.render(f"{start_text}", True, WHITE)
                    start_rect = start_message.get_rect()

                    pygame.draw.rect(screen, BLUE, ((300 - (start_rect.width // 2)), y + 150, start_rect.width + 20, start_rect.height + 20))
                    screen.blit(start_message, (300 - (start_rect.width // 2) + 10, y + 160))

                    start_game_button = pygame.Rect(300 - (start_rect.width // 2), y + 150, start_rect.width + 20, start_rect.height + 20)
                    if start_game_button.collidepoint(event.pos):
                        print(f'starting game with {player_count}')
                        pygame.display.set_caption("Battlefield Game")
                        screen.fill(WHITE)
                        waiting_for_input = False
                        return player_count, grid_window, screen_size, grid_size

        pygame.display.flip()


def display_rules_popup(screen_size):
    rules_screen_size = (900, 790)

    screen = pygame.display.set_mode((rules_screen_size))
    screen_width, screen_height = rules_screen_size

    pygame.display.set_caption("Rules of the Game")
    screen.fill(LIGHT_GRAY)

    rules_text = [
        [
            "STARTING:",
            "- You can move at most 1 position in any direction",
            "- Your HQ is the starting position",
            "- Each position has it's own attributes",
            "- Positional resources are added after each round"
        ],
        [
            "ROUNDS AND TURNS:",
            "- In a Round a player will have 3 turns, including ...",
            "  - Moving and occupying a new position",
            "  - Fortifying a current position",
            "  - Moving and attacking an enemy position",
        ],
        [
            "TERRAIN CELLS:",
            "- Terrain cells can require attributes to enter",
            "- But they have an advantage over normal cells ....",
            "- Mountains have 2* advantage",
            "- Water has 1.5 * advantage",
            "- Desert has a 0.5 disadvantage",
        ],
        [
            "HOW TO FORTIFY:",
            "- On selected cell press u to view current attribute",
            "- Click 1-7 to change attribute",
            "- To upgrade attributes: keys w or up arrow",
            "- To downgrade attributes: keys s or down arrow",
            "- See upgrade table for costs etc",
        ],
        [
           "BATTLES:",
            "- When you try to occupy enemy positions ...",
            "- If you have a stronger adjacent cell you will win",
            "- If there is a draw / loss you also lose your turns",
            "* Attackers use terrain advantage, damage and air_attack",
            "* Defenders use terrain advantage, HP and air_defense",
            "   NOTE: Comms allows you to attack with Multiple positions",
            "   e.g. comms of 1 allows 2 positions to combine forces etc",

        ],
        [
            "HOW TO WIN:",
            "- Capture HQs to take over all the players positions",
            "- You win by eliminating all enemy HQ's"
        ],
    ]

    y, y2 = (20, 20)
    for i in range(len(rules_text)):
        if i % 2 == 0:
            for line in rules_text[i]:
                if line[-1] in ("!", ":"):
                    text = title_font.render(line, True, BLUE)
                    text_rect = text.get_rect()
                    screen.blit(text, (10, y))
                    
                    pygame.draw.line(screen, BLACK, (10, y + text_rect.height), (10 + text_rect.width, y + text_rect.height), 2) 
                    y += 40
                else:
                    text = title_font.render(line, True, BLACK)
                    text_rect = text.get_rect()
                    screen.blit(text, (10, y))
                    y += 40
        else:
            for line in rules_text[i]:
                if line[-1] in ("!", ":"):
                    text = title_font.render(line, True, BLUE)
                    text_rect = text.get_rect()
                    screen.blit(text, (screen_width // 2 + 10, y2))
                    
                    pygame.draw.line(screen, BLACK, (screen_width // 2 + 10, y2 + text_rect.height), (screen_width // 2 + 10 + text_rect.width, y2 + text_rect.height), 2) 
                    y2 += 40
                else:
                    text = title_font.render(line, True, BLACK)
                    text_rect = text.get_rect()
                    screen.blit(text, (screen_width // 2 + 10, y2))
                    y2 += 40

    # return to game button
    rules_text = "Go to Game? ..."
    rules_message = title_font.render(f"{rules_text}", True, BLUE)

    text_rect = rules_message.get_rect()

    pygame.draw.rect(screen, GREEN, (screen_width * 0.7, y2 + 40, text_rect.width + 20, text_rect.height + 20))
    screen.blit(rules_message, (screen_width * 0.7 + 10, y2 + 50))

    # RESET GAME / change player count
    reset_text = "Reset Game? ..."
    reset_message = title_font.render(f"{reset_text}", True, WHITE)
    reset_text_rect = reset_message.get_rect()
    pygame.draw.rect(screen, BLUE, (screen_width * 0.7, y2 + 80, reset_text_rect.width + 20, reset_text_rect.height + 20))
    screen.blit(reset_message, (screen_width * 0.7 + 10, y2 + 90))

    pygame.display.flip()

    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting_for_input = False
                pygame.display.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                return_to_game_button = pygame.Rect(screen_width * 0.7, y2 + 40, text_rect.width + 20, text_rect.height + 20)
                if return_to_game_button.collidepoint(event.pos):
                    pygame.display.set_caption("Battlefield Game")
                    pygame.display.set_mode(screen_size)
                    screen.fill(WHITE)
                    waiting_for_input = False 

                reset_button = pygame.Rect(screen_width * 0.7, y2 + 80, reset_text_rect.width + 20, reset_text_rect.height + 20)
                if reset_button.collidepoint(event.pos):
                    screen.fill(WHITE)
                    waiting_for_input = False
                    return True
                """
                player_count, grid_window, screen_size, grid_size = game_choices()

                water_cell_color, desert_cell_color, mountains_cell_color, current_cell_color, player1, player2, player3, player4, players, selected_attribute, attribute_values, sound_active = generate_game_variables(player_count)

                grid, screen, cols, rows, grid_size, running, current_player, clicked_cell, info_message, game_active, cell_size = start_game(players, grid_window, screen_size, grid_size)
                """

def draw_extra_buttons(current_player, title_font, players, grid_size, cell_size):
    # whose turn is it message
    turn_text = f"player {current_player.name}'s round, {current_player.turns} moves left"
    turn_message = title_font.render(f"{turn_text}", True, WHITE)
    turn_text_rect = turn_message.get_rect()

    rect_height = turn_text_rect.height + 20
    COLOR = current_player.color

    pygame.draw.rect(screen, COLOR, (grid_size * cell_size + 5, cell_size * 2 + 5, cell_size * 2 - 10, rect_height))
    screen.blit(turn_message, (grid_size * cell_size + 15, cell_size * 2 + 15))

    
    # Display player information
    stat_boxes = [
    (grid_size * cell_size + 5, cell_size * 2 + 50 + i * 100, cell_size * 2 - 10, 80) for i in range(len(players))]
    
    ## above stat_boxes[i] = tuple of x coordinate, y coordinate, width and heightm used for bordering below ..
    for i, player in enumerate(players):
        if player == current_player:
            pygame.draw.rect(screen, player.color, stat_boxes[i])
            pygame.draw.rect(screen, LIGHT_GRAY, (stat_boxes[i][0] + 4, stat_boxes[i][1] + 4, stat_boxes[i][2] - 8, stat_boxes[i][3] - 8))
        else:
            pygame.draw.rect(screen, LIGHT_GRAY, stat_boxes[i])

        player_lines = [
            f"{player.name}:",
            f"Resources: {player.score}",
            f"Wins: {player.wins}",
        ]

        for j, line in enumerate(player_lines):
            line_render = title_font.render(line, True, BLACK)
            screen.blit(line_render, (stat_boxes[i][0] + 50, stat_boxes[i][1] + 10 + j * 20))
        

    # info message drawing
    pygame.draw.rect(screen, WHITE, (0, grid_size * cell_size + 10, cell_size * (grid_size - 1), 37))

    if info_message is not None:
        pygame.draw.rect(screen, current_cell_color, (0, grid_size * cell_size + 10, cell_size * (grid_size - 1), 37))
        if ":" in info_message:
            selected_attribute = info_message.split(":")[0]
            if icons[selected_attribute]:
                icon = icons[selected_attribute]
                max_height = title_font.get_height()
                if icon.get_height() > max_height:
                    icon = pygame.transform.scale(icon, (int(icon.get_width() * max_height / icon.get_height()), max_height))
                screen.blit(icon, (20, grid_size * cell_size + 20))
                text = title_font.render(info_message, True, BLACK)
                screen.blit(text, (50, grid_size * cell_size + 20))
        elif info_message == "":
            pygame.draw.rect(screen, WHITE, (0, grid_size * cell_size + 10, cell_size * 4, 37))
        else:
            text = title_font.render(info_message, True, BLACK)
            screen.blit(text, (0 + 50, grid_size * cell_size + 20))

        # play again message
        replay_text = "Play again?"
        replay_message = title_font.render(f"{replay_text}", True, WHITE)
        replay_text_rect = turn_message.get_rect()

        rect_height = turn_text_rect.height + 20

        pygame.draw.rect(screen, BLACK, (grid_size * cell_size + 5, grid_size * cell_size + 10, cell_size - 10, rect_height))
        screen.blit(replay_message, (grid_size * cell_size + 25, grid_size * cell_size + 20))

        # display rules message
        rules_text = "View Rules?"
        rules_message = title_font.render(f"{rules_text}", True, WHITE)
        rules_text_rect = rules_message.get_rect()

        rect_height = rules_text_rect.height + 20

        pygame.draw.rect(screen, BLACK, (cell_size * grid_size + cell_size + 5, grid_size * cell_size + 10, cell_size-10, rect_height))
        screen.blit(rules_message, (cell_size * grid_size + cell_size + 25, grid_size * cell_size + 20))

        # mute / unmute buttons
        max_height = 37
        pygame.draw.rect(screen, WHITE, (cell_size * (grid_size - 1) , grid_size * cell_size + 5, cell_size, 40))
        sound_icon = icons["mute"] if sound_active else icons["un_mute"]

        if sound_icon.get_height() > max_height:
                sound_icon = pygame.transform.scale(sound_icon, (int(sound_icon.get_width() * max_height / sound_icon.get_height()), max_height))
                
        screen.blit(sound_icon, (cell_size * (grid_size - 1) + 60, grid_size * cell_size + 5)) 


def draw_grid(rows, cols, grid, player1, player2, player3, player4, cell_size, title_font, icons):
    for row in range(rows):
        for col in range(cols):
            cell = grid[row][col]
            new_color_value = min(cell.resources * 2.5, 255)
            pygame.draw.rect(screen, (0,new_color_value, 0), (col * cell_size, row * cell_size, cell_size, cell_size))
            # arguments: surface, color (shade of green in accordance to the resources available), then (x coordinate at top left corner, y coordinate at top left corner, width, height)

            player_colors = {
                "P1": player1.color,
                "P2": player2.color,
                "P3": player3.color,
                "P4": player4.color,
            }

            # Assuming cell.controlled_by contains the player name
            player_color = player_colors.get(cell.controlled_by)

            if cell == clicked_cell:
                pygame.draw.rect(screen, player_color, (col * cell_size, row * cell_size, cell_size, cell_size))
                pygame.draw.rect(screen, current_cell_color, (col * cell_size + 4, row * cell_size + 4, cell_size - 8, cell_size - 8))

            elif isinstance(cell, HQ):
                pygame.draw.rect(screen, BLACK, (col * cell_size, row * cell_size, cell_size, cell_size)) # drawn rectangle i.e. border, top left coordinates, top right then width, height
                pygame.draw.rect(screen, player_color, (col * cell_size + 4, row * cell_size + 4, cell_size - 8, cell_size - 8)) # filled rectangle, starting + 2 on each axis then -4 on width and length to keep it within the square

            elif isinstance(cell, Terrain):
                if cell.controlled_by == "":
                    pygame.draw.rect(screen, cell.color, (col * cell_size, row * cell_size, cell_size, cell_size))
                else:
                    pygame.draw.rect(screen, player_color, (col * cell_size, row * cell_size, cell_size, cell_size))
                    pygame.draw.rect(screen, cell.color, (col * cell_size + 4, row * cell_size + 4, cell_size - 8, cell_size - 8))
            else:
                if cell.controlled_by:
                    pygame.draw.rect(screen, player_color, (col * cell_size, row * cell_size, cell_size, cell_size))

            cell_info = {
                "Resources": cell.resources,
                "Player": cell.controlled_by,
                "HP": cell.HP,
                "damage": cell.damage,
                "comms": cell.comms,
                "naval": cell.naval,
                "spec_ops": cell.spec_ops,
                "air_attack": cell.air_attack,
                "air_defense": cell.air_defense
            }

            y = 10
            for index, (label, item) in enumerate(cell_info.items()):
                if label == "Resources":
                    if isinstance(cell, HQ):
                        label = "HQ"
                    elif isinstance(cell, Terrain):
                        label = cell.type
                    else:
                        label = ""

                    icon = icons["Resources"]
                    max_height = title_font.get_height()
                    if icon.get_height() > max_height:
                        icon = pygame.transform.scale(icon, (int(icon.get_width() * max_height / icon.get_height()), max_height))
                        # above, if icon is bigger than font height, sets new width as relative to max_height to keep same ratio, then sets height as max_height
                    screen.blit(icon, (col * cell_size + 10, row * cell_size + y))
                    if label == "Mountains":
                        alt_title_font = pygame.font.Font(None, 22) 
                        text = alt_title_font.render(f'{label} {item}', True, WHITE)
                        screen.blit(text, (col * cell_size + 30, row * cell_size + y))
                    else:
                        text = title_font.render(f'{label} {item}', True, WHITE)
                        screen.blit(text, (col * cell_size + 30, row * cell_size + y))
                    y += 25

                elif label == "Player" or label == "Resources":
                    text = title_font.render(f'{label}: {item}', True, WHITE)
                    screen.blit(text, (col * cell_size + 10, row * cell_size + y))
                    y += 25

                elif label in icons:
                    icon = icons[label]
                    scaling_factor = 0.4
                    new_width = int(icon.get_width() * scaling_factor)
                    new_height = int(icon.get_height() * scaling_factor)
                    max_height = 2 * font.get_height()

                    if icon.get_height() > max_height:
                        icon = pygame.transform.scale(icon, (new_width, new_height))
                        # above, if icon is bigger than font height, sets new width as relative to max_height ratio, then sets height as max_height, scaling_factor allows size changes
                    if index % 2 == 0:
                        screen.blit(icon, (col * cell_size + 10, row * cell_size + y))
                        text = font.render(f'{item}', True, WHITE)
                        screen.blit(text, (col * cell_size + 10 + 30, row * cell_size + y))
                    else:
                        screen.blit(icon, (col * cell_size + 70, row * cell_size + y))
                        text = font.render(f'{item}', True, WHITE)
                        screen.blit(text, (col * cell_size + 70 + 30, row * cell_size + y))
                        y += 20

# main pygame drawing function
def pygame_setup(screen, icons, current_player, title_font, player1, player2, player3, player4, grid_size, cell_size, rows, cols, grid):
    draw_attribute_table(screen, icons)
    draw_extra_buttons(current_player, title_font, players, grid_size, cell_size)
    draw_grid(rows, cols, grid, player1, player2, player3, player4, cell_size, title_font, icons)

## Main game loop
    
player_count, grid_window, screen_size, grid_size = game_choices()

water_cell_color, desert_cell_color, mountains_cell_color, current_cell_color, player1, player2, player3, player4, players, selected_attribute, attribute_values, sound_active = generate_game_variables(player_count)

grid, screen, cols, rows, grid_size, running, current_player, clicked_cell, info_message, game_active, cell_size = start_game(players, grid_window, screen_size, grid_size)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            row = event.pos[1] // cell_size 
            col = event.pos[0] // cell_size

            """
            pygame.draw.rect(screen, BLACK, (grid_size * cell_size + 5, grid_size * cell_size + 10, cell_size - 10, rect_height))
            pygame.draw.rect(screen, BLACK, (cell_size * grid_size + cell_size + 5, grid_size * cell_size + 10, cell_size-10, rect_height))
            """

            restart_button = pygame.Rect(grid_size * cell_size + 5, grid_size * cell_size + 10, cell_size - 10, 40)
            if restart_button.collidepoint(event.pos):
                grid, screen, cols, rows, grid_size, running, current_player, clicked_cell, info_message, game_active, cell_size = start_game(players, grid_window, screen_size, grid_size)
                continue
            rules_button = pygame.Rect(cell_size * grid_size + cell_size + 5, grid_size * cell_size + 10, cell_size-10, 40)
            if rules_button.collidepoint(event.pos):
                reset = display_rules_popup(screen_size)
                if reset:
                    player_count, grid_window, screen_size, grid_size = game_choices()
                    water_cell_color, desert_cell_color, mountains_cell_color, current_cell_color, player1, player2, player3, player4, players, selected_attribute, attribute_values, sound_active = generate_game_variables(player_count)
                    grid, screen, cols, rows, grid_size, running, current_player, clicked_cell, info_message, game_active, cell_size = start_game(players, grid_window, screen_size, grid_size)
                continue

            mute_button = pygame.Rect((cell_size * (grid_size - 1) + 60, grid_size * cell_size + 5, 40, 40))
            if mute_button.collidepoint(event.pos):
                sound_active = False if sound_active == True else True
                info_message = "Game muted" if sound_active == False else "Game unmuted"
                continue

            if not game_active:
                info_message = "Game not active, please start new game"
                continue

            info_message = ""
            if 0 <= row < grid_size and 0 <= col < grid_size:
                cell = grid[row][col]
            else:
                info_message = update_info_message(info_message, "Clicked outside grid")
                continue

            if not is_touching(row, col, current_player, grid) and cell.controlled_by != current_player.name:
                out_of_range = True
                info_message = update_info_message(info_message, "Need to click on touching cells")
                continue
            elif isinstance(cell, Terrain) and cell.controlled_by == "":
                if cell.type == "Water" and not ability_checker(row, col, current_player, "naval", grid):
                    info_message = update_info_message(info_message, "Need a navy in an adjacent cell to access water")
                    continue
                elif cell.type == "Mountains" and not ability_checker(row, col, current_player, "spec_ops", grid):
                    info_message = update_info_message(info_message, "Need spec_ops in an adjacent cell to access mountains")
                    continue
            elif cell.controlled_by and cell.controlled_by != current_player.name:
                if isinstance(cell, Terrain) and cell.type == "Water" and not ability_checker(row, col, current_player, "naval", grid):
                    info_message = update_info_message(info_message, "Need a navy in an adjacent cell to Attack water")
                    continue
                elif isinstance(cell, Terrain) and cell.type == "Mountains" and not ability_checker(row, col, current_player, "spec_ops", grid):
                    info_message = update_info_message(info_message, "Need spec_ops in an adjacent cell to Attack mountains")
                    continue
                else:
                    check_sound(sounds, "battle")
                    defending_player = next((player for player in players if player.name == cell.controlled_by), None)
                    if battle(grid, row, col, current_player, players) == "attacker won":
                        clicked_cell = grid[row][col]
                        if isinstance(cell, HQ):
                            info_message = f'player{defending_player.name} eliminated by {current_player.name}'
                            cell.controlled_by = current_player.name
                            check_sound(sounds, "HQ_down")
                            if last_survivor(current_player, players):
                                info_message = f'winner =  {current_player.name}'
                                current_player.wins += 1
                                game_active = False
                                continue
                            current_player = take_turn(players, current_player)
                            continue
                        else:
                            info_message = "Attacker won the battle"
                            current_player = take_turn(players, current_player)
                            pass
                    elif battle(grid, row, col, current_player, players) == "stalemate, new round":
                        info_message = "Stalemate, switching players"
                        clicked_cell = None
                        current_player.turns = 0
                        current_player = take_turn(players, current_player)
                        continue
                    else:
                        info_message = "attack failed, switching players"
                        clicked_cell = None
                        current_player.turns = 0
                        current_player = take_turn(players, current_player)
                        continue
                        
            else:
                clicked_cell = grid[row][col]
                check_sound(sounds, "pop")
                info_message = ""

                if clicked_cell.controlled_by == current_player.name:
                    continue

            cell.controlled_by = current_player.name

            if current_player.turns == 1:
                update_scores(grid, rows, cols, current_player)
                clicked_cell = None
            current_player = take_turn(players, current_player)
        

        elif event.type == KEYDOWN:
            info_message = ""
            if clicked_cell is not None and clicked_cell.controlled_by == current_player.name:
                if event.key == K_u:
                    info_message = f'{selected_attribute}: {getattr(clicked_cell, selected_attribute)}'

                elif event.key == K_1:
                    selected_attribute = "HP"
                elif event.key == K_2:
                    selected_attribute = "damage"
                elif event.key == K_3:
                    selected_attribute = "comms"
                elif event.key == K_4:
                    selected_attribute = "naval"
                elif event.key == K_5:
                    selected_attribute = "spec_ops"
                elif event.key == K_6:
                    selected_attribute = "air_attack"
                elif event.key == K_7:
                    selected_attribute = "air_defense"
                
                info_message = f'{selected_attribute}: {getattr(clicked_cell, selected_attribute)}'
                
                min_val, max_val, upgrade_cost, downgrade_benefit = attribute_values[selected_attribute] # i.e. 4 values from the nested dictionary
                
                if event.key == K_w or event.key == K_UP:
                    if getattr(clicked_cell, selected_attribute) == max_val:
                        info_message = f'{selected_attribute}: Max reached'
                    elif upgrade_cost > current_player.score:
                        info_message = f'{selected_attribute}: Unable to upgrade, curr resources = {current_player.score}'
                        pass
                    else:
                        setattr(clicked_cell, selected_attribute, getattr(clicked_cell, selected_attribute) + 1)
                        current_player.score -= upgrade_cost
                        info_message = f'{selected_attribute}: upgraded: total upgrade cost = {upgrade_cost} resources'
                        if current_player.turns == 1:
                            update_scores(grid, rows, cols, current_player)
                            clicked_cell = None
                        current_player = take_turn(players, current_player)
                elif event.key == K_s or event.key == K_DOWN:
                    if getattr(clicked_cell, selected_attribute) == min_val:
                        info_message = f'{selected_attribute}: Min reached'
                    else:
                        setattr(clicked_cell, selected_attribute, max(getattr(clicked_cell, selected_attribute) - 1, 0))
                        current_player.score += downgrade_benefit
                        info_message = f'{selected_attribute}: downgraded: total downgrade benefit = {downgrade_benefit} resources'
                        if current_player.turns == 1:
                            update_scores(grid, rows, cols, current_player)
                            clicked_cell = None
                        current_player = take_turn(players, current_player)

                if event.key == K_ESCAPE:
                    clicked_cell = None

                if info_message:
                    check_sound(sounds, "info")
        

## PyGame visual updates
        pygame_setup(screen, icons, current_player, title_font, player1, player2, player3, player4, grid_size, cell_size, rows, cols, grid)   

    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()


