from dataclasses import dataclass, asdict
import json
import socket
import random
import threading
import customtkinter as ctk
import PIL
from io import BytesIO
import requests

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
    
def focus_next(event):
    event.widget.tk_focusNext().focus()

def connection(*event):
    try:
        HOST = ipEntry.get()
        PORT = int(portEntry.get())
        global nickname
        nickname = nickEntry.get() if nickEntry.get() else "Guest"+str(random.randint(0,9999))

        global clientSocket
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientSocket.connect((HOST, PORT))

        isConnect = True
        loginUI.place_forget()
        chatUI.place(relwidth=1, relheight=1)
        clientSocket.sendall(nickname.encode())
        print("서버와 연결됨.")

    except:
        print("입력값을 다시 확인하세요.")

def quit(*event):
    clientSocket.sendall("QUIT".encode())
    isConnect = False
    chatUI.place_forget()
    loginUI.place(relx=0.5, rely=0.5, anchor="center")
    clientSocket.close()

def chatHistoryAppend(msg):
    chatHistory.configure(state="normal")
    chatHistory.insert("end", msg+"\n")
    chatHistory.see("end")
    chatHistory.configure(state="disabled")

def chat(*event):
    if inputEntry.get():
        data = inputEntry.get()
        inputEntry.delete("0", "end")

        dataSplit = data.split(maxsplit=2)
        if data[0] == "/":
            if dataSplit[0].lower() == "/w" and len(dataSplit) >= 3:
                to = dataSplit[1]
                msg = dataSplit[2]

        else:
            to = "all"
            msg = data
            
        send_data = json.dumps({'type':"chat", 'nick':nickname, 'msg':msg, 'to':to})
        # print(data)
        # if to == "all":
        #     chatHistoryAppend("{} : {}".format(nickname, msg))
        # else:
        #     chatHistoryAppend("me -> {} : {}".format(nickname, msg))

        clientSocket.sendall(send_data.encode())

isConnect = False
nickname = ""

root = ctk.CTk()
root.geometry("270x480")
root.title("Socket Chat")
ctk.set_appearance_mode("System")  # "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")

# 로그인 UI
loginUI = ctk.CTkFrame(root, fg_color="transparent")
loginUI.place(relx=0.5, rely=0.5, anchor="center")

response = requests.get("https://uxwing.com/wp-content/themes/uxwing/download/brands-and-social-media/python-programming-language-icon.png")
pythonImage = ctk.CTkImage(light_image=PIL.Image.open(BytesIO(response.content)),
                         dark_image=PIL.Image.open(BytesIO(response.content)),
                         size=(100,100))
logoLabel = ctk.CTkLabel(loginUI, image=pythonImage, text="")
logoLabel.pack(pady=(10,0))

ipFortFrame = ctk.CTkFrame(loginUI, fg_color="transparent")
ipFortFrame.pack(pady=(20,0))

ipEntry = ctk.CTkEntry(ipFortFrame, placeholder_text="IP", width=150, height=35, corner_radius=10)
ipEntry.pack(side='left')
ipEntry.bind("<Return>", command=focus_next)

portEntry = ctk.CTkEntry(ipFortFrame, placeholder_text="Port", width=100, height=35, corner_radius=10)
portEntry.pack(side='right')
portEntry.bind("<Return>", command=focus_next)

nickEntry = ctk.CTkEntry(loginUI, placeholder_text="Nickname", width=250, height=35, corner_radius=10)
nickEntry.pack(pady=(2,0))
nickEntry.bind("<Return>", command=connection)

loginButton = ctk.CTkButton(loginUI, text="Connect", command=connection, width=100, height=35, corner_radius=10)
loginButton.pack(pady=10)

# 채팅창 UI
chatUI = ctk.CTkFrame(root, fg_color="transparent")

topMenu = ctk.CTkFrame(chatUI, fg_color="skyblue", height=35, corner_radius=0)
topMenu.pack(side="top", fill="x")

quitButton = ctk.CTkButton(topMenu, text="Quit", command=quit, width=35, height=35, corner_radius=10)
quitButton.pack(side="right")

inputUI = ctk.CTkFrame(chatUI, fg_color="transparent")
inputUI.pack(side="bottom", fill="x")

inputButton = ctk.CTkButton(inputUI, text="Enter", command=chat, width=70, height=35, corner_radius=10)
inputButton.pack(side="right")

inputEntry = ctk.CTkEntry(inputUI, placeholder_text="", height=35, corner_radius=10)
inputEntry.pack(side="left", fill="x", expand=True)
inputEntry.bind("<Return>", command=chat)

chatHistory = ctk.CTkTextbox(chatUI)
chatHistory.configure(state="disabled")
chatHistory.pack(fill="both", expand="True")


# HOST = '0.0.0.0'

# while True:
#     try:
#         PORT = int(input("포트:"))
#         break
#     except:
#         continue

# try:
#     nickname = str(input("이름:"))
# except:
#     nickname = "Guest"+str(random.randint(0,65535))
# print(nickname)

def receive():
    while True:
        try:
            recv_data = clientSocket.recv(1024)
            if recv_data:
                data = json.loads(recv_data.decode())
                print(data)
                if data['type'] == "chat":
                    if data['to'] == nickname:
                        msg = "{} -> me : {}".format(data['nick'], data['msg'])
                    
                    elif data['nick'] == nickname and data['to'] != "all":
                        msg = "me -> {} : {}".format(data['to'], data['msg'])

                    else:
                        msg = "{} : {}".format(data['nick'], data['msg'])
                    
                    chatHistoryAppend(msg)

                elif data['type'] == "sys":
                    chatHistoryAppend(data['msg'])

        except:
            continue

threading.Thread(target=receive, daemon=True).start()

root.mainloop()

# while True:
#     msg = input()
#     clientSocket.sendall(msg.encode('utf-8'))

clientSocket.close()