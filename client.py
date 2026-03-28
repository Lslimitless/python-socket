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

while True:
    try:
        nickname = int(input("이름:"))
        break
    except:
        continue

def receive():
    while True:
        try:
            data = clientSocket.recv(1024).decode('utf-8')
            if data:
                print(f"SERVER:{data}")

        except:
            break

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((HOST, PORT))
print("서버와 연결됨.")

threading.Thread(target=receive, daemon=True).start()

while True:
    msg = input()
    clientSocket.sendall(msg.encode('utf-8'))

clientSocket.close()