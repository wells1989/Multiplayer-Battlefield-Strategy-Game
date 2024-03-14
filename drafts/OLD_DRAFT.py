# pre battle sequence

import pygame
from pygame.locals import *
import sys
import random

# Define colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
LIGHT_GRAY = (235, 235, 224)
water_cell_color = (0, 153, 255)
desert_cell_color = (244, 164, 96)
mountains_cell_color = (105, 105, 105)
current_cell_color = (255, 153, 255)

"""
player1_cell_color = (0, 0, 230)
player2_cell_color = (230, 0, 0)
player3_cell_color = (255, 0, 255)
player4_cell_color = (255, 92, 51)"""

player1_cell_color = (0, 0, 230)
player2_cell_color = (230, 0, 0)

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
    
    def __str__(self, resources, HP, damage, comms, naval, spec_ops, air_attack, air_defense, controlled_by):
        return f'R: {resources}, HP: {HP}, damage: {damage}, comms: {comms}, naval: {naval}, spec_ops: {spec_ops}, air_attack: {air_attack}, air_defense = {air_defense}, controlled by: {controlled_by}'
    
class HQ (Cell):
    def __init__(self, resources, controlled_by):
        super().__init__(resources, HP=3, damage=3, comms=0, naval=0, spec_ops=0, air_attack=0, air_defense=3, controlled_by=controlled_by) 

class Terrain (Cell):
    def __init__(self, resources, controlled_by, type, color):
        super().__init__(resources, HP=1, damage=1, comms=0, naval=1, spec_ops=1, air_attack=0, air_defense=0, controlled_by=controlled_by)
        self.type = type
        self.color = color

    def __str__(self, type, resources):
        return f'terrain {type}, resources: {resources}'

# player classes
class Player:
    def __init__(self, name, wins, score, color,turns=3):
        self.name = name
        self.wins = wins
        self.score = score
        self.color = color
        self.turns = turns
    
    def turn(self):
        if self.turns == 0:
            pass
        else:
            self.turns -= 1

# Initialize Pygame
pygame.init()

# Set up the display window

grid_window = (600, 600)
screen = pygame.display.set_mode((900, 800))
pygame.display.set_caption("Battlefield Map")

title_font = pygame.font.Font(None, 24)
font = pygame.font.Font(None, 20)

screen.fill(WHITE)


# Define the grid and cell size
cell_size = 150
cols, rows = grid_window[0] // cell_size, grid_window[1] // cell_size
grid_size = 4

# 2 players initially
player1 = Player("P1", wins=0, score=500, color=(0, 0, 230))
player2 = Player("P2", wins=0, score=500, color=(230, 0, 0))


players = {player1.name, player2.name}
grid = [[HQ(resources=50, controlled_by=players.pop()) 
         if (row == 0 and col == 0) or (row == rows - 1 and col == cols - 1)
         else (
            Terrain(resources=random.randint(60, 180), controlled_by="", type="Water", color=(0, 153, 255)) if 0 < random.random() < 0.1 else
            Terrain(resources=random.randint(60, 180), controlled_by="", type="Mountains", color=(105, 105, 105)) if 0.1 < random.random() < 0.2 else
            Terrain(resources=random.randint(20, 50), controlled_by="", type="Desert", color=(244, 164, 96)) if 0.2 < random.random() < 0.25 else
            Cell(resources=random.randint(30, 100), HP=1, damage=1, comms=0, naval=0, spec_ops=0, air_attack=1, air_defense=1, controlled_by="")
        )
         for col in range(cols)] for row in range(rows)]
        # above, assigning HQ's controlled by random allocation, then adding else, based on random int, creates either a water / mountains / desert terrain or a normal call

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

icons = {
    "Resources": resources_symbol,
    "HP": hp_symbol,
    "damage": damage_symbol,
    "comms": comms_symbol,
    "naval": naval_symbol,
    "spec_ops": spec_ops_symbol,
    "air_attack": air_attack_symbol,
    "air_defense": air_defense_symbol,
    "Upgrade": plus_symbol_icon
}

## helper functions

