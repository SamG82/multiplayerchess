package main

import (
	"encoding/json"
	"fmt"
	"net"
)

const BufferSize = 128

// actions
const (
	StartGame      = "sg"
	RequestingGame = "rg"
	Ready          = "r"
	SendMove       = "sm"
)

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

// sends a start message  along with the players assigned side to the client
func sendStart(playerConn net.Conn, side side) {
	msg := Message{Action: StartGame, Data: map[string]interface{}{"side": side}}
	playerConn.Write(messageJSON(&msg))
}

func sendMessage(playerConn net.Conn, msg Message) {
	playerConn.Write(messageJSON(&msg))
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
