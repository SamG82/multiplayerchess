import pygame
from game import Game

screen_size = (1200, 800)

pygame.init()
screen = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()
pygame.display.set_caption("Chess")

screen.fill("white")

game_board = Game(screen)

run = True
while run:
    game_board.draw_squares()
    game_board.draw_pieces()
    game_board.draw_markers()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONUP:
            mouse_pos = pygame.mouse.get_pos()
            game_board.handle_click(mouse_pos)
    

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
