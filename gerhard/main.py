from PIL import Image, ImageDraw
import argparse
import click
import time

from gerhard.color_generator import *

@click.command(help="An image generator in the style of Gerhard Richter's Strip")
@click.option("--width", default=1920, help="width of generated image", type=int)
@click.option("--height", default=1080, help="height of generated image", type=int)
@click.option("--color", type=click.Choice(["random", "proxy"]), default="random", help="color generator", show_default=True, required=True)
@click.option("--color-distance", type=int, default=10, help="color distance in case of [--color proxy], should be between 0 - 255")
@click.option("--random-seed", help="random seed to generate the same image", default=(int(time.time())))
@click.option("--output", help="file name to generate", default=None, type=str)
@click.option("--method", help="type of image to generate", type=click.Choice(["lines", "spiral"]), required=True, prompt=True, default="lines")
@click.pass_context
def cli(ctx, width, height, color, color_distance, random_seed, output, method):
    ctx.ensure_object(dict)

    ctx.obj['width'] = width
    ctx.obj['height'] = height

    ctx.obj['color'] = color
    ctx.obj['color_distance'] = color_distance
    
    ctx.obj['random_seed'] = random_seed
    random.seed(random_seed)
    
    ctx.obj['output'] = output if output is not None else "output-{}.png".format(random_seed)

    # Init image
    im = Image.new("RGBA", (width, height), (255, 255, 255, 255))
    ctx.obj['draw'] = ImageDraw.Draw(im)

    # Color generator
    if color == 'random':
        ctx.obj['color_generator'] = gen_random
    elif color == 'proxy':
        ctx.obj['color_generator'] = gen_proxy

    if method == "lines":
        draw_lines(ctx)
    elif method == "spiral":
        draw_spiral(ctx)

    # Save image
    im.save(ctx.obj['output'])

def draw_lines(ctx):
    color_generator = ctx.obj['color_generator']
    color_distance = ctx.obj['color_distance']
    draw = ctx.obj['draw']

    width = ctx.obj['width']
    height = ctx.obj['height']

    click.echo("lines")
    click.echo(ctx.obj)
    color = gen_random({})
    for x in range(height):
        color = color_generator({"color": color, "distance": color_distance})
        draw.rectangle([0, x, width, x], fill=color, outline=color)


def draw_spiral(ctx):
    click.echo("spiral")
    click.echo(ctx.obj)

if __name__ == '__main__':
    cli()

# color = gen_random({})
# # Generate lines
# @click.command()
# def line():
#     for x in range(height):
#         color = color_generator({"color": color, "distance": color_distance})
#         draw.rectangle([0, x, width, x], fill=color, outline=color)

# def spiral():
#     # Color generator set to proxy
#     color_generator = gen_proxy
#     done = False
#     x = int(width / 2)
#     y = int(height / 2)
#     min_x, max_x = x, x
#     min_y, max_y = y, y
#     direction = 0
#     while done == False:
#         color = color_generator({"color": color, "distance": color_distance})
#         draw.point([(x, y)], color)
#         # Move
#         if direction == 0:
#             x += 1
#             if x > max_x:
#                 direction += 1
#                 max_x = x
#         elif direction == 1:
#             y += 1
#             if y > max_y:
#                 direction += 1
#                 max_y = y
#         elif direction == 2:
#             x -= 1
#             if x < min_x:
#                 direction += 1
#                 min_x = x
#         elif direction == 3:
#             y -= 1
#             if y < min_y:
#                 direction += 1
#                 min_y = y
#         direction = direction % 4
#         if x < 0 or y < 0 or x > width or y > height:
#             done = True

# # Save image
# im.save(output_file)
