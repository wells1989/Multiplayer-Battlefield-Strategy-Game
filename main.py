# refactored / separated code, to do: change main function / mini functions within it (cleaner / less code?) and scrolling / screen shrinking??
import pygame
from pygame.locals import *
import sys
from media.media import icons, sounds
from globals.constants import title_font, font
from globals.classes import HQ, Terrain
from utils.game_setup import start_game, generate_game_variables, reset_game
from utils.game_logic import is_touching, ability_checker, take_turn, battle, last_survivor, update_scores, check_sound, update_info_message, battle_lost, battle_won
from utils.game_display import pygame_setup, game_choices, display_rules_popup
from utils.event_handlers import handle_key_event


def mute_event_handler(sound_active, info_message):
    sound_active = False if sound_active == True else True
    info_message = "Game muted" if sound_active == False else "Game unmuted"

    return sound_active, info_message

## Main game loop

player_count, grid_window, screen_size, grid_size = game_choices()

water_cell_color, desert_cell_color, mountains_cell_color, current_cell_color, player1, player2, player3, player4, players, selected_attribute, attribute_values, sound_active = generate_game_variables(player_count)

grid, screen, cols, rows, grid_size, running, current_player, clicked_cell, info_message, game_active, cell_size = start_game(players, grid_window, screen_size, grid_size)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Click events
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            row = event.pos[1] // cell_size 
            col = event.pos[0] // cell_size

            # Restart game button
            restart_button = pygame.Rect(grid_size * cell_size + 5, grid_size * cell_size + 10, cell_size - 10, 40)
            if restart_button.collidepoint(event.pos):
                grid, screen, cols, rows, grid_size, running, current_player, clicked_cell, info_message, game_active, cell_size = start_game(players, grid_window, screen_size, grid_size)
                continue
            
            # View Rules button
            rules_button = pygame.Rect(cell_size * grid_size + cell_size + 5, grid_size * cell_size + 10, cell_size-10, 40)
            if rules_button.collidepoint(event.pos):
                # reset game button, returns True from display_rules_popup with new player count
                if display_rules_popup(screen_size):
                    player_count, grid_window, screen_size, grid_size, water_cell_color, desert_cell_color, mountains_cell_color, current_cell_color, player1, player2, player3, player4, players, selected_attribute,attribute_values, sound_active, grid, screen, rows, cols, running, current_player, clicked_cell, info_message, game_active, cell_size = reset_game(game_choices)
                    continue

            # mute / unmute button
            mute_button = pygame.Rect((cell_size * (grid_size - 1) + 60, grid_size * cell_size + 5, 40, 40))
            if mute_button.collidepoint(event.pos):
                sound_active, info_message = mute_event_handler(sound_active, info_message)
                continue

            # if game has been won ...
            if not game_active:
                info_message = "Game not active, please start new game"
                continue

            # info / error message control
            info_message = ""
            if 0 <= row < grid_size and 0 <= col < grid_size:
                cell = grid[row][col]
            else:
                info_message = update_info_message(info_message, "Clicked outside grid", sound_active, sounds)
                continue

            if not is_touching(row, col, current_player, grid, grid_size) and cell.controlled_by != current_player.name:
                info_message = update_info_message(info_message, "Need to click on touching cells", sound_active, sounds)
                continue
            elif isinstance(cell, Terrain) and cell.controlled_by == "":
                if cell.type == "Water" and not ability_checker(row, col, current_player, "naval", grid, grid_size):
                    info_message = update_info_message(info_message, "Need a navy to access water", sound_active, sounds)
                    continue
                elif cell.type == "Mountains" and not ability_checker(row, col, current_player, "spec_ops", grid, grid_size):
                    info_message = update_info_message(info_message, "Need spec_ops to access mountains", sound_active, sounds)
                    continue
            elif cell.controlled_by and cell.controlled_by != current_player.name:
                if isinstance(cell, Terrain) and cell.type == "Water" and not ability_checker(row, col, current_player, "naval", grid, grid_size):
                    info_message = update_info_message(info_message, "Need a navy to Attack water", sound_active, sounds)
                    continue
                elif isinstance(cell, Terrain) and cell.type == "Mountains" and not ability_checker(row, col, current_player, "spec_ops", grid, grid_size):
                    info_message = update_info_message(info_message, "Need spec_ops to Attack mountains", sound_active, sounds)
                    continue

                # Battle logic
                else:
                    check_sound(sounds, "battle", sound_active)
                    defending_player = next((player for player in players if player.name == cell.controlled_by), None)
                    if battle(grid, row, col, current_player, players, rows, cols, grid_size, defending_player) == "attacker won":
                        game_active, info_message, clicked_cell, current_player = battle_won(cell, players, defending_player, clicked_cell, current_player, check_sound, sounds, sound_active, game_active, update_scores, take_turn, info_message, grid, rows, cols, row, col)
                        continue
                    elif battle(grid, row, col, current_player, players, rows, cols, grid_size, defending_player) == "stalemate, new round":
                        info_message, clicked_cell, current_player = battle_lost("stalemate, changing player", clicked_cell, current_player, grid, rows, cols, players, update_scores, take_turn)
                        continue
                    else:
                        info_message, clicked_cell, current_player = battle_lost("attack failed, changing player", clicked_cell, current_player, grid, rows, cols, players, update_scores, take_turn) 
                        continue

            # normal cell clicking functionality    
            else:
                clicked_cell = grid[row][col]
                check_sound(sounds, "pop", sound_active)
                info_message = ""

                # allowing for updates on an already controlled cell
                if clicked_cell.controlled_by == current_player.name:
                    continue
            
            # else, taking control of the cell and switching players / updating scores ...
            cell.controlled_by = current_player.name

            current_player, clicked_cell = take_turn(players, current_player, update_scores, grid, rows, cols, clicked_cell)
        

        # key events (on already controlled cells)
        elif event.type == KEYDOWN:
            if event.key in (K_u, K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_w, K_UP, K_s, K_DOWN, K_ESCAPE):
                selected_attribute, clicked_cell, current_player, info_message = handle_key_event(selected_attribute, clicked_cell, current_player, event, attribute_values, take_turn, players, update_scores, grid, rows, cols, check_sound, sounds, sound_active)
            else:
                pass

## PyGame visual updates
        pygame_setup(screen, icons, current_player, title_font, font, player1, player2, player3, player4, grid_size, cell_size, rows, cols, grid, sound_active, info_message, current_cell_color, attribute_values, players, clicked_cell)
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
