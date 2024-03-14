import pygame
from globals.classes import Terrain

def handle_click(event, current_player, cell_size, grid_size, grid, rows, cols, start_game, players, grid_window, screen_size, display_rules_popup, reset_game, game_choices, update_info_message, sounds, is_touching, ability_checker, check_sound, battle_won, battle_lost, battle, update_scores, take_turn, sound_active, game_active):
    row = event.pos[1] // cell_size 
    col = event.pos[0] // cell_size

    # Restart game button
    restart_button = pygame.Rect(grid_size * cell_size + 5, grid_size * cell_size + 10, cell_size - 10, 40)
    if restart_button.collidepoint(event.pos):
        return start_game(players, grid_window, screen_size, grid_size)
    
    # View Rules button
    rules_button = pygame.Rect(cell_size * grid_size + cell_size + 5, grid_size * cell_size + 10, cell_size-10, 40)
    if rules_button.collidepoint(event.pos):
        # reset game button, returns True from display_rules_popup with new player count
        if display_rules_popup(screen_size):
            return reset_game(game_choices)

    # mute / unmute button
    mute_button = pygame.Rect((cell_size * (grid_size - 1) + 60, grid_size * cell_size + 5, 40, 40))
    if mute_button.collidepoint(event.pos):
        sound_active = False if sound_active == True else True
        info_message = "Game muted" if sound_active == False else "Game unmuted"
        return info_message, sound_active

    # if game has been won ...
    if not game_active:
        info_message = "Game not active, please start new game"
        return info_message

    # info / error message control
    info_message = ""
    if 0 <= row < grid_size and 0 <= col < grid_size:
        cell = grid[row][col]
    else:
        info_message = update_info_message(info_message, "Clicked outside grid", sound_active, sounds)
        return info_message

    if not is_touching(row, col, current_player, grid, grid_size) and cell.controlled_by != current_player.name:
        info_message = update_info_message(info_message, "Need to click on touching cells", sound_active, sounds)
        return info_message
    elif isinstance(cell, Terrain) and cell.controlled_by == "":
        if cell.type == "Water" and not ability_checker(row, col, current_player, "naval", grid, grid_size):
            info_message = update_info_message(info_message, "Need a navy to access water", sound_active, sounds)
            return info_message
        elif cell.type == "Mountains" and not ability_checker(row, col, current_player, "spec_ops", grid, grid_size):
            info_message = update_info_message(info_message, "Need spec_ops to access mountains", sound_active, sounds)
            return info_message
    elif cell.controlled_by and cell.controlled_by != current_player.name:
        if isinstance(cell, Terrain) and cell.type == "Water" and not ability_checker(row, col, current_player, "naval", grid, grid_size):
            info_message = update_info_message(info_message, "Need a navy to Attack water", sound_active, sounds)
            return info_message
        elif isinstance(cell, Terrain) and cell.type == "Mountains" and not ability_checker(row, col, current_player, "spec_ops", grid, grid_size):
            info_message = update_info_message(info_message, "Need spec_ops to Attack mountains", sound_active, sounds)
            return info_message

        # Battle logic
        else:
            check_sound(sounds, "battle", sound_active)
            defending_player = next((player for player in players if player.name == cell.controlled_by), None)
            if battle(grid, row, col, current_player, players, rows, cols, grid_size, defending_player) == "attacker won":
                return battle_won(cell, players, defending_player, clicked_cell, current_player, check_sound, sounds, sound_active, game_active, update_scores, take_turn, info_message, grid, rows, cols, row, col)
            elif battle(grid, row, col, current_player, players, rows, cols, grid_size, defending_player) == "stalemate, new round":
                return battle_lost("stalemate, changing player", clicked_cell, current_player, grid, rows, cols, players, update_scores, take_turn)
            else:
                return battle_lost("attack failed, changing player", clicked_cell, current_player, grid, rows, cols, players, update_scores, take_turn) 

    # normal cell clicking functionality    
    else:
        clicked_cell = grid[row][col]
        check_sound(sounds, "pop", sound_active)
        info_message = ""

        # allowing for updates on an already controlled cell
        if clicked_cell.controlled_by == current_player.name:
            return
    
    # else, taking control of the cell and switching players / updating scores ...
    cell.controlled_by = current_player.name

    current_player, clicked_cell = take_turn(players, current_player, update_scores, grid, rows, cols, clicked_cell)

    return current_player, clicked_cell