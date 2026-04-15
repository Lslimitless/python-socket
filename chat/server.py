from dataclasses import dataclass, asdict
import json
import socket
import threading

HOST = 'localhost'
PORT = 0

clients = {}

@dataclass
class Message:
    type : str
    nick : str
    msg : str
    to : str

    def encoding(self) -> bytes:
        return json.dumps(asdict(self)).encode()
    
    @classmethod
    def decoding(cls, raw_data: bytes):
        data = json.loads(raw_data.decode())
        return cls(**data)

def handle_client(conn, addr):
    # clients.append({'conn':conn, 'nick':nick})
    clients[conn] = conn.recv(1024).decode()
    nick = clients[conn]
    conn.sendall(json.dumps({'type':"sys", 'msg':"서버에 접속하였습니다."}).encode())
    print(f"{addr}({nick})에서 연결")
    print(f"연결된 클라이언트 수 : {len(clients)}")
    
    try:
        while clients[conn]:
            recv_data = conn.recv(1024)
            
            if recv_data.decode() == "QUIT" or recv_data == b'':
                print(f"{addr}({clients.get(conn)})의 연결이 종료됨.")
                del clients[conn]
                print(f"연결된 클라이언트 수 : {len(clients)}")
                conn.close()
                break
        
            elif recv_data:
                data = json.loads(recv_data.decode())
                print(data)

                if data['type'] == "chat":
                    # 존재하지 않는 닉네임에게 귓속말 할 시
                    if data['to'] != "all" and (not data['to'] in clients.values()):
                        try:
                            conn.sendall(json.dumps({'type':"sys", 'msg':"대상을 찾을 수 없습니다."}).encode())
                            continue
                        except:
                            pass
                        
                    # 자신에게 귓속말 할 시
                    elif data['to'] != "all" and data['to'] == data['nick']:
                        try:
                            conn.sendall(json.dumps({'type':"sys", 'msg':"자신에게 귓속말 할 수 없습니다."}).encode())
                            continue
                        except:
                            pass
                    

                    else:
                        # send_data = Message(type="chat", nick=data["nick"], msg=data["msg"], to="")
                        for target_conn, target_nick in clients.items():
                            if data['to'] == target_nick or \
                                data['to'] != "all" and data['nick'] == target_nick or \
                                data['to'] == "all":
                                try:
                                    target_conn.sendall(recv_data)
                                except:
                                    pass

    except:
        print(f"{addr}({clients.get(conn)})의 연결이 비정상적으로 종료됨.")
        conn.close()
        del clients[conn]
        print(f"연결된 클라이언트 수 : {len(clients)}")

    finally:
        try:
            conn.close()
            del clients[conn]
        except:
            pass

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind((HOST, PORT))
serverSocket.listen(5)

ip, assigned_port = serverSocket.getsockname()
print(f"IP:{ip}, {assigned_port} 포트에서 서버 시작.")

while True:
    conn, addr = serverSocket.accept()
    threading.Thread(target=handle_client, args=(conn, addr)).start()
    
serverSocket.close()
print("서버가 종료됨.")