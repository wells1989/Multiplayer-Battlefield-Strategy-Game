# separate handle_click function but not working ...

def handle_click(event, cell_size, grid_size, players, grid_window, screen, screen_size, start_game, game_choices, generate_game_variables, sound_active, info_message, game_active, grid, is_touching, current_player, sounds, ability_checker, update_info_message, rows, cols, check_sound, last_survivor, update_scores, take_turn, battle):
    row = event.pos[1] // cell_size 
    col = event.pos[0] // cell_size

    restart_button = pygame.Rect(grid_size * cell_size + 5, grid_size * cell_size + 10, cell_size - 10, 40)
    if restart_button.collidepoint(event.pos):
        grid, screen, cols, rows, grid_size, running, current_player, clicked_cell, info_message, game_active, cell_size = start_game(players, grid_window, screen_size, grid_size)
        return
    
    rules_button = pygame.Rect(cell_size * grid_size + cell_size + 5, grid_size * cell_size + 10, cell_size-10, 40)
    if rules_button.collidepoint(event.pos):
        reset = display_rules_popup(screen_size)
        if reset:
            player_count, grid_window, screen_size, grid_size = game_choices()
            water_cell_color, desert_cell_color, mountains_cell_color, current_cell_color, player1, player2, player3, player4, players, selected_attribute, attribute_values, sound_active = generate_game_variables(player_count)
            grid, screen, cols, rows, grid_size, running, current_player, clicked_cell, info_message, game_active, cell_size = start_game(players, grid_window, screen_size, grid_size)
        return

    mute_button = pygame.Rect((cell_size * (grid_size - 1) + 60, grid_size * cell_size + 5, 40, 40))
    if mute_button.collidepoint(event.pos):
        sound_active = False if sound_active == True else True
        info_message = "Game muted" if sound_active == False else "Game unmuted"
        return

    if not game_active:
        info_message = "Game not active, please start new game"
        return

    info_message = ""
    if 0 <= row < grid_size and 0 <= col < grid_size:
        cell = grid[row][col]
    else:
        info_message = update_info_message(info_message, "Clicked outside grid", sound_active, sounds)
        return

    if not is_touching(row, col, current_player, grid, grid_size) and cell.controlled_by != current_player.name:
        out_of_range = True
        info_message = update_info_message(info_message, "Need to click on touching cells", sound_active, sounds)
        return
    elif isinstance(cell, Terrain) and cell.controlled_by == "":
        if cell.type == "Water" and not ability_checker(row, col, current_player, "naval", grid, grid_size):
            info_message = update_info_message(info_message, "Need a navy to access water", sound_active, sounds)
            return
        elif cell.type == "Mountains" and not ability_checker(row, col, current_player, "spec_ops", grid, grid_size):
            info_message = update_info_message(info_message, "Need spec_ops to access mountains", sound_active, sounds)
            return
    elif cell.controlled_by and cell.controlled_by != current_player.name:
        if isinstance(cell, Terrain) and cell.type == "Water" and not ability_checker(row, col, current_player, "naval", grid, grid_size):
            info_message = update_info_message(info_message, "Need a navy to Attack water", sound_active, sounds)
            return
        elif isinstance(cell, Terrain) and cell.type == "Mountains" and not ability_checker(row, col, current_player, "spec_ops", grid, grid_size):
            info_message = update_info_message(info_message, "Need spec_ops to Attack mountains", sound_active, sounds)
            return
        else:
            check_sound(sounds, "battle", sound_active)
            defending_player = next((player for player in players if player.name == cell.controlled_by), None)
            if battle(grid, row, col, current_player, players, rows, cols, grid_size) == "attacker won":
                clicked_cell = grid[row][col]
                if isinstance(cell, HQ):
                    info_message = f'player {defending_player.name} eliminated by {current_player.name}'
                    cell.controlled_by = current_player.name
                    check_sound(sounds, "HQ_down", sound_active)
                    if last_survivor(current_player, players):
                        info_message = f'winner =  {current_player.name}'
                        current_player.wins += 1
                        game_active = False
                        return
                    else:
                        if current_player.turns == 1:
                            update_scores(grid, rows, cols, current_player)
                            clicked_cell = None
                        current_player = take_turn(players, current_player)
                        return
                else:
                    info_message = "Attacker won the battle"
                    cell.controlled_by = current_player.name
                    if current_player.turns == 1:
                        update_scores(grid, rows, cols, current_player)
                        clicked_cell = None
                    current_player = take_turn(players, current_player)
                    return
                
            elif battle(grid, row, col, current_player, players, rows, cols, grid_size) == "stalemate, new round":
                info_message = "Stalemate, switching players"
                clicked_cell = None
                current_player.turns = 0
                update_scores(grid, rows, cols, current_player)
                current_player = take_turn(players, current_player)
                return

            else:
                info_message = "attack failed, switching players"
                clicked_cell = None
                current_player.turns = 0
                update_scores(grid, rows, cols, current_player)
                current_player = take_turn(players, current_player)
                return
                
    else:
        clicked_cell = grid[row][col]
        check_sound(sounds, "pop", sound_active)
        info_message = ""

        if clicked_cell.controlled_by == current_player.name:
            return

    cell.controlled_by = current_player.name

    if current_player.turns == 1:
        update_scores(grid, rows, cols, current_player)
        clicked_cell = None
    current_player = take_turn(players, current_player)
        
