#!/usr/bin/env python3
"""
Generate an optimized static SVG dithered radial gradient
Usage:
    python generate_dither_svg.py > output.svg
"""

import math
import random

# ===============================
# Configuration
# ===============================

WIDTH = 1280
HEIGHT = 1280
PIXEL_SIZE = 8

CENTER_X = 0.5      # 0–1
CENTER_Y = 1.0      # slightly below frame for cinematic feel
RADIAL_SCALE = 0.8
DENSITY_CURVE = 2.0
BRIGHTNESS_CURVE = 1.2

NOISE_AMOUNT = 0     # 0 to disable

# Colors (RGB)
COLOR_INNER = (40, 120, 255)   # #2878ff
COLOR_MIDDLE = (8, 18, 46)     # #08122e
COLOR_OUTER = (21, 21, 21)     # #151515
BG_COLOR = (21, 21, 21)        # #151515

# 8x8 Bayer Matrix
BAYER_MATRIX = [
    [ 0,32, 8,40, 2,34,10,42],
    [48,16,56,24,50,18,58,26],
    [12,44, 4,36,14,46, 6,38],
    [60,28,52,20,62,30,54,22],
    [ 3,35,11,43, 1,33, 9,41],
    [51,19,59,27,49,17,57,25],
    [15,47, 7,39,13,45, 5,37],
    [63,31,55,23,61,29,53,21]
]

# ===============================
# Utility Functions
# ===============================

def rgb_to_hex(color):
    return "#%02x%02x%02x" % color

def interpolate(c1, c2, t):
    return (
        int(c1[0] + t * (c2[0] - c1[0])),
        int(c1[1] + t * (c2[1] - c1[1])),
        int(c1[2] + t * (c2[2] - c1[2]))
    )

def get_gradient_color(position):
    if position < 0.5:
        return interpolate(COLOR_INNER, COLOR_MIDDLE, position * 2)
    return interpolate(COLOR_MIDDLE, COLOR_OUTER, (position - 0.5) * 2)

def should_draw_pixel(grid_x, grid_y, brightness):
    threshold = brightness * 64
    bayer_value = BAYER_MATRIX[grid_y % 8][grid_x % 8]
    return bayer_value < threshold

# ===============================
# SVG Generation
# ===============================

def generate_svg():
    cx = CENTER_X * WIDTH
    cy = CENTER_Y * HEIGHT

    max_dist = math.sqrt(WIDTH**2 + HEIGHT**2) * RADIAL_SCALE
    inv_max_dist = 1.0 / max_dist

    print(f'<svg xmlns="http://www.w3.org/2000/svg" '
          f'width="{WIDTH}" height="{HEIGHT}" '
          f'viewBox="0 0 {WIDTH} {HEIGHT}">')

    print(f'  <rect width="100%" height="100%" fill="{rgb_to_hex(BG_COLOR)}"/>')
    print('  <g shape-rendering="crispEdges">')

    y = 0
    while y < HEIGHT:

        current_color = None
        run_start_x = None

        x = 0
        while x < WIDTH:

            dx = x - cx
            dy = y - cy
            dist = math.sqrt(dx*dx + dy*dy)
            normalized = min(dist * inv_max_dist, 1.0)

            grad_color = get_gradient_color(normalized)

            density = normalized ** (1.0 / DENSITY_CURVE)
            brightness = (1.0 - density) ** BRIGHTNESS_CURVE

            if NOISE_AMOUNT > 0:
                brightness += (random.random() - 0.5) * NOISE_AMOUNT
                brightness = max(0.0, min(1.0, brightness))

            grid_x = x // PIXEL_SIZE
            grid_y = y // PIXEL_SIZE

            draw = should_draw_pixel(grid_x, grid_y, brightness)

            if draw:
                hex_color = rgb_to_hex(grad_color)

                if current_color is None:
                    current_color = hex_color
                    run_start_x = x

                elif current_color != hex_color:
                    # flush previous run
                    width = x - run_start_x
                    print(f'    <rect x="{run_start_x}" y="{y}" '
                          f'width="{width}" height="{PIXEL_SIZE}" '
                          f'fill="{current_color}"/>')
                    current_color = hex_color
                    run_start_x = x
            else:
                if current_color is not None:
                    width = x - run_start_x
                    print(f'    <rect x="{run_start_x}" y="{y}" '
                          f'width="{width}" height="{PIXEL_SIZE}" '
                          f'fill="{current_color}"/>')
                    current_color = None

            x += PIXEL_SIZE

        # flush row end
        if current_color is not None:
            width = WIDTH - run_start_x
            print(f'    <rect x="{run_start_x}" y="{y}" '
                  f'width="{width}" height="{PIXEL_SIZE}" '
                  f'fill="{current_color}"/>')

        y += PIXEL_SIZE

    print('  </g>')
    print('</svg>')


if __name__ == "__main__":
    generate_svg()
