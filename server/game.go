package main

import (
	"net"
	"sync"
)

type Game struct {
	player1 net.Conn
	player2 net.Conn

	player1Turn bool
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
