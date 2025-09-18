import pygame
import os

BASE_IMG_PATH = 'data/sprites/'
BASE_SND_PATH = 'data/sounds/'

def load_image(path):
    try:
        img = pygame.image.load(BASE_IMG_PATH + path).convert()
        img.set_colorkey((0, 0, 0))
        return img
    except:
        print(f"Warning: Could not load image {BASE_IMG_PATH + path}")
        # Create a placeholder image
        surf = pygame.Surface((16, 16))
        surf.fill((255, 0, 255))  # Magenta placeholder
        return surf

def load_images(path):
    images = []
    try:
        for img_name in sorted(os.listdir(BASE_IMG_PATH + path)):
            if img_name.endswith('.png') or img_name.endswith('.jpg'):
                images.append(load_image(path + '/' + img_name))
    except FileNotFoundError:
        print(f"Warning: Could not load images from {BASE_IMG_PATH + path}")
        # Create a placeholder image
        surf = pygame.Surface((16, 16))
        surf.fill((255, 0, 255))  # Magenta placeholder
        images.append(surf)
    return images

def load_sound(path):
    try:
        return pygame.mixer.Sound(BASE_SND_PATH + path)
    except:
        print(f"Warning: Could not load sound {BASE_SND_PATH + path}")
        return None