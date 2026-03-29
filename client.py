import socket
import time
import random
import threading

HOST = '0.0.0.0'

while True:
    try:
        PORT = int(input("포트:"))
        break
    except:
        continue

try:
    nickname = str(input("이름:"))
    print(nickname)
except:
    nickname = "Guest"+str(random.randint(0,65535))

def receive():
    while True:
        try:
            data = clientSocket.recv(1024).decode('utf-8')
            if data:
                print(data)

        except:
            break

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((HOST, PORT))
clientSocket.sendall(nickname.encode('utf-8'))
print("서버와 연결됨.")


threading.Thread(target=receive, daemon=True).start()

while True:
    msg = input()
    clientSocket.sendall(msg.encode('utf-8'))

clientSocket.close()