package main

import (
	"math/rand"
	"net"
	"sync"
	"time"
)

// random true/false
func randomBool() bool {
	randSource := rand.NewSource(time.Now().UnixNano())
	randNum := rand.New(randSource)

	// eiher 0 or 1
	choice := randNum.Intn(2)

	return choice == 1
}

type Game struct {
	player1Conn net.Conn
	player2Conn net.Conn

	player1Side byte
	player2Side byte

	player1Turn bool
}

// returns a new game with default values from connections
func NewGame(player1Conn net.Conn, player2Conn net.Conn) *Game {
	return &Game{player1Conn, player2Conn, 0, 0, true}
}

// assign sides and start communicating with clients
func (g *Game) start() {
	choice := randomBool()
	if choice {
		g.player1Side = sideWhite
		g.player2Side = sideBlack
	} else {
		g.player1Side = sideBlack
		g.player2Side = sideWhite
	}

	sendStartMsg(g.player1Conn, g.player1Side)
	sendStartMsg(g.player2Conn, g.player2Side)
}

type GameList struct {
	mu    sync.Mutex
	games []*Game
}

func (g *GameList) addGame(newGame *Game) {
	g.mu.Lock()
	defer g.mu.Unlock()

	g.games = append(g.games, newGame)
}
