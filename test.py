import pygame
import os
# Absolute path to the media directory
absolute_media_directory = r"C:\Users\wells\Desktop\Documents\Programming\Projects\nucamp\battlegame\media"

# Initialize Pygame
pygame.init()

# Load an image
image_path = os.path.join(absolute_media_directory, "images", "resources_icon.png")
resources_icon = pygame.image.load(image_path)
