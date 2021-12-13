import socket
import hashlib

# Change IP
SERVER_IP, PORT = '192.168.11.142', 9214

if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((SERVER_IP, PORT))
    sock.settimeout(3)
    print('Connected')
    # socket server
    while True:
        msg = sock.recv(512)

        msg = msg.decode().split(",")
        print(f'Trying num: {msg[0]} for target: {msg[1]}')
        if msg[1] == hashlib.md5(msg[0].encode()).hexdigest():
            ans = "T" + msg[0]
            sock.send(ans.encode())
        else:
            sock.send("false".encode())
