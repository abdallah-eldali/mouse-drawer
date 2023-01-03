from enum import Enum
from PIL import Image
import networkx as nx
import matplotlib.pyplot as plt
import mouse
import time

#TODO:
# 1. Find a way to quit the events of the mouse
# 2. Only start when clicking on something
# 3. Review code + clean
# 4. Git commit everything needed and .gitignore for the images
# 5. Figure out Tkinter idea on a different script file

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
image = Image.open("result_bw.png")
image.convert("L")
width, height = image.size
print(width, height)


def pixel_in_range(pixel_position: tuple) -> bool:
    x, y = pixel_position
    return (0 <= x and x < width) and (0 <= y and y < height)

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

G = nx.DiGraph()

def follow_wall(previous_node: tuple, coming_from: Direction, current_position: tuple) -> set:
    nodes = [previous_node]

    going_to = next_directions(coming_from, current_position)

    #base case
    while going_to:
        if not going_straight(coming_from, going_to) and not previous_node == current_position:
            #create node
            new_node = current_position
            nodes.append(new_node)
            #create edges between new_node and previous_node
            G.add_edge(previous_node, new_node)
            #set previous_node = new_node
            previous_node = new_node

        #set current position as already visited
        visited.add(current_position)
        coming_from = opposite_direction(going_to)
        current_position = go_to(current_position, going_to)
        going_to = next_directions(coming_from, current_position)


    G.add_node(current_position)
    if not previous_node == current_position:
        #create edges between new_node and previous_node
        G.add_edge(previous_node, current_position)
        nodes.append(current_position)
        visited.add(current_position)

    return nodes

trees = [] #roots of trees
for y in range(height):
    for x in range(width):
        pixel = (x, y)
        if pixel_is_black(pixel) and pixel not in visited:
            trees.append(pixel)
            follow_wall(pixel, Direction.WEST, pixel)




p = {v:v for v in G.nodes}
nx.draw(G, pos=p, with_labels=False, node_size=1, width=0.1, arrows=False, arrowsize=1)
plt.show()

time.sleep(5)
ox,oy = mouse.get_position()
mouse_events = []
for tree_root in trees:
    nodes = list(nx.nodes(nx.dfs_tree(G, tree_root)))

    x, y = nodes[0]

    mouse.move(ox + x, oy + y)
    mouse.press()

    for i in range(1, len(nodes)):
        x, y = nodes[i]
        time.sleep(0.05)
        mouse.move(ox + x, oy + y)

    mouse.release()
    time.sleep(0.05)



    # root_x, root_y = tree[0]

    # # time.sleep(0.05)
    # mouse.move(ox + root_x, oy + root_y)
    # # time.sleep(0.05)
    # mouse.press()
    # for i in range(1, len(tree)):
    #     node_x, node_y = tree[i]

    #     mouse.move(ox + node_x, oy + node_y)

    # # time.sleep(0.05)
    # mouse.release()
    


    # x, y = root[0]
    # mouse.move(ox + x, oy + y)
    # mouse.press()
    # for i in range(1, len(root)):
    #     n = root[i]
    #     x, y = n
    #     mouse.move(ox + x, oy + y)

    # mouse.release()

    # current_node = root
    # x, y = current_node
    # # mouse.move(ox + x, oy + y)
    # # mouse.press()

    # children = G.successors(current_node)
    # print(children)

    # for child in children:
    #     print(child)

    # while children:
    #     child = children[0]

    #     x, y = child
    #     # mouse.move(ox + x, oy + y)

    #     current_node = child
        




"""

while there is a place to go to:
    going_to = get_direction()

    if going_straight:
        move to the new pixel
        mark it as visited

    else:
        when not going straight
        create node
        connect edge node to prev_node
        set the node as previous node



"""