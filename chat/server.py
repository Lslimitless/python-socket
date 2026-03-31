import socket
import threading

HOST = 'localhost'
PORT = 0

clients = []

def handle_client(conn, addr, nick):
    print(f"{addr}({nick})에서 연결")
    clients.append({'conn':conn, 'nick':nick})
    print(len(clients))
    
    try:
        while True:
            data = conn.recv(1024).decode('utf-8')
            if data:
                # /명령어 처리
                if data[0] == "/":
                    # /w 귓속말 기능
                    dataSplit = data.split(maxsplit=2)
                    if dataSplit[0].lower() == "/w" and len(dataSplit) >= 3:
                        print(f"{nick} -> {dataSplit[1]}:{dataSplit[2:][0]}")
                        # 자신에게 귓속말 하는지 여부
                        if nick != data.split()[1]:
                            for client in clients:
                                if client['nick'] == data.split()[1]:
                                    client['conn'].sendall(f"{nick} -> me:{dataSplit[2:][0]}".encode('utf-8'))
                        else:
                            conn.sendall("자신에게는 귓속말 할 수 없습니다.".encode('utf-8'))

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
serverSocket.listen(5)

ip, assigned_port = serverSocket.getsockname()
print(f"IP:{ip}, {assigned_port} 포트에서 서버 시작.")

while True:
    conn, addr = serverSocket.accept()
    nick = conn.recv(1024).decode('utf-8')

    threading.Thread(target=handle_client, args=(conn, addr, nick)).start()
    
serverSocket.close()