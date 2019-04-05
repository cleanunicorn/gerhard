from PIL import Image, ImageDraw
import argparse
from color_generator import *
import time

# Parse arguments
cli_args = argparse.ArgumentParser(
    description="A generator in the style of Gerhard Richter's Strip. "
)

# Size
cli_args.add_argument(
    "--width", help="Width of generated image", default=1920, type=int
)
cli_args.add_argument(
    "--height", help="Height of the generated image", default=1080, type=int
)

# Color generator
cli_args.add_argument(
    "--color",
    help="Color generator",
    default="random",
    type=str,
    choices=["random", "proxy"],
)
cli_args.add_argument(
    "--color-distance",
    help="Color distance (0 - 255) if --color is `proxy`",
    default=10,
    type=int,
)
cli_args.add_argument(
    "--color-random-seed",
    help="Random seed for color generator",
    default=int(time.time()),
    type=int,
)

# Draw type
cli_args.add_argument(
    "--method",
    help="Method to generate",
    default="line",
    type=str,
    choices=["line", "spiral"]
)

# Output
cli_args.add_argument("--output", help="File name to generate", default="output.png")

# Parse arguments
cli = cli_args.parse_args()

# Size
width = cli.width
height = cli.height

# Color generator
color_generator = cli.color
if color_generator == "random":
    color_generator = gen_random
elif color_generator == "proxy":
    color_generator = gen_proxy
color_distance = cli.color_distance
print("Using random seed: {}".format(cli.color_random_seed))
random.seed(cli.color_random_seed)

# Output
output_file = cli.output

# Init canvas
im = Image.new("RGBA", (width, height), (255, 255, 255, 255))
draw = ImageDraw.Draw(im)

color = gen_random({})
# Generate lines
if cli.method == "line":
    for x in range(height):
        color = color_generator({"color": color, "distance": color_distance})
        draw.rectangle([0, x, width, x], fill=color, outline=color)
elif cli.method == "spiral":
    done = False
    x = int(width / 2)
    y = int(height / 2)
    min_x, max_x = x, x
    min_y, max_y = y, y
    direction = 0
    while done == False:
        color = color_generator({"color": color, "distance": color_distance})
        draw.point([(x, y)], color)
        # Move
        if direction == 0:
            x += 1
            if x > max_x:
                direction += 1
                max_x = x
        elif direction == 1:
            y += 1
            if y > max_y:
                direction += 1
                max_y = y
        elif direction == 2:
            x -= 1
            if x < min_x:
                direction += 1
                min_x = x
        elif direction == 3:
            y -= 1
            if y < min_y:
                direction += 1
                min_y = y
        direction = direction % 4
        if x < 0 or y < 0 or x > width or y > height:
            done = True

# Save image
im.save(output_file)
