import pygame
from game import Game
from drawer import Drawer
from chess import Board

screen_size = (1200, 800)

pygame.init()
screen = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()
pygame.display.set_caption("Chess")

screen.fill("white")

chess_board = Board()
game_drawer = Drawer(screen, "white")
game_controller = Game(chess_board, game_drawer)

run = True
while run:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONUP:
            mouse_pos = pygame.mouse.get_pos()
            game_controller.handle_click_test(mouse_pos)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
