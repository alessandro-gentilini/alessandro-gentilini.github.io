import svgwrite
import random
from math import pi, sqrt

def generate_svg(radius, square_area_ratio=0.1):
    """Generates an SVG with a circle and non-overlapping squares.

    Args:
        radius: The radius of the circle.
        square_area_ratio: The ratio of the total square area to the circle area.

    Returns:
        The SVG string.
    """

    dwg = svgwrite.Drawing('circle_with_squares.svg', size=(2*radius, 2*radius))

    # Calculate the total area of the circle
    circle_area = pi * radius**2

    # Calculate the total area of the squares
    total_square_area = circle_area * square_area_ratio

    # Estimate the number of squares based on the total square area
    # Assuming square sides are equal, we can calculate the side length
    square_side_length = sqrt(total_square_area)
    num_squares = int(total_square_area / square_side_length**2)

    # Create the circle
    cx = radius
    cy = radius
    dwg.add(dwg.circle((cx, cy), radius, fill='lightblue'))

    # Place squares randomly within the circle, avoiding overlaps
    squares = []
    while len(squares) < num_squares:
        x = radius * (2 * random.random() - 1)
        y = radius * (2 * random.random() - 1)
        if (x-cx)**2 + (y-cy)**2 <= radius**2:  # Check if the square is within the circle
            square = dwg.rect((x - square_side_length/2, y - square_side_length/2),
                              (square_side_length, square_side_length), fill='red')
            overlap = False
            for existing_square in squares:
                if square.intersect(existing_square):
                    overlap = True
                    break
            if not overlap:
                squares.append(square)
                dwg.add(square)

    return dwg.tostring()

# Example usage:
svg_string = generate_svg(100)
with open('circle_with_squares.svg', 'w') as f:
    f.write(svg_string)