def get_surrounding_cells(row, col):
    surrounding_values = {
        "Left": grid[row - 1][col] if row - 1 >= 0 else None,
        "Right": grid[row + 1][col] if row + 1 < grid_size else None,
        "Top": grid[row][col - 1] if col - 1 >= 0 else None,
        "Bottom": grid[row][col + 1] if col + 1 < grid_size else None,

        "Top-Left": grid[row -1 ][col - 1] if row -1 >=0 and col -1 >= 0 else None,
        "Top-Right": grid[row + 1][col + 1] if row + 1 < grid_size and col + 1 < grid_size else None,
        "Bottom-Left": grid[row - 1][col + 1] if row - 1 >= 0 and col + 1 < grid_size else None,
        "Bottom-Right": grid[row + 1][col + 1] if row + 1 < grid_size and col + 1 < grid_size else None,
    }
    return surrounding_values


def is_touching(row, col, player, clicked_cell):
    surrounding_cells = get_surrounding_cells(row, col)

    for direction, cell in surrounding_cells.items():
        if cell is not None and player.name == cell.controlled_by:
            return True
        
    return False


def ability_checker(row, col, player, ability):
    surrounding_cells = get_surrounding_cells(row, col)

    for cell in surrounding_cells.values():
        if cell is not None and cell.controlled_by == player.name and getattr(cell, ability) > 0:
            return True
    
    return False

def spec_ops_ability(row, col, player):
    surrounding_cells = get_surrounding_cells(row, col)

    for cell in surrounding_cells.values():
        if cell is not None and cell.controlled_by == player.name and cell.spec_ops > 0:
            return True
    
    return False



# drawing the table from the icons and selected_attributes
def draw_attribute_table(screen, icons, selected_attribute):
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

def take_turn(current_player):
    current_player.turn()

    if current_player.turns == 0:
        current_player = player2 if current_player == player1 else player1
        current_player.turns = 3
        return current_player
    
    return current_player

## Main game loop
running = True
current_player = random.choice([player1, player2])
clicked_cell = None
info_message=""
print(f'current player: {current_player.name}')

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            row = event.pos[1] // cell_size 
            col = event.pos[0] // cell_size

            info_message = ""
            print(info_message)
            if 0 <= row < grid_size and 0 <= col < grid_size:
                cell = grid[row][col]
            else:
                print("clicked outside grid")
                info_message = "Clicked outside grid"
                continue

            if not is_touching(row, col, current_player, cell) and cell.controlled_by != current_player.name:
                out_of_range = True
                print("need to click on touching cells")
                info_message = "Need to click on touching cells"
                continue
            elif isinstance(cell, Terrain):
                if cell.type == "Water" and not ability_checker(row, col, current_player, "naval"):
                    info_message = "Need a navy in an adjacent cell to access water"
                    continue
                elif cell.type == "Mountains" and not ability_checker(row, col, current_player, "spec_ops"):
                    info_message = "Need spec_ops in an adjacent cell to access mountains"
                    continue
            else:
                clicked_cell = grid[row][col]
                info_message = ""

                if clicked_cell.controlled_by == current_player.name:
                    continue        

            cell.controlled_by = current_player.name

            for row in range(rows):
                for col in range(cols):
                    cell= grid[row][col]
                    if cell.controlled_by == current_player.name:
                        current_player.score += cell.resources
            
        
            current_player = take_turn(current_player)
        
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
                        info_message = f'{selected_attribute}: upgraded, at a cost of - {upgrade_cost}'
                        current_player = take_turn(current_player)
                elif event.key == K_s or event.key == K_DOWN:
                    if getattr(clicked_cell, selected_attribute) == min_val:
                        info_message = f'{selected_attribute}: Min reached'
                    else:
                        setattr(clicked_cell, selected_attribute, max(getattr(clicked_cell, selected_attribute) - 1, 0))
                        current_player.score += downgrade_benefit
                        info_message = f'{selected_attribute}: downgraded, gaining + {downgrade_benefit}'
                        current_player = take_turn(current_player)

                if event.key == K_ESCAPE:
                    clicked_cell = None
        


## PyGame visual updates
            
# Upgrade box to top right
        draw_attribute_table(screen, icons, selected_attribute)


