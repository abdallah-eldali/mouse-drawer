from enum import Enum
from PIL import Image
import networkx as nx
import matplotlib.pyplot as plt

class Direction(Enum):
    NORTH = (0, -1)
    NORTHEAST = (1, -1)
    EAST = (1, 0)
    SOUTHEAST = (1, 1)
    SOUTH = (0, 1)
    SOUTHWEST = (-1, 1)
    WEST = (-1, 0)
    NORTHWEST = (-1, -1)

directions = []
direction_index = {}
for index, direction in enumerate(Direction):
    directions.append(direction)
    direction_index[direction] = index

visited = set()    #create a set (O(1) for retrievel according to stackoverflow) of already visited pixels
image = Image.open("test_c.png")
image.convert("L")
width, height = image.size
print(width, height)


def pixel_in_range(pixel_position: tuple) -> bool:
    x, y = pixel_position
    return (0 < x and x < width) and (0 < y and y < height)

def pixel_is_black(pixel_position: tuple) -> bool:
    return image.getpixel(pixel_position) == 0

def already_visited(pixel_position: tuple) -> bool:
    return pixel_position in visited

def go_to(current_position: tuple, going_to: Direction) -> tuple:
    return tuple(sum(x) for x in zip(current_position, going_to.value)) #adds the two tuples element-wise

def is_a_wall(current_position: tuple, direction: Direction) -> bool:
    #get pixel coordinates
    new_position = go_to(current_position, direction)

    #check if out-range in the image
    #check if it's not a black pixel
    #check if we already visited it
    return not pixel_in_range(new_position) or not pixel_is_black(new_position) or already_visited(new_position)

def next_directions(coming_from: Direction, current_position: tuple) -> Direction:
    #get the index of the directions were are coming from
    i = direction_index[coming_from]

    #loop over all directions on the circular list of directions
    for j in range(1, len(directions)):
        new_direction = directions[(i+j) % len(directions)]

        #if not a wall, then return the new direction
        if not is_a_wall(current_position, new_direction):
            return new_direction

    return None

def going_straight(coming_from: Direction, going_to: Direction) -> bool:
    index = direction_index[coming_from]

    opposite_direction_index = int((index + len(directions)/2) % len(directions))
    
    return directions[opposite_direction_index] == going_to

def opposite_direction(direction: Direction) -> Direction:
    #get index of direction
    index = direction_index[direction]

    #get the opposite index (i.e.: the index in the opposite side of the circle/cardinal compass)
    opposite_direction_index = int((index + len(directions)/2) % len(directions))

    return directions[opposite_direction_index]

G = nx.Graph()

def follow_wall(previous_node: tuple, coming_from: Direction, current_position: tuple) -> None:
    going_to = next_directions(coming_from, current_position)

    #base case
    if not going_to:
        return

    if not going_straight(coming_from, going_to):
        #create node
        new_node = current_position
        #create edges between new_node and previous_node
        G.add_edge(previous_node, new_node)
        #set previous_node = new_node
        previous_node = new_node

    #set current position as already visited
    visited.add(current_position)
    follow_wall(previous_node, opposite_direction(going_to), go_to(current_position, going_to))

found_first_pixel = False

#TODO: Change this to make it so we find other pixels that haven't been visited before
for y in range(height):
    for x in range(width):
        if pixel_is_black((x, y)):
            follow_wall((x, y), Direction.WEST, (x, y))
            found_first_pixel = True
            break
    
    if found_first_pixel:
        break
            

p = {v:v for v in G.nodes}
print(p)
nx.draw(G, pos=p, with_labels=False, node_size=1, width=0.1)
plt.show()