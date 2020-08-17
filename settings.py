import pygame

# There are all game and engine settings

# Main settings
SIZE_WINDOW = (1024, 650)
DEFAULT_COLOR = (102, 153, 255)
SIZE_TILE = 16
FPS = 120

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (125, 125, 125)
GOLD = (255, 223, 0)

# Wall
WALL_IMG = "img/PNG/Tiles/tile_44.png"

# Player
PLAYER_SPEED = 200
DIAGONAL_COEFFICIENT = 0.7
PLAYER_IMG = "img/PNG/Hitman 1/hitman1_gun.png"
ROTATION_SPEED = 100
CALL_DOWN_SHOT = 100
PLAYER_HIT_BOX = pygame.rect.Rect(0, 0, 30, 30)

# Mob
MOB_IMG = "img/PNG/Zombie 1/zoimbie1_hold.png"
MOB_SPEED = 40
MOB_HIT_BOX = pygame.rect.Rect(0, 0, 30, 30)

# Bullet
BULLET_LIFETIME = 1000
BULLET_SPEED = 500
