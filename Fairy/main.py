import os
import sys
import tkinter as tk
from Fairy import process_message  # Import AI processing logic
from queue import Queue
import threading

def on_send():
    """Handle the send button click."""
    user_input = textbox_1.get()
    if not user_input.strip():
        return

    textarea_1.insert(tk.END, f"User: {user_input}\n")
    textbox_1.delete(0, tk.END)

    # Start a thread to process the AI response
    threading.Thread(target=process_and_display_response, args=(user_input,)).start()

def process_and_display_response(user_input):
    """Process user input and display AI's response."""
    response_queue = Queue()

    # Call the AI processing logic
    process_message(user_input, response_queue)

    # Get the AI's response and display it in the text area
    while not response_queue.empty():
        response = response_queue.get()
        textarea_1.insert(tk.END, f"{response}\n")

# UI Setup
def load_asset(path):
    base = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    assets = os.path.join(base, "assets")
    return os.path.join(assets, path)

window = tk.Tk()
window.geometry("1432x752")
window.configure(bg="#343541")
window.title("ChatGPT User Interface (Community)")

canvas = tk.Canvas(
    window,
    bg = "#343541",
    width = 1432,
    height = 752,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x=0, y=0)

canvas.create_rectangle(0, 0, 261, 752, fill='#202123', outline="")

canvas.create_text(
    48,
    711,
    anchor="nw",
    text="Log out",
    fill="#ffffff",
    font=("Inter", 13 * -1)
)

image_1 = tk.PhotoImage(file=load_asset("frame_1/1.png"))

canvas.create_image(24, 717, image=image_1)

image_2 = tk.PhotoImage(file=load_asset("frame_1/2.png"))

canvas.create_image(31, 716, image=image_2)

image_3 = tk.PhotoImage(file=load_asset("frame_1/3.png"))

canvas.create_image(30, 717, image=image_3)

canvas.create_line(8, 545, 252, 545, fill="#000000", width=1.0)

canvas.create_rectangle(8, 66, 252, 111, fill='#343540', outline="")

canvas.create_text(
    49,
    25,
    anchor="nw",
    text="New chat",
    fill="#ffffff",
    font=("Inter", 13 * -1)
)

image_4 = tk.PhotoImage(file=load_asset("frame_1/4.png"))

canvas.create_image(29, 31, image=image_4)

image_5 = tk.PhotoImage(file=load_asset("frame_1/5.png"))

canvas.create_image(29, 31, image=image_5)

canvas.create_rectangle(8, 9, 252, 54, fill='#000000', outline="#444654", width="1.0")

canvas.create_text(
    49,
    82,
    anchor="nw",
    text="Chatbot definition expl",
    fill="#ececf1",
    font=("Inter", 13 * -1)
)

image_6 = tk.PhotoImage(file=load_asset("frame_1/6.png"))

canvas.create_image(28, 88, image=image_6)

image_7 = tk.PhotoImage(file=load_asset("frame_1/7.png"))

canvas.create_image(215, 93, image=image_7)

image_8 = tk.PhotoImage(file=load_asset("frame_1/8.png"))

canvas.create_image(211, 87, image=image_8)

canvas.create_text(
    48,
    557,
    anchor="nw",
    text="Clear conversations",
    fill="#ffffff",
    font=("Inter", 13 * -1)
)

image_9 = tk.PhotoImage(file=load_asset("frame_1/9.png"))

canvas.create_image(236, 84, image=image_9)

image_10 = tk.PhotoImage(file=load_asset("frame_1/10.png"))

canvas.create_image(236, 88, image=image_10)

image_11 = tk.PhotoImage(file=load_asset("frame_1/11.png"))

canvas.create_image(235, 88, image=image_11)

image_12 = tk.PhotoImage(file=load_asset("frame_1/12.png"))

canvas.create_image(237, 88, image=image_12)

image_13 = tk.PhotoImage(file=load_asset("frame_1/13.png"))

canvas.create_image(28, 558, image=image_13)

image_14 = tk.PhotoImage(file=load_asset("frame_1/14.png"))

canvas.create_image(27, 562, image=image_14)

image_15 = tk.PhotoImage(file=load_asset("frame_1/15.png"))

canvas.create_image(26, 564, image=image_15)

image_16 = tk.PhotoImage(file=load_asset("frame_1/16.png"))

canvas.create_image(29, 564, image=image_16)

# Entry Box for User Input
textbox_1 = tk.Entry(
    window,
    bd=0,
    bg="#40414e",
    fg="#ffffff",
    insertbackground="#ffffff",
    highlightthickness=0,
    font=("Arial", 12),
)
textbox_1.place(x=10, y=530, width=680, height=40)

# Text Area for Chat
textarea_1 = tk.Text(
    window,
    bd=0,
    bg="#444654",
    fg="#ffffff",
    insertbackground="#ffffff",
    highlightthickness=0,
    font=("Arial", 12),
    wrap=tk.WORD,
)
textarea_1.place(x=10, y=10, width=780, height=500)
textarea_1.config(state=tk.NORMAL)

# Send Button
button_1 = tk.Button(
    window,
    text="Send",
    bg="#5865f2",
    fg="#ffffff",
    font=("Arial", 12, "bold"),
    command=on_send,
)
button_1.place(x=700, y=530, width=80, height=40)

canvas.create_text(
    734,
    32,
    anchor="nw",
    text="FAIRY",
    fill="#ffffff",
    font=("Istok Web", 34 * -1)
)

image_18 = tk.PhotoImage(file=load_asset("frame_1/18.png"))

canvas.create_image(1367, 128, image=image_18)

image_19 = tk.PhotoImage(file=load_asset("frame_1/19.png"))

canvas.create_image(1395, 128, image=image_19)

canvas.create_text(
    329,
    121,
    anchor="nw",
    text="A chatbot is a computer program that simulates human conversation through voice commands or text chats or both. It can be integrated with various messaging platforms like Facebook Messenger, WhatsApp, WeChat, etc. and can be used for a variety of purposes, such as customer service, entertainment, and e-commerce.\n",
    fill="#ffffff",
    font=("Inter", 15 * -1)
)

window.resizable(False, False)
window.mainloop()
