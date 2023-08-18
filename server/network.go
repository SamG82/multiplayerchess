package main

import (
	"fmt"
	"net"
)

// constant network codes
const (
	requestGame  byte = 'r' // client requesting a new match
	startingGame byte = 's' // notifies client of a game starting

	sideWhite byte = 'w'
	sideBlack byte = 'b'
)

// sends a start code along with the players assigned side to the client
func sendStartMsg(conn net.Conn, side byte) {
	msg := []byte{startingGame, side}

	_, err := conn.Write(msg)
	if err != nil {
		fmt.Println(err)
	}
}
