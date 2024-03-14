from globals.classes import Terrain, HQ


# function to collect values from all cells surrounded the cell clicked_on
def get_surrounding_cells(row, col, grid, grid_size):
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


# uses the get_surrounding_cells to check the player has a touching cell
def is_touching(row, col, player, grid, grid_size):
    surrounding_cells = get_surrounding_cells(row, col, grid, grid_size)

    for direction, cell in surrounding_cells.items():
        if cell is not None and player.name == cell.controlled_by:
            return True
        
    return False


# uses the get_surrounding_cells to check the player has a touching cell with the required ability
def ability_checker(row, col, player, ability, grid, grid_size):
    surrounding_cells = get_surrounding_cells(row, col, grid, grid_size)

    for cell in surrounding_cells.values():
        if cell is not None and cell.controlled_by == player.name and getattr(cell, ability) > 0:
            return True
    
    return False


# switches player, giving new player 3 turns
def switch_player(players, old_current_player):

    index = players.index(old_current_player)

    new_index = (index + 1) % len(players)
    current_player = players[new_index]

    current_player.turns = 3

    return current_player


# takes turn for current player and switches if necessary
def take_turn(players, current_player, update_scores, grid, rows, cols, clicked_cell):

    if current_player.turns == 1:
        update_scores(grid, rows, cols, current_player)
        clicked_cell = None
    
    current_player.turn()

    if current_player.turns == 0:
        current_player = switch_player(players, current_player)

        while current_player.defeated:
            current_player = switch_player(players, current_player)
        return current_player, clicked_cell
    
    return current_player, clicked_cell


# when a player clicks on an enemy position, either taking it over or creating a stalemate / loss
def battle(grid, row, col, attacking_player, players, rows, cols, grid_size, defending_player):
    defending_cell = grid[row][col]

    defending_cell_power = defending_cell.HP + defending_cell.air_defense
    if isinstance(defending_cell, Terrain):
        defending_cell_power *= defending_cell.advantage

    surrounding_cells = get_surrounding_cells(row, col, grid, grid_size)

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
            print("most powerful adjacent cell: ", attacking_power_totals[-1])
            total_power += attacking_power_totals.pop()
            attacking_cells -= 1

        print(f'attacking cell with combined power: {total_power} vs defending cell: {defending_cell_power}')

    if total_power > defending_cell_power:
        if isinstance(defending_cell, HQ):
            defending_player.defeated = True
            takeover(attacking_player, defending_player, grid, rows, cols)
        return "attacker won"
    elif total_power == defending_cell_power:
        return "stalemate, new round"
    else:
        return "defender won, new round"


# when a battle is won, updating scores and possible taking over of enemy cells
def battle_won(cell, players, defending_player, clicked_cell, current_player, check_sound, sounds, sound_active, game_active, update_scores, take_turn, info_message, grid, rows, cols, row, col):
    attacking_player = current_player
    clicked_cell = grid[row][col]
    if isinstance(cell, HQ):
        info_message = f'player {defending_player.name} eliminated by {attacking_player.name}'
        cell.controlled_by = current_player.name
        check_sound(sounds, "HQ_down", sound_active)
        if last_survivor(current_player, players):
            info_message = f'winner =  {current_player.name}'
            current_player.wins += 1
            game_active = False
            return game_active, info_message, clicked_cell, current_player
        else:
            current_player, clicked_cell = take_turn(players, current_player, update_scores, grid, rows, cols, clicked_cell)
            return game_active, info_message, clicked_cell, current_player
    else:
        info_message = "Attacker won the battle"
        cell.controlled_by = current_player.name
        current_player, clicked_cell = take_turn(players, current_player, update_scores, grid, rows, cols, clicked_cell)
        return game_active, info_message, clicked_cell, current_player


# when a battle is lost, adding up score then switching player
def battle_lost(loss_message, clicked_cell, current_player, grid, rows, cols, players, update_scores, take_turn):
    info_message = loss_message
    clicked_cell = None
    current_player.turns = 0
    update_scores(grid, rows, cols, current_player)
    current_player, clicked_cell = take_turn(players, current_player, update_scores, grid, rows, cols, clicked_cell)

    return info_message, clicked_cell, current_player


# when a player takes an enemy HQ, also captures all of the enemy positions
def takeover(attacking_player, defending_player, grid, rows, cols):
    for row in range(rows):
        for col in range(cols):
            cell = grid[row][col]
            if cell.controlled_by == defending_player.name:
                cell.controlled_by = attacking_player.name


# boolean check to see if there are other undefeated players
def last_survivor(current_player, players):
    active_players = [player for player in players if player.name != current_player.name and player.defeated == False]

    return False if active_players else True


# at the end of a turn the grid is checked and players get resources from their controlled cells
def update_scores(grid, rows, cols, current_player):
    for row in range(rows):
        for col in range(cols):
            cell= grid[row][col]
            if cell.controlled_by == current_player.name:
                current_player.score += cell.resources


# allows for sounds based on sound_active boolean
def check_sound(sounds, sound, sound_active):
    return sounds[sound].play() if sound_active else None


# updating info_message along with possible sound alert
def update_info_message(info_message, string, sound_active, sounds):
    info_message = string
    if info_message:
        check_sound(sounds, "info", sound_active)
    return info_message
