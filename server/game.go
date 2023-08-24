package main

import (
	"math/rand"
	"net"
	"time"
)

const (
	sideWhite = "white"
	sideBlack = "black"
)

// random true/false
func randomBool() bool {
	randSource := rand.NewSource(time.Now().UnixNano())
	randNum := rand.New(randSource)

	// eiher 0 or 1
	return randNum.Intn(2) == 1
}

// return 2 sides in random order
func getRandomizedSides() (string, string) {
	if randomBool() {
		return sideWhite, sideBlack
	}

	return sideBlack, sideWhite
}

type Game struct {
	player1Conn net.Conn
	player2Conn net.Conn

	player1Side string
	player2Side string

	player1Turn bool
}

// return a new game variable with default values using 2 player connections
func NewGame(player1Conn net.Conn, player2Conn net.Conn) Game {
	side1, side2 := getRandomizedSides()

	return Game{
		player1Conn,
		player2Conn,
		side1,
		side2,
		true,
	}
}

// send start messages and start listening for player messages
func (g *Game) start() {
	sendStartMsg(g.player1Conn, g.player1Side)
	sendStartMsg(g.player2Conn, g.player2Side)
}