# drawing grid and values etc
        
        for row in range(rows):
            for col in range(cols):
                cell = grid[row][col]
                new_color_value = min(cell.resources * 2.5, 255)
                pygame.draw.rect(screen, (0,new_color_value, 0), (col * cell_size, row * cell_size, cell_size, cell_size))
                # arguments: surface, color (shade of green in accordance to the resources available), then (x coordinate at top left corner, y coordinate at top left corner, width, height)

                player_color = player1.color if cell.controlled_by == "P1" else player2.color

                if cell == clicked_cell:
                    pygame.draw.rect(screen, current_cell_color, (col * cell_size, row * cell_size, cell_size, cell_size))

                elif isinstance(cell, HQ):
                    pygame.draw.rect(screen, BLACK, (col * cell_size, row * cell_size, cell_size, cell_size)) # drawn rectangle i.e. border, top left coordinates, top right then width, height
                    pygame.draw.rect(screen, player_color, (col * cell_size + 2, row * cell_size + 2, cell_size - 4, cell_size - 4)) # filled rectangle, starting + 2 on each axis then -4 on width and length to keep it within the square

                elif isinstance(cell, Terrain):
                    if cell.controlled_by == "":
                        pygame.draw.rect(screen, cell.color, (col * cell_size, row * cell_size, cell_size, cell_size))
                    else:
                        pygame.draw.rect(screen, player_color, (col * cell_size, row * cell_size, cell_size, cell_size))
                        pygame.draw.rect(screen, cell.color, (col * cell_size + 2, row * cell_size + 2, cell_size - 4, cell_size - 4))
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


        # whose turn is it message
        turn_text = f"player 1's round, {current_player.turns} moves left" if current_player.name == "P1" else f"player 2's round, {current_player.turns} moves left"
        turn_message = title_font.render(f"{turn_text}", True, WHITE)
        turn_text_rect = turn_message.get_rect()

        rect_x = (grid_size * cell_size - turn_text_rect.width) // 2
        rect_y = grid_size * cell_size + 10
        rect_width = turn_text_rect.width + 20
        rect_height = turn_text_rect.height + 20
        COLOR = BLUE if current_player.name == "P1" else RED

        pygame.draw.rect(screen, COLOR, (rect_x, rect_y, rect_width, rect_height))
        screen.blit(turn_message, (rect_x + 10, rect_y + 10))
        
        # player 1 stats
        pygame.draw.rect(screen, LIGHT_GRAY, (0, grid_size * cell_size + 60, grid_size * cell_size // 2, 80))
        player1_lines = [
        "Player 1:",
        f"Resources: {player1.score}",
        f"Wins: {player1.wins}",
        ]

        for i, line in enumerate(player1_lines):
            line_render = title_font.render(line, True, BLUE)
            screen.blit(line_render, (80, grid_size * cell_size + 70 + i * 20))  

        # player 2 stats
        pygame.draw.rect(screen, LIGHT_GRAY, (grid_size * cell_size // 2, grid_size * cell_size + 60, grid_size * cell_size // 2, 80))
        player2_lines = [
        "Player 2:",
        f"Resources: {player2.score}",
        f"Wins: {player2.wins}",
        ]

        for i, line in enumerate(player2_lines):
            line_render = title_font.render(line, True, RED)
            screen.blit(line_render, (grid_size * cell_size // 2 + 80, grid_size * cell_size + 70 + i * 20))             
        
        # info_message (for upgrades etc)
            
        pygame.draw.rect(screen, WHITE, (0, grid_size * cell_size + 150, grid_size * cell_size, 35))

        if info_message is not None:
            pygame.draw.rect(screen, current_cell_color, (0, grid_size * cell_size + 150, grid_size * cell_size, 35))
            if ":" in info_message:
                selected_attribute = info_message.split(":")[0]
                if icons[selected_attribute]:
                    icon = icons[selected_attribute]
                    max_height = title_font.get_height()
                    if icon.get_height() > max_height:
                        icon = pygame.transform.scale(icon, (int(icon.get_width() * max_height / icon.get_height()), max_height))
                        screen.blit(icon, (grid_size * cell_size + 10, y))
                    screen.blit(icon, (20, grid_size * cell_size + 160))
                    text = title_font.render(info_message, True, BLACK)
                    screen.blit(text, (50, grid_size * cell_size + 160))
            elif info_message == "":
                pygame.draw.rect(screen, WHITE, (0, grid_size * cell_size + 150, grid_size * cell_size, 35))
            else:
                text = title_font.render(info_message, True, BLACK)
                screen.blit(text, (40, grid_size * cell_size + 160))


    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()

