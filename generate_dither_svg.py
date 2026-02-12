#!/usr/bin/env python3
"""
Generate a static SVG dithered gradient
Usage: python generate_dither_svg.py > output.svg
"""

import math

# Configuration
WIDTH = 1280
HEIGHT = 1280
PIXEL_SIZE = 6
CENTER_X = 0.5  # 50%
CENTER_Y = 1.0  # 100%
RADIAL_SCALE = 1.2
DENSITY_CURVE = 1.8

# Colors (RGB)
COLOR_INNER = (40, 120, 255)  # #2878ff
COLOR_MIDDLE = (8, 18, 46)    # #08122e
COLOR_OUTER = (0, 0, 0)       # #000000
BG_COLOR = (0, 0, 0)          # #000000

# Bayer matrix 8x8
BAYER_MATRIX = [
    [ 0, 32,  8, 40,  2, 34, 10, 42],
    [48, 16, 56, 24, 50, 18, 58, 26],
    [12, 44,  4, 36, 14, 46,  6, 38],
    [60, 28, 52, 20, 62, 30, 54, 22],
    [ 3, 35, 11, 43,  1, 33,  9, 41],
    [51, 19, 59, 27, 49, 17, 57, 25],
    [15, 47,  7, 39, 13, 45,  5, 37],
    [63, 31, 55, 23, 61, 29, 53, 21]
]

def interpolate_color(c1, c2, factor):
    """Interpolate between two RGB colors"""
    r = int(c1[0] + factor * (c2[0] - c1[0]))
    g = int(c1[1] + factor * (c2[1] - c1[1]))
    b = int(c1[2] + factor * (c2[2] - c1[2]))
    return (r, g, b)

def get_gradient_color(position):
    """Get color at normalized position (0-1)"""
    if position < 0.5:
        return interpolate_color(COLOR_INNER, COLOR_MIDDLE, position * 2)
    else:
        return interpolate_color(COLOR_MIDDLE, COLOR_OUTER, (position - 0.5) * 2)

def should_draw_pixel(grid_x, grid_y, brightness):
    """Determine if pixel should be drawn based on Bayer matrix"""
    threshold = brightness * 64
    bayer_value = BAYER_MATRIX[grid_y % 8][grid_x % 8]
    return bayer_value < threshold

def generate_svg():
    """Generate SVG with dithered gradient"""
    cx = CENTER_X * WIDTH
    cy = CENTER_Y * HEIGHT
    max_dist = math.sqrt(WIDTH**2 + HEIGHT**2) * RADIAL_SCALE
    
    # Start SVG
    print(f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">')
    
    # Background
    print(f'  <rect width="{WIDTH}" height="{HEIGHT}" fill="rgb{BG_COLOR}"/>')
    
    # Generate pixels
    print('  <g id="ditherPixels">')
    
    y = 0
    while y < HEIGHT:
        x = 0
        while x < WIDTH:
            # Calculate distance from center
            dx = x - cx
            dy = y - cy
            distance = math.sqrt(dx*dx + dy*dy)
            
            # Normalize distance
            normalized_dist = min(distance / max_dist, 1.0)
            
            # Get gradient color
            grad_color = get_gradient_color(normalized_dist)
            
            # Calculate density
            density = normalized_dist ** (1.0 / DENSITY_CURVE)
            brightness = 1.0 - density
            
            # Check if pixel should be drawn
            grid_x = int(x / PIXEL_SIZE)
            grid_y = int(y / PIXEL_SIZE)
            
            if should_draw_pixel(grid_x, grid_y, brightness):
                print(f'    <rect x="{x}" y="{y}" width="{PIXEL_SIZE}" height="{PIXEL_SIZE}" fill="rgb{grad_color}"/>')
            
            x += PIXEL_SIZE
        y += PIXEL_SIZE
    
    print('  </g>')
    print('</svg>')

if __name__ == '__main__':
    generate_svg()
