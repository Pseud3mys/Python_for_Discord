import socket
import random

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)

# max 65 535, evite les doubles commeca
PORT = random.randint(65432, 65535)  # Port to listen on (non-privileged ports are > 1023)


def hack_input(text=">? "):
    print(":input:"+str(PORT)+":"+text)
    input_str = ""
    # server to receive answer
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                input_str = data.decode('utf-8')
                conn.sendall(b'ok')
    return input_str
