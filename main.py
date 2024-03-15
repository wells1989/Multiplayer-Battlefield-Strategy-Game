# refactored / separated code, to do: change main function / mini functions within it (cleaner / less code?) and scrolling / screen shrinking??
import pygame
from pygame.locals import *
import sys
from media.media import icons, sounds
from globals.constants import title_font, font
from globals.classes import HQ, Terrain
from utils.game_setup import start_game, generate_game_variables, reset_game
from utils.game_logic import is_touching, ability_checker, take_turn, battle, last_survivor, update_scores, check_sound, update_info_message, battle_lost, battle_won, mute_event_handler
from utils.game_display import pygame_setup, game_choices, display_rules_popup
from utils.event_handlers import handle_key_event, handle_quit_event, buttons_event_handler, handle_cell_clicks

## Main game loop

player_count, grid_window, screen_size, grid_size = game_choices()

water_cell_color, desert_cell_color, mountains_cell_color, current_cell_color, player1, player2, player3, player4, players, selected_attribute, attribute_values, sound_active = generate_game_variables(player_count)

grid, screen, cols, rows, grid_size, running, current_player, clicked_cell, info_message, game_active, cell_size = start_game(players, grid_window, screen_size, grid_size)

while running:
    for event in pygame.event.get():
        running = handle_quit_event(event)

        # Click events
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            row = event.pos[1] // cell_size 
            col = event.pos[0] // cell_size

            # on screen buttons and inactive state
            button = buttons_event_handler(game_active, event, mute_event_handler, grid_size, cell_size, start_game, players, grid_window, screen_size, display_rules_popup, reset_game, game_choices, sound_active, info_message, grid)
            if button == "restart":
                grid, screen, cols, rows, grid_size, running, current_player, clicked_cell, info_message, game_active, cell_size = start_game(players, grid_window, screen_size, grid_size)
                continue
            elif button == "reset":
                player_count, grid_window, screen_size, grid_size, water_cell_color, desert_cell_color, mountains_cell_color, current_cell_color, player1, player2, player3, player4, players, selected_attribute,attribute_values, sound_active, grid, screen, rows, cols, running, current_player, clicked_cell, info_message, game_active, cell_size = reset_game(game_choices)
                continue
            elif button == "mute":
                sound_active, info_message = mute_event_handler(sound_active, info_message)
                continue
            elif button == "inactive_game":
                info_message = "Game not active, please start new game"
                continue
            
            # cell click functionality
            info_message = ""
            if 0 <= row < grid_size and 0 <= col < grid_size:
                cell = grid[row][col] 

            cell_click_result = handle_cell_clicks(row, col, grid, grid_size, cell_size, update_info_message, sound_active, sounds, is_touching, current_player, ability_checker, info_message, players, rows, cols, battle, check_sound, battle_won, battle_lost, update_scores, take_turn)
            if cell_click_result:
                if cell_click_result[0] == "error":
                    info_message = update_info_message(info_message, cell_click_result[1], sound_active, sounds)
                    continue
                elif cell_click_result[0] == "attacker won":
                    cell = cell_click_result[1]
                    defending_player = cell_click_result[2]
                    game_active, info_message, clicked_cell, current_player = battle_won(cell, players, defending_player, clicked_cell, current_player, check_sound, sounds, sound_active, game_active, update_scores, take_turn, info_message, grid, rows, cols, row, col)
                    continue
                elif cell_click_result == "stalemate":
                    info_message, clicked_cell, current_player = battle_lost("stalemate, changing player", clicked_cell, current_player, grid, rows, cols, players, update_scores, take_turn)
                    continue
                elif cell_click_result == "attack failed":
                    info_message, clicked_cell, current_player = battle_lost("attack failed, changing player", clicked_cell, current_player, grid, rows, cols, players, update_scores, take_turn) 
                    continue
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

## PyGame visual updates
        pygame_setup(screen, icons, current_player, title_font, font, player1, player2, player3, player4, grid_size, cell_size, rows, cols, grid, sound_active, info_message, current_cell_color, attribute_values, players, clicked_cell)
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
