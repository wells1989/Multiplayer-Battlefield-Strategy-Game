import pygame

## media files

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

mute_icon = pygame.image.load("media/images/muted_icon.png")
unmute_icon = pygame.image.load("media/images/unmuted_icon.png")

icons = {
    "Resources": resources_symbol,
    "HP": hp_symbol,
    "damage": damage_symbol,
    "comms": comms_symbol,
    "naval": naval_symbol,
    "spec_ops": spec_ops_symbol,
    "air_attack": air_attack_symbol,
    "air_defense": air_defense_symbol,
    "Upgrade": plus_symbol_icon,
    "mute": mute_icon,
    "un_mute": unmute_icon,
}

# sounds

import os
pygame.mixer.init()

# Set up the paths to the sound files (e.g. effects_directory would be root directory i.e. chaser.effects

# then win_sound_path would be chaser.effects.win
current_directory = os.path.dirname(__file__)
effects_directory = os.path.join(current_directory, 'sounds')
pop_sound_path = os.path.join(effects_directory, 'pop.mp3')
battle_sound_path = os.path.join(effects_directory, 'battle.mp3')
HQ_down_sound_path = os.path.join(effects_directory, 'HQ_down.mp3')
info_sound_path = os.path.join(effects_directory, 'info.mp3')

#sounds 
sounds = {
    "pop": pygame.mixer.Sound(pop_sound_path),
    "battle": pygame.mixer.Sound(battle_sound_path),
    "HQ_down": pygame.mixer.Sound(HQ_down_sound_path),
    "info": pygame.mixer.Sound(info_sound_path)
}