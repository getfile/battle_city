import time
import pygame

pygame.init()
surface = pygame.display.set_mode([400, 400])
tank = pygame.Surface((16, 16), pygame.SRCALPHA)
# print("tank", tank.get_alpha())
img = pygame.image.load("resources/Sprites.png").convert_alpha()
# print("img", img.get_alpha())
# img.convert_alpha()
tank.blit(img, (-128, -128))
# print("tank", tank.get_alpha())
tank = pygame.transform.scale(tank, (32, 32))
surface.fill(pygame.Color(255, 0, 0))
surface.blit(tank, (100, 100))

pygame.display.flip()
time.sleep(1)
