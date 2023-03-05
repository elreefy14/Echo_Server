import socket
import threading
import string
import time

HOST = '127.0.0.1'  # define as a global variable
PORT = 12346  # use a non-privileged port
def handle_client(conn, addr):
    print(f"New connection from {addr}")
    while True:
        data = conn.recv(1024).decode().strip()
        if not data:
            break
        print(f"Received from {addr}: {data}")
        
        first_char = data[0]
        string_to_order = data[1:]
        if first_char == 'A':
            ordered_string = ''.join(sorted(string_to_order))
        elif first_char == 'C':
            ordered_string = string_to_order.upper()
        elif first_char == 'D':
            ordered_string = ''.join(sorted(string_to_order, reverse=True))
        else:
            ordered_string = data
        
        conn.sendall(ordered_string.encode())
        print(f"Sent to {addr}: {ordered_string}")

    conn.close()
    print(f"Connection from {addr} closed")


def run_server():
 

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Server listening on port {PORT}")

        while True:
            conn, addr = s.accept()
            handle_client(conn, addr)


if __name__ == '__main__':
    # start the server in a separate thread
    server_thread = threading.Thread(target=run_server)
    server_thread.start()

    # wait for the server to start up
    time.sleep(1)
    
    # create a test client and send messages
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((HOST, PORT))
            # read input from user in an infinite loop and send to server
        while True:
            message = input("Enter a message: ")
            if not message:
                break
            client.sendall(message.encode())
            response = client.recv(1024).decode().strip()
            print(f"Received from server: {response}")


        # # test case 1: send a message starting with 'A'
        # message = 'Ahello'
        # client.sendall(message.encode())
        # response = client.recv(1024).decode().strip()
        # assert response == 'ehllo', f'Expected "ehllo", but got "{response}"'

        # # test case 2: send a message starting with 'C'
        # message = 'Cgoodbye'
        # client.sendall(message.encode())
        # response = client.recv(1024).decode().strip()
        # assert response == 'GOODBYE', f'Expected "GOODBYE", but got "{response}"'

        # # test case 3: send a message starting with 'D'
        # message = 'Dworld'
        # client.sendall(message.encode())
        # response = client.recv(1024).decode().strip()
        # assert response == 'wrold', f'Expected "wrold", but got "{response}"'

        # # test case 4: send a message starting with a different character
        # message = 'Xtest'
        # client.sendall(message.encode())
        # response = client.recv(1024).decode().strip()
        # assert response == 'Xtest', f'Expected "Xtest", but got "{response}"'

    # stop the server
    server_thread.join()

