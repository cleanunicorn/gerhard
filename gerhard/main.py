from PIL import Image, ImageDraw
import argparse
import click
import time
import random

from gerhard.image_draw import draw_lines, draw_spiral
from gerhard.color_generator import gen_random, gen_proxy


@click.command(help="An image generator in the style of Gerhard Richter's Strip")
@click.option("--width", default=1920, help="width of generated image", type=int)
@click.option("--height", default=1080, help="height of generated image", type=int)
@click.option(
    "--color",
    type=click.Choice(["random", "proxy"]),
    default="random",
    help="color generator",
    show_default=True,
    required=True,
)
@click.option(
    "--color-distance",
    type=int,
    default=10,
    help="color distance in case of [--color proxy], should be between 0 - 255",
)
@click.option(
    "--random-seed",
    help="random seed to generate the same image",
    default=(int(time.time())),
)
@click.option("--output", help="file name to generate", default=None, type=str)
@click.option(
    "--method",
    help="type of image to generate",
    type=click.Choice(["lines", "spiral"]),
    required=True,
    prompt=True,
    default="lines",
)
@click.pass_context
def cli(ctx, width, height, color, color_distance, random_seed, output, method):
    ctx.ensure_object(dict)

    ctx.obj["width"] = width
    ctx.obj["height"] = height

    ctx.obj["color"] = color
    ctx.obj["color_distance"] = color_distance

    ctx.obj["random_seed"] = random_seed
    random.seed(random_seed)

    ctx.obj["output"] = (
        output if output is not None else "output-{}.png".format(random_seed)
    )

    # Init image
    im = Image.new("RGBA", (width, height), (255, 255, 255, 255))
    ctx.obj["draw"] = ImageDraw.Draw(im)

    # Color generator
    if color == "random":
        ctx.obj["color_generator"] = gen_random
    elif color == "proxy":
        ctx.obj["color_generator"] = gen_proxy

    if method == "lines":
        draw_lines(ctx)
    elif method == "spiral":
        draw_spiral(ctx)

    # Save image
    im.save(ctx.obj["output"])


if __name__ == "__main__":
    cli()
