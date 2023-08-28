package main

import (
	"encoding/json"
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
	Conclude       = "c"  // game is concluding
	Disconnect     = "dc" // client disconnected
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

func writeMessage(msg Message, conns ...net.Conn) {
	for _, conn := range conns {
		conn.Write(messageJSON(&msg))
	}
}

// sends a start message with initial board state and players assigned side to the player
func sendStart(color chess.Color, initialBoard chess.Board, playerConns ...net.Conn) {
	data := map[string]interface{}{
		"color": color.String(),
		"board": boardData(initialBoard),
	}

	msg := Message{Action: StartGame, Data: data}
	writeMessage(msg, playerConns...)
}

// sends a conclusion message with winner and reason
func sendConclusion(winner string, reason string, playerConns ...net.Conn) {
	msg := Message{Action: Conclude, Data: map[string]interface{}{"winner": winner, "reason": reason}}
	writeMessage(msg, playerConns...)
}

// send a new board state to both players
func sendBoard(board chess.Board, playerConns ...net.Conn) {
	msg := Message{Action: UpdateBoard, Data: boardData(board)}
	writeMessage(msg, playerConns...)
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
	writeMessage(msg, conn)

	response, _ := readFromConn(conn)
	return response.Action == Ready
}

// continously gets messages from a connection and puts them in msgChan
func getMessages(playerConn net.Conn, msgChan chan<- Message) {
	for {
		msg, err := readFromConn(playerConn)
		if err != nil {
			msgChan <- Message{Action: Disconnect, From: playerConn, Data: map[string]interface{}{}}
			return
		}
		msgChan <- msg
	}
}
