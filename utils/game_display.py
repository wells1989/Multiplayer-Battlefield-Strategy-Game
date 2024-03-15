import pygame
from globals.constants import WHITE, BLACK, BLUE, font, title_font, LIGHT_GRAY, GREEN
from globals.classes import Terrain, HQ


# main pygame drawing function
def pygame_setup(screen, icons, current_player, title_font, font, player1, player2, player3, player4, grid_size, cell_size, rows, cols, grid, sound_active, info_message, current_cell_color, attribute_values, players, clicked_cell):
    draw_attribute_table(screen, icons, attribute_values, grid_size, cell_size)
    draw_extra_buttons(current_player, title_font, players, grid_size, cell_size, icons, screen, sound_active, info_message, current_cell_color)
    draw_grid(rows, cols, grid, player1, player2, player3, player4, cell_size, title_font, font, icons, screen, current_cell_color, clicked_cell)


# drawing the upgrades table from the icons and selected_attributes
def draw_attribute_table(screen, icons, attribute_values, grid_size, cell_size):
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


# run on program entry, player selects number of players and screen size etc based off that
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

        button_rect = pygame.draw.rect(screen, WHITE, (x, y + 50, text_rect.width + 20, text_rect.height + 20))
        buttons.append((button_rect, i))
        screen.blit(options_message, (x + 10, y + 60))
        x += 170

    player_count = None
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
                        if player_count == 2: # REFAC
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
                        pygame.display.set_caption("Battlefield Game")
                        screen.fill(WHITE)
                        waiting_for_input = False
                        return player_count, grid_window, screen_size, grid_size

        pygame.display.flip()


# view of showing rules, and options for players to reset the game (e.g. starting over with a new number of players)
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


# drawing player buttons (right side)
def draw_extra_buttons(current_player, title_font, players, grid_size, cell_size, icons, screen, sound_active, info_message, current_cell_color):
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

        rect_height = replay_text_rect.height + 20

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


# drawing main grid
def draw_grid(rows, cols, grid, player1, player2, player3, player4, cell_size, title_font, font, icons, screen, current_cell_color, clicked_cell):
    for row in range(rows):
        for col in range(cols):
            cell = grid[row][col]
            new_color_value = min(cell.resources * 2.5, 255)
            pygame.draw.rect(screen, (0,new_color_value, 0), (col * cell_size, row * cell_size, cell_size, cell_size))

            player_colors = {
                "P1": player1.color,
                "P2": player2.color,
                "P3": player3.color,
                "P4": player4.color,
            }

            player_color = player_colors.get(cell.controlled_by)

            if cell == clicked_cell:
                pygame.draw.rect(screen, player_color, (col * cell_size, row * cell_size, cell_size, cell_size))
                pygame.draw.rect(screen, current_cell_color, (col * cell_size + 4, row * cell_size + 4, cell_size - 8, cell_size - 8))

            elif isinstance(cell, HQ):
                pygame.draw.rect(screen, BLACK, (col * cell_size, row * cell_size, cell_size, cell_size))
                pygame.draw.rect(screen, player_color, (col * cell_size + 4, row * cell_size + 4, cell_size - 8, cell_size - 8)) 

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
