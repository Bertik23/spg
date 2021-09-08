from tkinter import Tk, Canvas
from PIL import ImageTk, Image, ImageDraw, ImageFont
import random
from math import sin, cos, pi

W, H = 512, 512
img = Image.new("RGBA", (W, H))
imgDraw = ImageDraw.Draw(img)

font = ImageFont.truetype("fonts/Roboto-Regular.ttf", 128)

lineWidth = int(W/10)
print(lineWidth)
b = lineWidth/2

outlines = [
    "circle",
    [(b, b), (b, H-b), (W-b, H-b), (W-b, b)],
    [(b, b), (W/2, H-b), (W-b, b)],
    [(W-b, H-b), (W/2, b), (b, H-b)]
]

fillColors = [
    "blue",
    "white"
]

outlineColors = [
    "red",
    "blue"
]

inSigns = [
    ""
    "number",
    "text"
]

outline = random.choice(outlines)
fillColor = random.choice(fillColors)
outlineColor = random.choice(outlineColors)
inSign = random.choice(inSigns)
cancel = random.choice([True, False])

# inSign = "number"
# outline = outlines[0]
# cancel = True


if outline == "circle":
    imgDraw.ellipse(
        [(b, b), (W-b, H-b)], outline=outlineColor, width=lineWidth,
        fill=fillColor
    )
else:
    imgDraw.polygon(outline, fill=fillColor)
    imgDraw.line(outline+[outline[0]], fill=outlineColor, width=lineWidth)
    for point in outline+[outline[0]]:
        imgDraw.ellipse(
            (point[0] - lineWidth/2, point[1] - lineWidth/2,
             point[0] + lineWidth/2, point[1] + lineWidth/2),
            fill=outlineColor
        )

if inSign == "number":
    p = 0
    if outline == "circle":
        p = 0
    if outlines.index(outline) == 2:
        p = -b*2
        # font = ImageFont.truetype("fonts/Roboto-Regular.ttf", 128)
    if outlines.index(outline) == 3:
        p = b*2
        # font = ImageFont.truetype("fonts/Roboto-Regular.ttf", 128)
    num = str(random.randint(0, 100))
    w, h = imgDraw.textsize(num, font=font)
    imgDraw.text(((W-w)/2, (H-h)/2+p), num, fill="black", font=font)
    # imgDraw.text((64, 64), num, anchor="mm", font=font)

if cancel:
    if outline == "circle":
        u = -3/4*pi
        cancelLines = [(W/2 - (W-b/2)*sin(u), H/2 - (H-b/2)*sin(u)),
                       (W/2 + (W-b/2)*cos(u), H/2 + (H-b/2)*cos(u))]
        print(cancelLines)
        imgDraw.line(cancelLines, fill=outlineColor, width=int(lineWidth/2))

window = Tk()
canvas = Canvas(width=W, height=H)
canvas.pack()

znacka = ImageTk.PhotoImage(image=img)

canvas.create_image(
    0, 0,
    image=znacka,
    anchor="nw"
)

window.mainloop()
