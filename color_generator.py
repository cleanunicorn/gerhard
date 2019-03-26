import random
from enum import Enum


def gen_random(options):
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), 255)


def gen_proxy(options):
    r, g, b, _ = options["color"]
    return (
        random.randint(
            max(0, r - options["distance"]), min(255, r + options["distance"])
        ),
        random.randint(
            max(0, g - options["distance"]), min(255, g + options["distance"])
        ),
        random.randint(
            max(0, b - options["distance"]), min(255, b + options["distance"])
        ),
        255,
    )