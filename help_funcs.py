import socket


SERVER_IP = '127.0.0.1'
SERVER_PORT = 5678
TARGET = "EC9C0F7EDCC18A98B1F31853B1813301".lower() #target

def setup_socket():
	"""
	Creates new listening socket and returns it
	Recieves: -
	Returns: the socket object
	"""
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)# defining the basic socket settings
	server_socket.bind((SERVER_IP, SERVER_PORT))# defining the socket with our details
	server_socket.listen(5)# limting the number of clients can connect
	print("Listening for connections on port %d" % SERVER_PORT)
	return server_socket


def recv_msg(conn):
    """recieves a socket and returns the data recieved as a string
    """
    try:
        data = conn.recv(2048).decode()
        print("Server Response: " + data)
        return data
    except:
        print("ERROR WHILE GETTING CLIENT'S REQUEST")


def send_range(conn, range_num):
	"""uses the global variable rANGE_NUM in oreder to send the range to the client
	"""
	from_num = str(pow(10, 10)* range_num)
	to_num = str(pow(10, 10)* (range_num + 1))
	conn.send((from_num + '-' + to_num + '-' + TARGET).encode())

	