package main

import (
	"fmt"
	"net"
	"os"
)

// create new game variables from the playerQueue
func createGames(playerQueue chan net.Conn) {
	for {
		player1 := <-playerQueue
		player2 := <-playerQueue

		// handle the first player disconnecting while in queue
		if !connIsAlive(player1) {
			go func() {
				playerQueue <- player2
			}()
			continue
		}

		ng := NewGameLobby(player1, player2)
		go ng.run()
	}
}

// handles a new client connection to add them to the queue
func newConnHandler(conn net.Conn, gameQueue chan<- net.Conn) {
	message, err := readFromConn(conn)
	if err != nil {
		fmt.Println(err)
		return
	}

	switch message.Action {
	case RequestingGame:
		gameQueue <- conn
	}

}

func main() {
	listener, err := net.Listen("tcp", ":"+os.Args[1])
	if err != nil {
		fmt.Println(err)
		return
	}

	defer listener.Close()

	playerQueue := make(chan net.Conn)
	go createGames(playerQueue)

	// listen for new connections
	for {
		connection, err := listener.Accept()
		if err != nil {
			fmt.Println(err)
			continue
		}

		go newConnHandler(connection, playerQueue)
	}

}
