import os
import sys
import tkinter as tk

def load_asset(path):
    base = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    assets = os.path.join(base, "assets")
    return os.path.join(assets, path)

window = tk.Tk()
window.geometry("1433x745")
window.configure(bg="#ffffff")
window.title("ChatGPT User Interface (Community)")

canvas = tk.Canvas(
    window,
    bg = "#ffffff",
    width = 1433,
    height = 745,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x=0, y=0)
canvas.create_text(
    560,
    385,
    anchor="nw",
    text="Continue",
    fill="#FFFFFF",
    font=("Istok Web", 20 * -1)
)
button_1_image = tk.PhotoImage(file=load_asset("button.png"))

button_1 = tk.Button(
    image=button_1_image,
    relief="flat",
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_1 has been pressed!")
)

button_1.place(x=560, y=385, width=320, height=50)



textbox_1 = tk.Entry(
    bd=0,
    bg="#000000",
    fg="#FFFFFF",
    insertbackground="#FFFFFF",
    highlightthickness=0
)

textbox_1.place(x=566, y=294, width=314, height=52)

canvas.create_text(
    576,
    275,
    anchor="nw",
    text="User",
    fill="#343541",
    font=("Istok Web", 14 * -1)
)

canvas.create_text(
    555,
    187,
    anchor="nw",
    text="Welcome",
    fill="#2e3339",
    font=("Istok Web", 40 * -1)
)

window.resizable(False, False)
window.mainloop()
