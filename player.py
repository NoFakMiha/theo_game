import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image= pygame.image.load("sprites/user/user_running_1.png")
        self.rect = self.image.get_rect(midbottom = (200,315))
        self.gravity = 0

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >=315:
            self.gravity -=25

    def apply_gravity(self):
        self.gravity +=1
        self.rect.y = self.gravity
        if self.rect.bottom >=315: self.rect.bottom = 315

    def update(self):
        self.player_input()
        self.apply_gravity()