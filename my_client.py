import socket
import hashlib
from hashlib import md5
import threading


PORT = 5678
IP = "127.0.0.1"


def str_to_hash(client_input="Hello World!"):
    hash_object = hashlib.md5(client_input.encode())
    hashed_code = hash_object.hexdigest()
    return hashed_code


def start_hashing(fromnum, to, hashes):
    global is_found
    for i in range(int(fromnum), int(to)):
        print("\n Num: {} \n Hash: {} \n".format(i ,str_to_hash(str(i))))
        if str_to_hash(str(i)) == hashes.lower():
            print("Your Number is: {}".format(i))
            is_found = True
            return i
    return -1


def connect():
    """connect the client to the server
    Returns:
        socket[socket]:
    """
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # defining the socket
    my_socket.connect((IP, PORT))  # connect to the server
    print("Connected to server on port %d" % PORT)
    return my_socket


def main():
    global is_found 
    is_found = False
    threads_lst = []
    conn_sock = connect()
    print("Connected...")
    found = False

    while not found:
        try:
            conn_sock.send("REQUEST".encode())
        except:
            print("Another client found the password :(")
            break
        data = conn_sock.recv(1024).decode()
        start, end, hashes = data.split("-")
        start = int(start)
        end = int(end)
        for i in range(5):
            threads_lst.append(threading.Thread(target = start_hashing, args = ((start+((end-start)/5)*(i)),(start+((end - start)/5)*(i+1)), hashes)))
        for t in threads_lst:
            t.start()
        flag = True
        while flag:
            for t in threads_lst:
                if is_found:
                    num = t.join
                    flag = False
                    found = True
                    conn_sock.send("Hash: {0}".format(num))
                    conn_sock.close()
    

if __name__ == '__main__':
    main()