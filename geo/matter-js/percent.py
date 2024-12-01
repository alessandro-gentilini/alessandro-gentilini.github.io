import svgwrite
import random
from math import pi, sqrt, sin, cos
#from shapely.geometry import box, Polygon
import shapely

def is_overlapping(polygon1, polygon2):
  """Checks if two polygons overlap.

  Args:
    polygon1: A Shapely Polygon object.
    polygon2: A Shapely Polygon object.

  Returns:
    True if the polygons overlap, False otherwise.
  """

  return polygon1.intersects(polygon2)

def generate_svg(radius, square_area_ratio, square_side_ratio):
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
    square_side_length = square_side_ratio*radius

    # Create the circle
    cx = radius
    cy = radius
    dwg.add(dwg.circle((cx, cy), radius, fill='black'))

    xy = []
    NN = 70
    for i in range(0,NN):
        x_i = cx+radius*cos(i*2*pi/NN)
        y_i = cy+radius*sin(i*2*pi/NN)
        xy.append((x_i,y_i))
    dwg.add(dwg.polygon(xy,fill='white'))
    circle_approx = shapely.Polygon(xy)

    filled_area = 0

    # Place squares randomly within the circle, avoiding overlaps
    squares = []
    while filled_area < total_square_area:
        x = cx + random.uniform(-radius,+radius)#radius * (2 * random.random() - 1)
        y = cy + random.uniform(-radius,+radius)#radius * (2 * random.random() - 1)
        L = square_side_length*random.uniform(0.8,1.2)
        sut = shapely.box(x-L/2,y-L/2,x+L/2,y+L/2)        
        #if (x-cx)**2 + (y-cy)**2 <= radius**2:  # Check if the square is within the circle
        if shapely.within(sut,circle_approx):

            square = dwg.rect((x-L/2, y-L/2),
                              (L, L), fill='black')

            overlap = False
            for existing_square in squares:
                if is_overlapping(sut,existing_square):
                    overlap = True
                    break
            if not overlap:
                squares.append(sut)
                dwg.add(square)
                filled_area = filled_area+square_side_length**2
                print(filled_area/total_square_area)

    return dwg.tostring()

# Example usage:
svg_string = generate_svg(500,.6,.15)
with open('circle_with_squares.svg', 'w') as f:
    f.write(svg_string)