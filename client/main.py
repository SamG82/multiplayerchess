import pygame

import drawer
from network import Client
from game import Game

def main():
    screen_size = (1200, 800)

    screen = pygame.display.set_mode(screen_size)
    clock = pygame.time.Clock()
    pygame.display.set_caption("Chess")

    screen.fill("white")
    menu = drawer.MenuDrawer(screen)
    menu.message_popup("Waiting for opponent", 400, 250)
    pygame.display.flip()

    client = Client("127.0.0.1", 3000)
    client.connect()
    game_request = client.request_game()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False

        if not game_request.is_alive():
            waiting = False

    # pass the drawer and client into game and start
    board_drawer = drawer.BoardDrawer(screen, client.color)
    game = Game(client, board_drawer)
    game.start()

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                      
            elif event.type == pygame.MOUSEBUTTONDOWN:
               game.handle_click(pygame.mouse.get_pos())

        if game.winner:
            menu.message_popup(
                    f"{game.winner} wins by {game.conclude_reason}.",
                    450,
                    140
                )
        else:
            board_drawer.draw()

        clock.tick(60)
        pygame.display.flip()

if __name__ == "__main__":
    main()