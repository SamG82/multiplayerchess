package main

import (
	"fmt"
	"net"
)

const port = ":3000"

func main() {
	listener, err := net.Listen("tcp", port)
	if err != nil {
		fmt.Println(err)
		return
	}

	defer listener.Close()

	for {
		connection, err := listener.Accept()
		if err != nil {
			fmt.Println(err)
		}

		buffer := make([]byte, 512)

		msgLen, err := connection.Read(buffer)
		if err != nil {
			fmt.Println(err)
		}

		trimmedMsg := buffer[:msgLen]

		fmt.Println("Message received: " + string(trimmedMsg))
	}
}
