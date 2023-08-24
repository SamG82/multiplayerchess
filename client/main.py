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

    c = Client("127.0.0.1", 3000)
    c.connect()
    result_store = {}

    # start queueing for a game
    game_req = threading.Thread(target=c.request_game, args=(result_store,), daemon=True)
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
    game_drawer = drawer.ChessDrawer(screen, result_store["side"])
    game_controller = Game(chess_board, game_drawer)

    # start the main game loop
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

if __name__ == "__main__":
    main()