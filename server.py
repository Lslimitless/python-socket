import socket
import threading

HOST = '0.0.0.0'
PORT = 0

clients = []

def handle_client(conn, addr, nick):
    print(f"{addr}({nick})에서 연결")
    clients.append({'conn':conn, 'nick':nick})
    
    try:
        while True:
            data = conn.recv(1024).decode('utf-8')
            if data:
                if data[0] == "/":
                    dataSplit = data.split(maxsplit=2)
                    if len(dataSplit) >= 3:
                        if dataSplit[0].lower() == "/w":
                            print(f"{nick} -> {dataSplit[1]}:{dataSplit[2:][0]}")
                            for client in clients:
                                if client['nick'] == data.split()[1]:
                                    client['conn'].sendall(f"{nick} -> me:{dataSplit[2:][0]}".encode('utf-8'))
    
                else:
                    msg = data

                    for client in clients:
                        if client['conn'] == conn:
                            print(f"{nick}:{msg}")

                        else:
                            client['conn'].sendall(f"{nick}:{msg}".encode('utf-8'))
    except:
        pass
    finally:
        print(f"{addr}의 연결이 종료됨.")
        for client in clients:
            if client['conn'] == conn:
                clients.remove(client)

        conn.close()

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind((HOST, PORT))
serverSocket.listen(1)

assigned_port = serverSocket.getsockname()[1]
print(f"{assigned_port} 포트에서 서버 시작.")

while True:
    conn, addr = serverSocket.accept()
    nick = conn.recv(1024).decode('utf-8')

    threading.Thread(target=handle_client, args=(conn, addr, nick)).start()
    
serverSocket.close()