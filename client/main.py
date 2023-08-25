import pygame
import threading

import drawer
from game import Game
from chess import Board
from network import Client


def main():
    screen_size = (1200, 800)

    screen = pygame.display.set_mode(screen_size)
    clock = pygame.time.Clock()
    pygame.display.set_caption("Chess")

    screen.fill("white")

    menu = drawer.MenuDrawer(screen)
    menu.message_popup("Waiting for opponent", 400, 250)

    client = Client("127.0.0.1", 3000)
    client.connect()

    # start queueing for a game
    game_req = threading.Thread(target=client.request_game, daemon=True)
    game_req.start()
    
    # wait for the thread
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        if not game_req.is_alive():
            waiting = False
    
    chess_board = Board()
    game_drawer = drawer.ChessDrawer(screen, client.side)
    game_controller = Game(chess_board, game_drawer, client)

    # start the main game loop
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONUP:
                mouse_pos = pygame.mouse.get_pos()
                game_controller.handle_click(mouse_pos)

        pygame.display.flip()

        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()