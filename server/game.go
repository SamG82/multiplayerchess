package main

import (
	"math/rand"
	"net"
	"time"
)

const (
	SideWhite = "white"
	SideBlack = "black"
)

type side string

// random true/false
func randomBool() bool {
	randSource := rand.NewSource(time.Now().UnixNano())
	randNum := rand.New(randSource)

	// eiher 0 or 1
	return randNum.Intn(2) == 1
}

// return 2 sides in random order
func getRandomizedSides() (side, side) {
	if randomBool() {
		return SideWhite, SideBlack
	}

	return SideBlack, SideWhite
}

type Game struct {
	players map[side]net.Conn
	turn    side
}

// return a new game variable with default values using 2 player connections
func NewGame(player1Conn net.Conn, player2Conn net.Conn) Game {
	side1, side2 := getRandomizedSides()
	return Game{
		players: map[side]net.Conn{side1: player1Conn, side2: player2Conn},
		turn:    SideWhite,
	}
}

func getOpponent(playerConn net.Conn, g Game) (side, net.Conn) {
	for side, conn := range g.players {
		if conn != playerConn {
			return side, conn
		}
	}

	return "", nil
}

// send start messages and start handling player messages
func (g *Game) run() {
	msgChan := make(chan Message)
	for side, conn := range g.players {
		sendStart(conn, side)
		go getMessages(conn, msgChan)
	}

	for msg := range msgChan {
		switch msg.Action {
		case SendMove:
			if msg.From != g.players[g.turn] {
				continue
			}

			oppSide, oppConn := getOpponent(msg.From, *g)
			sendMessage(oppConn, msg)

			g.turn = oppSide
		}
	}
}
