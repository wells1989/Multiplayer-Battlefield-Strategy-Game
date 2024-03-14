from pygame.locals import *

def handle_key_event(selected_attribute, clicked_cell, current_player, event, attribute_values, take_turn, players, update_scores, grid, rows, cols, check_sound, sounds, sound_active):
    info_message = ""
    if clicked_cell is not None and clicked_cell.controlled_by == current_player.name:
        print(selected_attribute)
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