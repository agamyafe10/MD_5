import hashlib
import threading
import time
import socket
import select
from help_funcs import *


# deafault settings
SERVER_IP = '127.0.0.1'
SERVER_PORT = 5678
RANGE_NUM = 1


server_socket = setup_socket()
open_client_sockets = []  # the sockets which currently connected to the server
flag = False
print("Started Server Listening Operation...")
while not flag:
    r_list, w_list, x_list = select.select([server_socket] + open_client_sockets, open_client_sockets, [])
    for current_socket in r_list:
        if current_socket is server_socket:  # if it is a new client
            (new_socket, address) = server_socket.accept()
            print("new socket connected to server: ", new_socket.getpeername())
            open_client_sockets.append(new_socket)
        else:
            client_request = recv_msg(current_socket)# recieves the client request
            if client_request is None:
                print("[Client Disconnected Surprisingly]")
                open_client_sockets.remove(current_socket)
                continue
            if client_request == "REQUEST":# if the clients asks for a range
                send_range(current_socket, RANGE_NUM)
                RANGE_NUM += 1# change the range so every client will get a different range
            elif "Hash:" in client_request:# if  a client found 
                flag = True
                print("The clients have foud the password")
                open_client_sockets.remove(current_socket)# removes theclient that found the password
                for client in open_client_sockets:# runs through the clients and tell them to stop running
                    client.send("STOP".encode())
                    open_client_sockets.remove(client)
            
# יש מצב שצריך להשתמש בשלחיה של הכל לכל הלקוחות באופן מרוכז כדי לדעת איפה זה נפל