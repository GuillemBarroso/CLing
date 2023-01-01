import pygame
from pygame.locals import *

class Player():
    def __init__(self, x, y, image):
        self.velocity = 5
        self.x = x
        self.y = y
        self.image = image
        self.direction = "N"

    def move(self):
        # Storing the key pressed using key.get_pressed() method
        key_pressed_is = pygame.key.get_pressed()

        # Changing the coordinates of the player
        if key_pressed_is[K_LEFT]:
            self.x -= self.velocity
        if key_pressed_is[K_RIGHT]:
            self.x += self.velocity
        if key_pressed_is[K_UP]:
            self.y -= self.velocity
        if key_pressed_is[K_DOWN]:
            self.y += self.velocity

    def draw(self, canvas, direction):
        self.direction = direction
        if self.direction == "N":
            canvas.blit(self.image, (self.x, self.y))
        elif self.direction == "W":
            canvas.blit(pygame.transform.rotate(self.image, 90), (self.x, self.y))
        elif self.direction == "E":
            canvas.blit(pygame.transform.rotate(self.image, -90), (self.x, self.y))
        elif self.direction == "S":
            canvas.blit(pygame.transform.flip(self.image, True, True), (self.x, self.y))
        elif self.direction == "NE":
            canvas.blit(pygame.transform.rotate(self.image, -45), (self.x, self.y))
