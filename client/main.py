import pygame
pygame.init()

import drawer
from game import Game
from chess import Board
from network import Client
    
screen_size = (1200, 800)

screen = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()
pygame.display.set_caption("Chess")

screen.fill("white")

c = Client("127.0.0.1", 3000)
c.connect()
side = c.request_game()

menu = drawer.MenuDrawer(screen)
menu.message_popup("Waiting for opponent", 400, 250)

chess_board = Board()
game_drawer = drawer.ChessDrawer(screen, side)
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
