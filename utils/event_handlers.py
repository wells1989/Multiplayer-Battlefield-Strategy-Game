import pygame
from pygame.locals import *
from globals.classes import Terrain

# Handling key presses on cells
def handle_key_event(selected_attribute, clicked_cell, current_player, event, attribute_values, take_turn, players, update_scores, grid, rows, cols, check_sound, sounds, sound_active):
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
        
        min_val, max_val, upgrade_cost, downgrade_benefit = attribute_values[selected_attribute]
        
        # Handling upgrade logic
        if event.key == K_w or event.key == K_UP:
            if getattr(clicked_cell, selected_attribute) == max_val:
                info_message = f'{selected_attribute}: Max reached'
            elif upgrade_cost > current_player.score:
                info_message = f'{selected_attribute}: Unable to upgrade, curr resources = {current_player.score}'
                pass
            else:
                setattr(clicked_cell, selected_attribute, getattr(clicked_cell, selected_attribute) + 1)
                current_player.score -= upgrade_cost
                info_message = f'{selected_attribute}: upgraded: - {upgrade_cost} resources'
                current_player, clicked_cell = take_turn(players, current_player, update_scores, grid, rows, cols, clicked_cell)
        
        # Handling downgrade logic
        elif event.key == K_s or event.key == K_DOWN:
            if getattr(clicked_cell, selected_attribute) == min_val:
                info_message = f'{selected_attribute}: Min reached'
            else:
                setattr(clicked_cell, selected_attribute, max(getattr(clicked_cell, selected_attribute) - 1, 0))
                current_player.score += downgrade_benefit
                info_message = f'{selected_attribute}: downgraded: + {downgrade_benefit} resources'
                current_player, clicked_cell = take_turn(players, current_player, update_scores, grid, rows, cols, clicked_cell)

        if event.key == K_ESCAPE:
            clicked_cell = None

        if info_message:
            check_sound(sounds, "info", sound_active)

        return selected_attribute, clicked_cell, current_player, info_message
    
    else:
        return selected_attribute, clicked_cell, current_player, info_message

# handling pygame Quit
def handle_quit_event(event):
   return False if event.type == pygame.QUIT else True


# Handling the on screen buttons
def buttons_event_handler(game_active, event, mute_event_handler, grid_size, cell_size, start_game, players, grid_window, screen_size, display_rules_popup, reset_game, game_choices, sound_active, info_message, grid):
    restart_button = pygame.Rect(grid_size * cell_size + 5, grid_size * cell_size + 10, cell_size - 10, 40)
    if restart_button.collidepoint(event.pos):
        return "restart"
    
    # View Rules button
    rules_button = pygame.Rect(cell_size * grid_size + cell_size + 5, grid_size * cell_size + 10, cell_size-10, 40)
    if rules_button.collidepoint(event.pos):
        # reset game button, returns True from display_rules_popup with new player count
        if display_rules_popup(screen_size):
            return "reset"

    # mute / unmute button
    mute_button = pygame.Rect((cell_size * (grid_size - 1) + 60, grid_size * cell_size + 5, 40, 40))
    if mute_button.collidepoint(event.pos):
        return "mute"
    
    if not game_active:
        return "inactive_game"
    

# Handling cell_click events
def handle_cell_clicks(row, col, grid, grid_size, cell_size, update_info_message, sound_active, sounds, is_touching, current_player, ability_checker, info_message, players, rows, cols, battle, check_sound, battle_won, battle_lost, update_scores, take_turn):
    info_message = ""
    if 0 <= row < grid_size and 0 <= col < grid_size:
        cell = grid[row][col]
    else:
        return "error", "Clicked outside grid"

    if not is_touching(row, col, current_player, grid, grid_size) and cell.controlled_by != current_player.name:
        return "error", "Need to click on touching cells"

    elif isinstance(cell, Terrain) and cell.controlled_by == "":
        if cell.type == "Water" and not ability_checker(row, col, current_player, "naval", grid, grid_size):
            return "error", "Need a navy to access water"
  
        elif cell.type == "Mountains" and not ability_checker(row, col, current_player, "spec_ops", grid, grid_size):
            return "error", "Need spec_ops to access mountains"
   
    elif cell.controlled_by and cell.controlled_by != current_player.name:
        if isinstance(cell, Terrain) and cell.type == "Water" and not ability_checker(row, col, current_player, "naval", grid, grid_size):
            return "error", "Need a navy to Attack water"
  
        elif isinstance(cell, Terrain) and cell.type == "Mountains" and not ability_checker(row, col, current_player, "spec_ops", grid, grid_size):
            return "error", "Need spec_ops to Attack mountains"
 
        # Battle logic
        else:
            check_sound(sounds, "battle", sound_active)
            defending_player = next((player for player in players if player.name == cell.controlled_by), None)
            if battle(grid, row, col, current_player, players, rows, cols, grid_size, defending_player) == "attacker won":
                return "attacker won", cell, defending_player

            elif battle(grid, row, col, current_player, players, rows, cols, grid_size, defending_player) == "stalemate, new round":
                return "stalemate"
 
            else:
                return "attack failed"

    # normal cell clicking functionality    
    else:
        return None
