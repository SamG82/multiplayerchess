from thread import threaded
from network import Action
import pygame
from typing import Literal

# gets the clicked name of a rect from a dictionary
def get_clicked(mouse_pos, rect_map):
    for name, rect in rect_map.items():
        if rect.collidepoint(mouse_pos):
            return name
        
    return None

# connects client and drawer, manages click events
class Game:
    def __init__(self, client, board_drawer):
        self.client = client
        self.drawer = board_drawer
        self.winner = None
        self.conclude_reason = None

    @threaded
    def update_from_client(self):
        while True:
            message = self.client.messages.get()
            if message.action == Action.START_GAME:
                self.drawer.piece_locations = message.data["board"]
            elif message.action == Action.UPDATE_BOARD:
                self.drawer.piece_locations = message.data
            elif message.action == Action.CONCLUDE:
                self.winner = message.data["winner"]
                self.conclude_reason = message.data["reason"]

    # shows a promotion prompt and waits for a response
    def handle_promotion(self) -> Literal["q", "r", "b", "n"]:
        choice_rects = self.drawer.draw_promotion_prompt()
        pygame.display.flip()

        # show prompt and block until answered
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    choice = get_clicked(mouse_pos, choice_rects)

                    return choice
                
    def start(self):
        self.client.listen()
        self.update_from_client()

    def handle_click(self, mouse_pos):
        clicked_square = get_clicked(mouse_pos, self.drawer.squares)
        clicked_piece = self.drawer.piece_locations.get(clicked_square, '0')

        if self.drawer.selected_square:

            # unseleted the square if it was clicked again
            if clicked_square == self.drawer.selected_square:
                self.drawer.selected_square = None
                return
            

            selected_piece = self.drawer.piece_locations.get(self.drawer.selected_square)

            end_rank = "8" if self.client.color == "w" else "1"
            near_end = "7" if self.client.color == "w" else "2"
            
            clicked_end_rank = clicked_square and end_rank in clicked_square
            pawn_selected = selected_piece == self.drawer.perspective+'p'
            pawn_near_end = near_end in self.drawer.selected_square

            if clicked_end_rank and pawn_selected and pawn_near_end:
                promo_choice = self.handle_promotion()
                self.client.send_move(self.drawer.selected_square, clicked_square, promo_choice)
                self.drawer.selected_square = None
                return
            
            enemy_piece_clicked = clicked_piece and clicked_piece[0] != self.drawer.perspective

            # if an enemy piece was clicked or no piece was clicked, attempt a move
            if enemy_piece_clicked or not clicked_piece:
                self.client.send_move(self.drawer.selected_square, clicked_square)
                self.drawer.selected_square = None


        clicked_piece_side = clicked_piece[0]
        if clicked_piece_side == self.drawer.perspective:
            self.drawer.selected_square = clicked_square
