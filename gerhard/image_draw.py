from gerhard.color_generator import gen_random


def draw_lines(ctx):
    color_generator = ctx.obj["color_generator"]
    color_distance = ctx.obj["color_distance"]
    draw = ctx.obj["draw"]

    width = ctx.obj["width"]
    height = ctx.obj["height"]

    color = gen_random({})
    for x in range(height):
        color = color_generator({"color": color, "distance": color_distance})
        draw.rectangle([0, x, width, x], fill=color, outline=color)


def draw_spiral(ctx):
    color_generator = ctx.obj["color_generator"]
    color_distance = ctx.obj["color_distance"]
    draw = ctx.obj["draw"]

    width = ctx.obj["width"]
    height = ctx.obj["height"]

    color = gen_random({})

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
