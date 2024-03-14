"""
    restart_button = pygame.Rect(grid_size * cell_size // 2 + 10, grid_size * cell_size + 170, 155, 34)
    if restart_button.collidepoint(event.pos):
        grid_size, cell_size, window_size, grid, window, player1_score, player2_score, player1_break_cards, player2_break_cards, chance_turn, player1_turn, warning_message, winning_message, BLACK, RED, BLUE, GRAY, GREEN, WHITE, extra_turn, running, game_active, font, alt_font, menu_font = generate_game_variables() 
        continue

                    # restart button if there is no winning_message (i.e. mid-game)
    if not winning_message:
        restart_text = "Restart"
        restart_message = font.render(f"{restart_text}", True, BLACK)
        restart_text_rect = restart_message.get_rect()
        pygame.draw.rect(window, BLUE, (grid_size * cell_size // 2 + 10, grid_size * cell_size + 170, rules_text_rect.width, restart_text_rect.height + 10))

        window.blit(restart_message, (grid_size * cell_size // 2 + 30 , grid_size * cell_size + 175))


"""

"""
upgrade_button = pygame.Rect(grid_size * cell_size + 5, cell_size * 3, cell_size * 2 - 10, cell_size * 2)
            if upgrade_button.collidepoint(event.pos):
                print("upgrade button clicked")
                continue
            """