package main

import (
	"encoding/json"
	"fmt"
	"net"

	"github.com/notnil/chess"
)

const BufferSize = 1024

// actions
const (
	StartGame      = "sg" // start code to send to clients when 2 players were found
	RequestingGame = "rg" // client connected and is requesting a game
	Ready          = "r"  // ready check for clients
	SendMove       = "sm" // sending a move
	UpdateBoard    = "ub" // sending a new updated board state
)

// represents a message between client and server
type Message struct {
	Action string                 `json:"action"`
	From   net.Conn               `json:"-"`
	Data   map[string]interface{} `json:"data"`
}

// returns json bytes for a Message
func messageJSON(m *Message) []byte {
	msgJSON, _ := json.Marshal(m)
	return msgJSON
}

// converts chess.board's squaremap to sendable data
func boardData(b chess.Board) map[string]interface{} {
	boardData := make(map[string]interface{})

	for square, piece := range b.SquareMap() {
		boardData[square.String()] = piece.Color().String() + piece.Type().String()
	}

	return boardData
}

// sends a start message with initial board state and players assigned side to the player
func sendStart(playerConn net.Conn, color chess.Color, initialBoard chess.Board) {
	data := map[string]interface{}{
		"color": color.String(),
		"board": boardData(initialBoard),
	}

	msg := Message{Action: StartGame, Data: data}
	playerConn.Write(messageJSON(&msg))
}

// send a new board state to both players
func sendBoard(player1 net.Conn, player2 net.Conn, board chess.Board) {

	msg := Message{Action: UpdateBoard, Data: boardData(board)}
	player1.Write(messageJSON(&msg))
	player2.Write(messageJSON(&msg))
}

// wrapper for making a buffer and reading a message from connection
func readFromConn(conn net.Conn) (Message, error) {
	buffer := make([]byte, BufferSize)
	len, err := conn.Read(buffer)

	trimmedMsg := buffer[:len]

	var response Message
	json.Unmarshal(trimmedMsg, &response)
	response.From = conn

	return response, err
}

// writes a ready message to the connection and expects one back
func connIsAlive(conn net.Conn) bool {
	msg := Message{Action: Ready, Data: map[string]interface{}{}}
	conn.Write(messageJSON(&msg))

	response, _ := readFromConn(conn)
	return response.Action == Ready
}

// continously gets messages from a connection and puts them in msgChan
func getMessages(playerConn net.Conn, msgChan chan<- Message) {
	for {
		msg, err := readFromConn(playerConn)
		if err != nil {
			fmt.Println(err)
		}
		msgChan <- msg
	}
}
