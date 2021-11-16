# importing needed libraries
import socket
import threading
import tkinter as tk
from datetime import datetime

# creating variables for use later
chat = ["Messages will Show-up here,"]
users = ["Current users:"]
FORMAT = "ascii" # format to send messages in

# getting the users name and connected using set IP and Port
print("Connecting to 127.0.0.1")
IP = "127.0.0.1"
print("using port 22222")
PORT = 22222
print("What should others know you as?")
NAME = input("Name: ")
# Creating socket for client and connecting to server socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((IP, PORT))

# Function for receiving requests from the server
def receive():
    while True:
        try:
            message = client.recv(1024).decode(FORMAT)
            if message == "Name":
                client.send(NAME.encode(FORMAT))
            elif "ufs712464" in message: # checks to see if recieved message contains the "phrase" for user list
                msg = message.replace('ufs712464', '')
                msglist = list(msg.split(' '))
                msglist1 = ["Current users: "] + msglist
                lbl_users["text"] = '\n'.join(map(str, msglist1))
            else:
                chat.append(str(message))
                lbl_chat["text"] = '\n'.join(map(str, chat))
        except:
            print("Error, closing connection")
            client.close()
            window.quit()
            break

# Function for sending request for the server
def send():
    msg = Input.get()
    Input.delete(0, tk.END)
    now = datetime.now()
    current_time = now.strftime("[%H:%M:%S] ")  # get the time to add to the message
    message = f'{current_time}{NAME}: {msg}'
    client.send(message.encode(FORMAT))


# creating window for TKinter
window = tk.Tk()
window.title(f'Chatroom - ({NAME})')
window.rowconfigure([0, 1], weight=1)
window.columnconfigure([0, 1], weight=1)
# Created a frame and made a canvas inside of it
container = tk.Frame(window)
canvas = tk.Canvas(container, bg="#161831")
# Made a scrollbar inside of the container
scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas)
# This is how I connected the scrollbar and the canvas inside the frame "container"
scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)
container.grid(row=0, column=0)
# This is the label for the text itself within the frame "container"
lbl_chat = tk.Label(master=scrollable_frame, anchor='nw', justify="left",
                    wraplength=350, fg="#478F97", bg="#161831", font="Helvetica 11", text='\n'.join(map(str, chat)))
# label for the users
lbl_users = tk.Label(master=window,  relief="ridge", anchor='nw', justify="left",
                     width=15, height=10, font="Helvetica", text='\n'.join(map(str, users)))
# Entry box for the user to input text
Input = tk.Entry(master=window, width=65, justify="left")
# button for the user to send input text
btn_Input = tk.Button(master=window, font="Helvetica", text="send", command=send)

# pack and grid is used to set where the widgets are displayed using a grid
canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")
lbl_chat.pack()
lbl_users.grid(row=0, column=1, padx=(5, 5))
Input.grid(row=1, column=0)
btn_Input.grid(row=1, column=1)

# uses multithreading to be able to simultaneously check for receive requests
ReceiveThread = threading.Thread(target=receive)
ReceiveThread.start()
# Ktinker intergrated loop for the window display
window.mainloop()
