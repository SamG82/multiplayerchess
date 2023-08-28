package main

import (
	"math/rand"
	"net"
	"time"

	"github.com/notnil/chess"
)

// random true/false
func randomBool() bool {
	randSource := rand.NewSource(time.Now().UnixNano())
	randNum := rand.New(randSource)

	// eiher 0 or 1
	return randNum.Intn(2) == 1
}

// return 2 colors in random order
func randomizedColors() (chess.Color, chess.Color) {
	var choice chess.Color
	if randomBool() {
		choice = chess.White
	} else {
		choice = chess.Black
	}

	return choice, choice.Other()
}

// holds connections to both players along with the chess game
type GameLobby struct {
	players   map[chess.Color]net.Conn
	turn      net.Conn
	chessGame chess.Game
}

// return a new game variable with default values using 2 player connections
func NewGameLobby(player1Conn net.Conn, player2Conn net.Conn) GameLobby {
	color1, color2 := randomizedColors()
	players := map[chess.Color]net.Conn{color1: player1Conn, color2: player2Conn}

	return GameLobby{
		players:   players,
		turn:      players[chess.White],
		chessGame: *chess.NewGame(chess.UseNotation(chess.UCINotation{})),
	}
}

// send start messages and start handling player messages
func (gl *GameLobby) run() {
	msgChan := make(chan Message)
	initialBoard := *gl.chessGame.Position().Board()
	for side, conn := range gl.players {
		sendStart(conn, side, initialBoard)
		go getMessages(conn, msgChan)
	}

	for msg := range msgChan {
		switch msg.Action {
		case SendMove:
			// skip the message if it isn't the player's turn
			if msg.From != gl.turn {
				continue
			}

			// attempt to make the move on the board
			move := msg.Data["move"].(string)
			err := gl.chessGame.MoveStr(move)
			if err != nil {
				continue
			}

			sendBoard(gl.players[chess.White], gl.players[chess.Black], *gl.chessGame.Position().Board())
			gl.turn = gl.players[gl.chessGame.Position().Turn()]
		}
	}
}
