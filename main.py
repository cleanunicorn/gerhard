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

# Generate lines
color = gen_random({})
for x in range(height):
    color = color_generator({"color": color, "distance": color_distance})
    draw.rectangle([0, x, width, x], fill=color, outline=color)

# Save image
im.save(output_file)
