import socket
import random
import threading
import customtkinter as ctk

def login(event):
    HOST = ipEntry.get()
    PORT = int(portEntry.get())
    nickname = nickEntry.get()

    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect((HOST, PORT))
    clientSocket.sendall(nickname.encode('utf-8'))
    print("서버와 연결됨.")

root = ctk.CTk()
root.geometry("270x480")
root.title("Socket Chat")
ctk.set_appearance_mode("dark")  # "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")

ipFortFrame = ctk.CTkFrame(root)
ipFortFrame.pack(pady=(10,0))

ipEntry = ctk.CTkEntry(ipFortFrame, placeholder_text="IP", width=150, height=35, corner_radius=10)
ipEntry.pack(side='left')

portEntry = ctk.CTkEntry(ipFortFrame, placeholder_text="Port", width=100, height=35, corner_radius=10)
portEntry.pack(side='right')

nickEntry = ctk.CTkEntry(root, placeholder_text="Nickname", width=250, height=35, corner_radius=10)
nickEntry.pack(pady=(2, 0))
nickEntry.bind("<Return>", command=login)

loginButton = ctk.CTkButton(root, text="Sign in", command=login, width=100, height=35, corner_radius=10)
loginButton.pack(pady=(2, 0))

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
            data = clientSocket.recv(1024).decode('utf-8')
            if data:
                print(data)

        except:
            break

threading.Thread(target=receive, daemon=True).start()

root.mainloop()

# while True:
#     msg = input()
#     clientSocket.sendall(msg.encode('utf-8'))


clientSocket.close()