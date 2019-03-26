from PIL import Image, ImageDraw
import random

# size of image
width, height = (800, 600)
canvas = (width, height)

# init canvas
im = Image.new("RGBA", canvas, (255, 255, 255, 255))
draw = ImageDraw.Draw(im)

# lines rectangles
for x in range(height):
    color = (
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
        255,
    )
    draw.rectangle([0, x, width, x], fill=color, outline=color)

# save image
im.save("./im.png")
