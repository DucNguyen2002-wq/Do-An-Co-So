import json
import os
import tkinter as tk
from tkinter import messagebox

DATA_FILE = "user_data.json"

# Hàm tiện ích để tải và lưu dữ liệu JSON
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    return {"users": {}}

def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

# Đăng nhập hoặc đăng ký
def login_or_register():
    login_window = tk.Tk()
    login_window.title("Login / Register")
    login_window.geometry("400x300")
    login_window.configure(bg="#2c2f33")

    current_user = {}

    def handle_login():
        username = username_entry.get().strip()
        password = password_entry.get().strip()

        if not username or not password:
            messagebox.showerror("Error", "Username and Password are required.")
            return

        data = load_data()
        users = data.get("users", {})

        if username in users and users[username]["password"] == password:
            current_user["username"] = username
            login_window.destroy()
        else:
            messagebox.showerror("Error", "Invalid username or password.")

    def handle_register():
        username = username_entry.get().strip()
        password = password_entry.get().strip()

        if not username or not password:
            messagebox.showerror("Error", "Username and Password are required.")
            return

        data = load_data()
        users = data.get("users", {})

        if username in users:
            messagebox.showerror("Error", "Username already exists.")
        else:
            users[username] = {"password": password, "chat_history": []}
            save_data(data)
            messagebox.showinfo("Success", "Registration successful. You can now login.")

    # Giao diện đăng nhập/đăng ký
    tk.Label(login_window, text="Username:", bg="#2c2f33", fg="#ffffff").pack(pady=10)
    username_entry = tk.Entry(login_window)
    username_entry.pack(pady=10)

    tk.Label(login_window, text="Password:", bg="#2c2f33", fg="#ffffff").pack(pady=10)
    password_entry = tk.Entry(login_window, show="*")
    password_entry.pack(pady=10)

    tk.Button(login_window, text="Login", command=handle_login, bg="#5865f2", fg="#ffffff").pack(pady=10)
    tk.Button(login_window, text="Register", command=handle_register, bg="#5865f2", fg="#ffffff").pack(pady=10)

    login_window.mainloop()
    return current_user
