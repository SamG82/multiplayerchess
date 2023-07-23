import pygame
from game import Game

screen_size = (1200, 800)

pygame.init()
screen = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()
pygame.display.set_caption("Chess")

screen.fill("white")

game_board = Game(screen)
game_board.draw_grid()
game_board.draw_pieces()

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False


    pygame.display.flip()

    clock.tick(60)

pygame.quit()
