import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox

HOST = '127.0.0.1'  # Server IP address (localhost here)
PORT = 12345        # Server port

class ChatClient:
    def __init__(self, master):
        self.master = master
        self.master.title("Chat Client")
        self.master.geometry("400x500")

        self.nickname = ""

        self.build_gui()
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def build_gui(self):
        self.top_frame = tk.Frame(self.master)
        self.top_frame.pack(pady=10)

        tk.Label(self.top_frame, text="Enter Nickname:").pack(side=tk.LEFT)
        self.nickname_entry = tk.Entry(self.top_frame)
        self.nickname_entry.pack(side=tk.LEFT)
        self.connect_btn = tk.Button(self.top_frame, text="Connect", command=self.connect_to_server)
        self.connect_btn.pack(side=tk.LEFT, padx=5)

        self.chat_area = scrolledtext.ScrolledText(self.master, state='disabled')
        self.chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.message_entry = tk.Entry(self.master, state='disabled')
        self.message_entry.pack(padx=10, pady=5, fill=tk.X)
        self.message_entry.bind("<Return>", self.send_message)

        self.send_btn = tk.Button(self.master, text="Send", state='disabled', command=self.send_message)
        self.send_btn.pack(pady=5)

    def connect_to_server(self):
        self.nickname = self.nickname_entry.get().strip()
        if not self.nickname:
            messagebox.showwarning("Input Error", "Please enter a nickname.")
            return

        try:
            self.client_socket.connect((HOST, PORT))
        except Exception as e:
            messagebox.showerror("Connection Error", f"Cannot connect to server:\n{e}")
            return

        self.nickname_entry.config(state='disabled')
        self.connect_btn.config(state='disabled')
        self.message_entry.config(state='normal')
        self.send_btn.config(state='normal')

        threading.Thread(target=self.receive_messages, daemon=True).start()

    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                if message == "NICKNAME":
                    self.client_socket.send(self.nickname.encode('utf-8'))
                else:
                    self.display_message(message)
            except:
                self.client_socket.close()
                break

    def send_message(self, event=None):
        message = self.message_entry.get().strip()
        if message:
            full_message = f"{self.nickname}: {message}"
            try:
                self.client_socket.send(full_message.encode('utf-8'))
            except:
                messagebox.showerror("Error", "Not connected to server.")
            self.message_entry.delete(0, tk.END)

    def display_message(self, message):
        self.chat_area.config(state='normal')
        self.chat_area.insert(tk.END, message + "\n")
        self.chat_area.config(state='disabled')
        self.chat_area.yview(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    client = ChatClient(root)
    root.mainloop()
