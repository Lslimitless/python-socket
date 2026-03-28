import socket
import threading

HOST = '0.0.0.0'
PORT = 0

clients = []

def handle_client(conn, addr):
    print(f"{addr}에서 연결")
    clients.append(conn)
    try:
        while True:
            data = conn.recv(1024)
            if data:
                msg = data.decode('utf-8')
                print(f"{addr}:{msg}")

                for client in clients:
                    if client != conn:
  
                        client.sendall(f"{addr}:{msg}".encode('utf-8'))
    except:
        pass
    finally:
        print(f"{addr}의 연결이 종료됨.")
        clients.remove(conn)
        conn.close()

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind((HOST, PORT))
serverSocket.listen(1)

assigned_port = serverSocket.getsockname()[1]
print(f"{assigned_port} 포트에서 서버 시작.")

while True:
    conn, addr = serverSocket.accept()

    threading.Thread(target=handle_client, args=(conn, addr)).start()
    
serverSocket.close()