#!/usr/bin/env python
# coding: utf-8

import socket
from _thread import *
import threading


def readFile(conn, fileType):
    fileName = "test." + fileType
    File = open(fileName, 'wb')
    while True:
        try:
            Data = conn.recv(1)
            if not Data:
                break
            File.write(Data)
        except ConnectionResetError as e:
            break


# thread fuction
def threaded(conn):
    while True:
        # data received from client
        data = conn.recv(1024)
        if data.decode() == "pgm":
            readFile(conn, "pgm")
            break

        if data.decode() == "json":
            readFile(conn, "json")
            break

        if not data:
            break

        print("Receive data:", data.decode())

        if float(data.decode().split(',')[2]) > 3000.0:
            print("lacation :",
                  data.decode().split(',')[0],
                  "is fire!!!!!!!!!!!!!!!!!!!!!!!")
            # do anything

    # connection closed
    conn.close()


if __name__ == '__main__':
    # 建立一个服务端
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  #防止端口被佔用

    ip = socket.gethostbyname(socket.gethostname())  #ip, port
    port = 6668

    print("Host :", ip)  #固定ip才可以連線
    server.bind((ip, port))  #绑定要监听的端口
    server.listen(4)  #开始监听 表示可以使用四个链接排队
    print("Socket is listening...")
    while True:
        conn, addr = server.accept()  #等待链接,多个链接的时候就会出现问题,其实返回了两个值
        print('Connected to :', addr[0], ':', addr[1])

        # Start a new thread and return its identifier
        start_new_thread(threaded, (conn, ))
    server.close()
