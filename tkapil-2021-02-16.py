from tkinter import Tk, Canvas
from PIL import ImageTk, Image
from random import randint

window = Tk()
window.config(cursor="none")
canvas = Canvas(window, width=800, height=600)
canvas.pack()

prokop = ImageTk.PhotoImage(file="images/prokopAne.png")
cursorFile = ImageTk.PhotoImage(file="images/cursor.png")

for i in range(50):
    canvas.create_image(
        randint(0, 800),
        randint(0, 600),
        image=prokop,
        anchor="nw")


# window.config(cursor=cursorFile)
cursor = canvas.create_image(0, 0, image=cursorFile, anchor="nw")
window.bind("<Motion>", lambda e: canvas.coords(cursor, e.x, e.y))

window.mainloop()
