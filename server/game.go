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

// returns a winner string from an outcome
func getWinner(outcome chess.Outcome) string {
	if outcome == chess.WhiteWon {
		return "White"
	} else if outcome == chess.BlackWon {
		return "Black"
	} else {
		return "Draw"
	}
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
		sendStart(side, initialBoard, conn)
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

			if endReason := gl.chessGame.Method(); endReason != chess.NoMethod {
				winner := getWinner(gl.chessGame.Outcome())
				sendConclusion(winner, endReason.String(), gl.players[chess.White], gl.players[chess.Black])
			}

			sendBoard(*gl.chessGame.Position().Board(), gl.players[chess.White], gl.players[chess.Black])
			gl.turn = gl.players[gl.chessGame.Position().Turn()]

		case Disconnect:
			// game is already done
			if gl.chessGame.Method() != chess.NoMethod {
				continue
			}

			var disconnectedColor chess.Color
			for color, conn := range gl.players {
				if conn == msg.From {
					disconnectedColor = color
				}
			}

			gl.chessGame.Resign(disconnectedColor)
			winner := getWinner(gl.chessGame.Outcome())
			reason := gl.chessGame.Method().String()

			sendConclusion(winner, reason, gl.players[chess.White], gl.players[chess.Black])
			return
		}
	}
}
