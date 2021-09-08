from tkinter import Tk, Canvas, Scale, Button, HORIZONTAL

class Dummy:
    pass

mouse = Dummy()
mouse.width = 1
mouse.color = "#000000"

def move(e):
    if getattr(mouse, "pressed", False):
        canvas.create_line(getattr(mouse, "x", e.x), getattr(mouse, "y", e.y), e.x, e.y, width=mouse.width, fill=mouse.color)
        mouse.x = e.x 
        mouse.y = e.y
    else:
        mouse.x = e.x
        mouse.y = e.y

def wheel(e):
    if e.delta > 0:
        mouse.width += 1
    else:
        mouse.width = max(mouse.width-1, 1)

def rgbToHex(r,g,b):
    out = '#%02x%02x%02x' % (r,g,b)
    return out

def setColor():
    mouse.color = rgbToHex(rgb[0].get(),rgb[1].get(), rgb[2].get())


window = Tk()
window.title("Okno")
canvas = Canvas(window, width=800, height=600, background="white")
canvas.pack()
rgb = [Scale(window, from_=0, to=255, orient=HORIZONTAL), Scale(window, from_=0, to=255, orient=HORIZONTAL), Scale(window, from_=0, to=255, orient=HORIZONTAL)]
for i in rgb:
    i.pack()
Button(window, text="Barva", command=setColor).pack()

#canvas.create_line(0,0,800,600, fill="#EEE", width=5)

window.bind("<Motion>", move)
window.bind("<Button-1>", lambda e: setattr(mouse,"pressed",True))
window.bind("<ButtonRelease-1>", lambda e: setattr(mouse,"pressed",False))
window.bind("<KeyPress-space>", lambda e: canvas.create_rectangle(0,0,800,600, fill="white", width=0))
window.bind("<MouseWheel>", wheel)
window.mainloop()