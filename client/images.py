from pygame.image import load

dark_square = load("./media/square brown dark_png_1024px.png")
light_square = load("./media/square brown light_png_1024px.png")
yellow_square = load("./media/yellow_square.png")

move_marker = load("./media/move_marker.png")

piece_images = {
    "pawn_black": load("./media/b_pawn_png_1024px.png"),
    "rook_black": load("./media/b_rook_png_1024px.png"),
    "knight_black": load("./media/b_knight_png_1024px.png"),
    "bishop_black": load("./media/b_bishop_png_1024px.png"),
    "queen_black": load("./media/b_queen_png_1024px.png"),
    "king_black": load("./media/b_king_png_1024px.png"),

    "pawn_white": load("./media/w_pawn_png_1024px.png"),
    "rook_white": load("./media/w_rook_png_1024px.png"),
    "knight_white": load("./media/w_knight_png_1024px.png"),
    "bishop_white": load("./media/w_bishop_png_1024px.png"),
    "queen_white": load("./media/w_queen_png_1024px.png"),
    "king_white": load("./media/w_king_png_1024px.png")
}