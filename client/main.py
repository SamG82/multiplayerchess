import pygame


pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()

run = True

while run:
    pygame.display.flip()

    clock.tick(60)


pygame.quit()
