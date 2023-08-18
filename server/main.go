package main

import (
	"fmt"
	"net"
)

const port = ":3000"

// network codes
const (
	requestMatch byte = 'r'
)

// global list of all created games
var allGames GameList

// create new game variables from the gameQueu
func createGames(gameQueue <-chan net.Conn) {
	for {
		player1 := <-gameQueue
		player2 := <-gameQueue

		newGame := Game{player1, player2, true}

		allGames.addGame(&newGame)
	}
}

// handles a new client connection to add them to the queue
func newConnHandler(conn net.Conn, gameQueue chan<- net.Conn) {
	buffer := make([]byte, 16)

	msgLen, err := conn.Read(buffer)

	if err != nil {
		fmt.Println(err)
		return
	}

	message := buffer[:msgLen]

	switch message[0] {
	case requestMatch:
		gameQueue <- conn
	}

}

func main() {
	listener, err := net.Listen("tcp", port)
	if err != nil {
		fmt.Println(err)
		return
	}

	defer listener.Close()

	gameQueue := make(chan net.Conn)
	go createGames(gameQueue)

	// listen for new connections
	for {
		connection, err := listener.Accept()
		if err != nil {
			fmt.Println(err)
			continue
		}

		go newConnHandler(connection, gameQueue)
	}

}
