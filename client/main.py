import pygame

import drawer
from network import Client
from thread import threaded

def get_clicked(mouse_pos, square_map):
    for name, rect in square_map.items():
        if rect.collidepoint(mouse_pos):
            return name
        
    return None

@threaded
def update_board_positions(client, board_drawer):
    while True:
        board_data = client.board_updates.get()
        board_drawer.piece_positions = board_data

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
    game_request = client.request_game()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False

        if not game_request.is_alive():
            waiting = False

    board_drawer = drawer.BoardDrawer(screen, client.side)
    client.listen()
    update_board_positions(client, board_drawer)

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                
                if board_drawer.selected_square:
                    clicked_square = get_clicked(mouse_pos, board_drawer.squares)

                    # unseleted the square if it was clicked again
                    if clicked_square == board_drawer.selected_square:
                        board_drawer.selected_square = None
                        continue

                    clicked_piece = board_drawer.piece_positions.get(clicked_square)
                    enemy_piece_clicked = clicked_piece and clicked_piece[0] != board_drawer.perspective

                    
                    selected_piece = board_drawer.piece_positions.get(board_drawer.selected_square)
                    if clicked_square and ("1" in clicked_square or "8" in clicked_square) and selected_piece == client.side+'p':
                        choice_rects = board_drawer.draw_promotion_prompt()
                        pygame.display.flip()

                        unanswered = True
                        while unanswered:
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    run = False
                                    unanswered = False

                                if event.type == pygame.MOUSEBUTTONDOWN:
                                    mouse_pos = pygame.mouse.get_pos()
                                    for option, rect in choice_rects.items():
                                        if rect.collidepoint(mouse_pos):
                                            client.send_move(f"{board_drawer.selected_square}{clicked_square}{option}")
                                            unanswered = False
                                
                    # if an enemy piece was clicked or no piece was clicked, attempt a move
                    if enemy_piece_clicked or not clicked_piece:
                        client.send_move(f"{board_drawer.selected_square}{clicked_square}")
                        board_drawer.selected_square = None


                clicked_piece_position = get_clicked(mouse_pos, board_drawer.pieces)
                clicked_piece_side = board_drawer.piece_positions.get(clicked_piece_position, '0')[0]
                
                if clicked_piece_side == board_drawer.perspective:
                    board_drawer.selected_square = clicked_piece_position


        clock.tick(60)
        board_drawer.draw_board()
        pygame.display.flip()

if __name__ == "__main__":
    main()