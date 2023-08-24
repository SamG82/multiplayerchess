package main

import (
	"encoding/json"
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
	Data   map[string]interface{} `json:"data"`
}

// returns json bytes for a Message
func messageJSON(m *Message) []byte {
	msgJSON, _ := json.Marshal(m)
	return msgJSON
}

// sends a start message along with the players assigned side to the client
func sendStartMsg(conn net.Conn, side string) {
	msg := Message{Action: StartGame, Data: map[string]interface{}{"side": side}}
	conn.Write(messageJSON(&msg))
}

// wrapper for making a buffer and reading a message from connection
func readFromConn(conn net.Conn) (Message, error) {
	buffer := make([]byte, BufferSize)
	len, err := conn.Read(buffer)

	trimmedMsg := buffer[:len]

	var response Message
	json.Unmarshal(trimmedMsg, &response)

	return response, err
}

func connIsAlive(conn net.Conn) bool {
	msg := Message{Action: Ready, Data: map[string]interface{}{}}
	conn.Write(messageJSON(&msg))

	response, _ := readFromConn(conn)
	return response.Action == Ready
}
