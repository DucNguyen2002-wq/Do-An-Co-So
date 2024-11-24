import tkinter as tk
from Fairy import process_message, load_history  # Import logic từ AI.py
from queue import Queue
import threading

# Giao diện cơ bản
def run_ui():
    root = tk.Tk()
    root.title("ChatGPT UI")
    root.geometry("1280x940")
    root.configure(bg="#2c2f33")

    # Nạp lịch sử từ file
    chat_history = load_history()

    # Hiển thị lịch sử trong `textarea_1`
    def display_chat_history():
        """Hiển thị lịch sử trò chuyện trong textarea_1."""
        textarea_1.config(state=tk.NORMAL)
        textarea_1.delete(1.0, tk.END)  # Xóa nội dung cũ

        for entry in chat_history:
            role = "User" if entry["role"] == "user" else "Fairy"
            message = entry["parts"][0]
            textarea_1.insert(tk.END, f"{role}: {message}\n")

        textarea_1.config(state=tk.DISABLED)

    # Nút gửi
    def on_send():
        user_input = textbox.get()
        if user_input.strip():
            # Hiển thị tin nhắn người dùng
            textarea.config(state=tk.NORMAL)
            textarea.insert(tk.END, f"User: {user_input}\n")
            textarea.config(state=tk.DISABLED)
            textbox.delete(0, tk.END)

            # Thêm tin nhắn vào lịch sử
            chat_history.append({"role": "user", "parts": [user_input]})
            display_chat_history()  # Cập nhật `textarea_1`

            # Start a thread to process the AI response
            threading.Thread(target=process_and_display_response, args=(user_input,)).start()

    def process_and_display_response(user_input):
        """Xử lý tin nhắn và hiển thị phản hồi của AI."""
        response_queue = Queue()

        # Gửi tin nhắn đến AI và lấy phản hồi
        process_message(user_input, response_queue)

        while not response_queue.empty():
            response = response_queue.get()

            # Hiển thị phản hồi AI
            textarea.config(state=tk.NORMAL)
            textarea.insert(tk.END, f"{response}\n")
            textarea.config(state=tk.DISABLED)

            # Thêm phản hồi AI vào lịch sử
            chat_history.append({"role": "model", "parts": [response]})
            display_chat_history()  # Cập nhật `textarea_1`

    # Vùng hiển thị văn bản (toàn bộ chat hiện tại)
    textarea = tk.Text(
        root,
        bd=0,
        bg="#444654",
        fg="#ffffff",
        insertbackground="#ffffff",
        highlightthickness=0,
        font=("Arial", 12),
        wrap=tk.WORD,
    )
    textarea.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    # Vùng hiển thị lịch sử chat
    textarea_1 = tk.Text(
        root,
        bd=0,
        bg="#33333d",
        fg="#ffffff",
        insertbackground="#ffffff",
        highlightthickness=0,
        font=("Arial", 12),
        wrap=tk.WORD,
    )
    textarea_1.pack(side="left", padx=10, pady=10, fill=tk.Y)

    # Khung nhập liệu
    frame_input = tk.Frame(root, bg="#2c2f33")
    frame_input.pack(padx=10, pady=10, fill=tk.X)

    # Ô nhập liệu
    textbox = tk.Entry(
        frame_input,
        bd=0,
        bg="#40414e",
        fg="#ffffff",
        insertbackground="#ffffff",
        highlightthickness=0,
        font=("Arial", 12),
    )
    textbox.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))

    # Nút bấm
    button = tk.Button(
        frame_input,
        text="Send",
        bg="#5865f2",
        fg="#ffffff",
        font=("Arial", 12, "bold"),
        command=on_send,
    )
    button.pack(side=tk.RIGHT)

    # Hiển thị lịch sử khi khởi động
    display_chat_history()

    root.mainloop()

run_ui()
