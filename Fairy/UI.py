import tkinter as tk
from auth import login_or_register, load_data, save_data
from Fairy import process_message  # Import logic từ AI.py
from queue import Queue
import threading
import pyttsx3


def run_ui(current_user):
    """Giao diện chính sau khi đăng nhập."""
    root = tk.Tk()
    root.title("Fairy UI")
    root.geometry("1280x720")
    root.configure(bg="#2c2f33")

    # Khởi tạo engine Text-to-Speech
    tts_engine = pyttsx3.init()

    def speak(text):
        """Phát âm thanh từ văn bản."""
        tts_engine.say(text)
        tts_engine.runAndWait()

    # Nạp lịch sử từ file
    data = load_data()
    chat_history = data["users"][current_user["username"]]["chat_history"]

    def save_chat_history():
        """Lưu lịch sử chat của người dùng."""
        data["users"][current_user["username"]]["chat_history"] = chat_history
        save_data(data)

    def display_chat_history():
        """Hiển thị lịch sử trò chuyện trong listbox."""
        listbox_history.delete(0, tk.END)
        for entry in chat_history:
            role = "User" if entry["role"] == "user" else "Fairy"
            message = entry["parts"][0]
            listbox_history.insert(tk.END, f"{role}: {message}")

    def on_send():
        """Xử lý gửi tin nhắn."""
        user_input = textbox.get()
        if user_input.strip():
            textarea.config(state=tk.NORMAL)
            textarea.insert(tk.END, f"User: {user_input}\n")
            textarea.config(state=tk.DISABLED)
            textbox.delete(0, tk.END)
            chat_history.append({"role": "user", "parts": [user_input]})
            display_chat_history()
            save_chat_history()
            threading.Thread(target=process_and_display_response, args=(user_input,)).start()

    def process_and_display_response(user_input):
        """Xử lý và hiển thị phản hồi của AI."""
        response_queue = Queue()
        process_message(user_input, response_queue)
        while not response_queue.empty():
            response = response_queue.get()
            textarea.config(state=tk.NORMAL)
            textarea.insert(tk.END, f"{response}\n")
            textarea.config(state=tk.DISABLED)
            chat_history.append({"role": "model", "parts": [response]})
            display_chat_history()
            save_chat_history()
            threading.Thread(target=speak, args=(response,)).start()

    def on_select_history(event):
        """Hiển thị tin nhắn được chọn từ lịch sử."""
        try:
            selected_index = listbox_history.curselection()[0]
            selected_text = listbox_history.get(selected_index)
            role, message = selected_text.split(":", 1)
            textarea.config(state=tk.NORMAL)
            textarea.insert(tk.END, f"Replayed {role}: {message.strip()}\n")
            textarea.config(state=tk.DISABLED)
        except IndexError:
            print("No history item selected.")

    def play_history_audio():
        """Phát âm thanh từ lịch sử phản hồi của AI."""
        for entry in chat_history:
            if entry["role"] == "model":
                threading.Thread(target=speak, args=(entry["parts"][0],)).start()

    def logout():
        """Xử lý đăng xuất và quay lại màn hình đăng nhập."""
        save_chat_history()  # Lưu lịch sử trước khi đăng xuất
        root.destroy()  # Đóng giao diện hiện tại
        # Restart login/register screen
        new_user = login_or_register()
        if new_user:
            run_ui(new_user)

    # Canvas hiển thị banner
    canvas = tk.Canvas(root, bg="#343541", width=1280, height=60, bd=0, highlightthickness=0)
    canvas.create_text(640, 30, anchor="center", text="FAIRY", fill="#ffffff", font=("Istok Web", 34, "bold"))
    canvas.pack(side="top", fill=tk.X)

    # Khung lịch sử chat
    listbox_history = tk.Listbox(
        root, bd=0, bg="#33333d", fg="#ffffff", font=("Arial", 12), selectbackground="#5865f2", selectforeground="#ffffff"
    )
    listbox_history.pack(side="left", fill=tk.Y, padx=(10, 0), pady=(0, 10))

    # Khung hiển thị văn bản
    textarea = tk.Text(
        root, bd=0, bg="#444654", fg="#ffffff", insertbackground="#ffffff", font=("Arial", 12), wrap=tk.WORD
    )
    textarea.pack(side="top", fill=tk.BOTH, expand=True, padx=10, pady=(10, 0))
    textarea.config(state=tk.DISABLED)

    # Khung nhập liệu
    frame_input = tk.Frame(root, bg="#2c2f33")
    frame_input.pack(side="bottom", fill=tk.X, padx=10, pady=10)

    # Ô nhập liệu
    textbox = tk.Entry(
        frame_input, bd=0, bg="#40414e", fg="#ffffff", insertbackground="#ffffff", font=("Arial", 12)
    )
    textbox.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))

    # Nút bấm gửi tin nhắn
    button = tk.Button(
        frame_input, text="Send", bg="#5865f2", fg="#ffffff", font=("Arial", 12, "bold"), command=on_send
    )
    button.pack(side=tk.RIGHT)

    # Nút phát giọng nói của lịch sử
    history_button = tk.Button(
        frame_input, text="🔊 Play History", bg="#5865f2", fg="#ffffff", font=("Arial", 12, "bold"), command=play_history_audio
    )
    history_button.pack(side=tk.LEFT, padx=(0, 10))

    # Nút đăng xuất
    logout_button = tk.Button(
        frame_input, text="Logout", bg="#ff5c5c", fg="#ffffff", font=("Arial", 12, "bold"), command=logout
    )
    logout_button.pack(side=tk.LEFT, padx=(0, 10))

    # Gắn sự kiện chọn từ listbox
    listbox_history.bind("<<ListboxSelect>>", on_select_history)

    # Hiển thị lịch sử khi khởi động
    display_chat_history()
    root.mainloop()

# Main
if __name__ == "__main__":
    current_user = login_or_register()
    if current_user:
        run_ui(current_user)
