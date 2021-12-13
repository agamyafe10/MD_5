import hashlib
import threading
import socket
import time

# change ip
IP, PORT   = '192.168.11.153', 9214
TRG = "EC9C0F7EDCC18A98B1F31853B1813301".lower() #target
found = False
current_try = 0

# Handles every new client
def handler(client, address):
    global current_try, found
    while not found:
        x = str(current_try).zfill(10)
        x+=","
        x+=TRG
        print(f'sending num: {current_try} to {address}')
        current_try+=1
        client.send(x.encode())
        # -----------------------------------
        ans = client.recv(512).decode()
        if not ans:
            print(f'disconncted {address}')
            return
        if ans[0]=="T":
            found = True
            time.sleep(2)
            print(f'Found {ans[1:]}')
            return

if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((IP, PORT))
    sock.listen(1)
    print("Running")

    
    while not found:
        try:
            client, address = sock.accept()
            print(f"connected to client {address}")

            thr = threading.Thread(target=handler, args=(client, address))
            thr.start()
        except:
            continue