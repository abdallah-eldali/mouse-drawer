from PIL import Image
import networkx as nx
import matplotlib.pyplot as plt
import mouse
import time
from compass import *
from multiprocessing import Process
import keyboard
import pyautogui

pyautogui.FAILSAFE = False

# TODO:
# 1. Find a way to quit the events of the mouse
# 2. Only start when clicking on something
# 3. Review code + clean
# 4. Git commit everything needed and .gitignore for the images
# 5. Figure out Tkinter idea on a different script file


class MouseDraw:
    def __init__(self, image: Image, image_path: str = None) -> None:
        self.__visited_pixels = set()  # set of already visited pixels in the image
        self.__image = image    # TODO check if the image is valid (i.e.: an Image object)
        self.__image_width, self.__image_height = image.size
        self.__graph = nx.DiGraph()
        self.__linked_lists = self.__create_linked_list_trees()

    def __is_pixel_in_range(self, position: tuple[int]) -> bool:
        x, y = position
        return (0 <= x < self.__image_width) and (0 <= y < self.__image_height)

    def __is_pixel_black(self, position: tuple[int]) -> bool:
        return self.__image.getpixel(position) == 0

    @staticmethod
    def __next_pixel(from_position: tuple[int], to_direction: Direction) -> tuple[int]:
        return tuple(sum(elem) for elem in zip(from_position, to_direction.value))  # adds the two tuples element-wise

    def __is_direction_a_wall(self, from_position: tuple[int], to_direction: Direction) -> bool:
        next_pixel = self.__next_pixel(from_position, to_direction)

        return not self.__is_pixel_in_range(next_pixel) or \
            not self.__is_pixel_black(next_pixel) or \
            next_pixel in self.__visited_pixels

    def __next_direction(self, from_direction: Direction, current_position: tuple[int]) -> Direction:
        # iterate over all the cardinal directions and choose the one without a wall
        for direction in get_cardinal_points_from(from_direction):
            if not self.__is_direction_a_wall(current_position, direction):
                return direction

        # if no directions has been found that isn't a wall, then return None
        return None

    @staticmethod
    def __going_straight(from_direction: Direction, to_direction: Direction) -> bool:
        return are_opposite(from_direction, to_direction)

    def __follow_wall(self, from_direction: Direction, current_position: tuple[int]) -> None:
        previous_position = current_position
        while to_direction := self.__next_direction(from_direction, current_position):  # walrus operator
            if not self.__going_straight(from_direction, to_direction) and not current_position == previous_position:
                # create node
                new_node = current_position
                # create edges between the new node and the previous node (note: nodes = positions in this graph)
                self.__graph.add_edge(previous_position, new_node)
                # set the previous position as the current position
                previous_position = current_position

            # set the current position as already visited
            self.__visited_pixels.add(current_position)
            # set the new position
            current_position = self.__next_pixel(current_position, to_direction)
            # set the direction we came from
            from_direction = opposite_direction(to_direction)

        # at this point, we no longer have anywhere else to go to
        self.__graph.add_node(current_position)
        if not previous_position == current_position:
            self.__graph.add_edge(previous_position, current_position)
            self.__visited_pixels.add(current_position)

    # since each tree only has one child and one parent this graph is just a bunch of linked lists bundled together
    def __create_linked_list_trees(self) -> list[list[tuple[int]]]:
        tree_roots = []  # list of the roots of each spanning tree
        for y in range(self.__image_height):
            for x in range(self.__image_width):
                pixel_position = (x, y)
                if self.__is_pixel_black(pixel_position) and pixel_position not in self.__visited_pixels:
                    tree_roots.append(pixel_position)
                    self.__follow_wall(Direction.WEST, pixel_position)

        linked_lists = []  # lists of linked-lists
        for tree_root in tree_roots:
            linked_lists.append(list(nx.nodes(nx.dfs_tree(self.__graph, tree_root))))

        return linked_lists

    def __draw_from_bg(self, x: int, y: int) -> None:
        print("DEBUG STARTING TO DRAW")
        for linked_list in self.__linked_lists:
            # from 0..N-1
            for i in range(len(linked_list) - 1):
                if keyboard.is_pressed('esc'):
                    print("Stop drawing")
                    return

                start_x, start_y = linked_list[i]
                end_x, end_y = linked_list[i+1]

                mouse.drag(start_x + x, start_y + y, end_x + x, end_y + y)
                time.sleep(0.00001)



            """            
            first_pixel_x, first_pixel_y = linked_list[0]
            start_x, start_y = x + first_pixel_x, y + first_pixel_y
            print(start_x, start_y)

            # from 1 ... N
            for pixel in linked_list[1:]:
                if keyboard.is_pressed('esc'):
                    print("Stop drawing")
                    return
                end_x, end_y = pixel
                print(end_x, end_y)
                mouse.drag(start_x, start_y, end_x, end_y)
                start_x, start_y = end_x, end_y
                break
            break
            
            """



            # move to the first pixel in the list and keep pressing the left button of the mouse
            # px, py = linked_list[0]
            # mouse.move(x + px, y + py)

            # iterate over the rest of the pixels and move to those while still pressing
            # for pixel in linked_list[1:]:
            #     # NOTE: This is checked to stop the drawing, multiprocessing seems to have too much overhead
            #     if keyboard.is_pressed('esc'):
            #         print("Stop drawing")
            #         return
            #     px, py = pixel
            #     time.sleep(0.025)    # this is needed since if the mouse goes too fast, the drawing won't work
            #     mouse.move(x + px, y + py)

            # release the mouse pressing and sleep
            # mouse.release()
            # time.sleep(0.025)

    @staticmethod
    def __stop_drawing():
        while not keyboard.is_pressed('esc'):
            print("Not pressing 'esc'")
            continue

        print("Pressed 'esc'... exiting")
        exit(0)

    def draw_from(self, x: int, y: int) -> None:
        # bg = Process(target=test)
        # # bg.daemon = True
        # print("STARTING THE BG PROCESS")
        # bg.start()
        #
        # print("STARTING THE LISTENING")
        # while bg.is_alive():
        #     if keyboard.is_pressed('esc'):
        #         print("No 'esc'")
        #         bg.terminate()
        self.__draw_from_bg(x, y)


    def view_graph(self) -> None:
        nx.draw(self.__graph,
                pos={position: position for position in self.__graph.nodes},
                with_labels=False,
                node_size=1,
                width=0.1,
                arrows=False,
                arrowsize=1)
        plt.gca().invert_yaxis()
        plt.show()

"""

visited = set()  # create a set (O(1) for retrievel according to stackoverflow) of already visited pixels

# TODO: This should come from the GUI
image = Image.open("muT5j.png")
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
    return tuple(sum(x) for x in zip(current_position, going_to.value))  # adds the two tuples element-wise


def is_a_wall(current_position: tuple, direction: Direction) -> bool:
    # get pixel coordinates
    new_position = go_to(current_position, direction)

    # check if out-range in the image
    # check if it's not a black pixel
    # check if we already visited it
    return not pixel_in_range(new_position) or not pixel_is_black(new_position) or already_visited(new_position)


def next_directions(coming_from: Direction, current_position: tuple) -> Direction:
    # get the index of the directions were are coming from
    i = direction_index[coming_from]

    # loop over all directions on the circular list of directions
    for j in range(1, len(directions)):
        new_direction = directions[(i + j) % len(directions)]

        # if not a wall, then return the new direction
        if not is_a_wall(current_position, new_direction):
            return new_direction

    return None


def going_straight(coming_from: Direction, going_to: Direction) -> bool:
    index = direction_index[coming_from]

    opposite_direction_index = int((index + len(directions) / 2) % len(directions))

    return directions[opposite_direction_index] == going_to


def opposite_direction(direction: Direction) -> Direction:
    # get index of direction
    index = direction_index[direction]

    # get the opposite index (i.e.: the index in the opposite side of the circle/cardinal compass)
    opposite_direction_index = int((index + len(directions) / 2) % len(directions))

    return directions[opposite_direction_index]


G = nx.DiGraph()


def follow_wall(previous_node: tuple, coming_from: Direction, current_position: tuple) -> set:
    nodes = [previous_node]

    going_to = next_directions(coming_from, current_position)

    # base case
    while going_to:
        if not going_straight(coming_from, going_to) and not previous_node == current_position:
            # create node
            new_node = current_position
            nodes.append(new_node)
            # create edges between new_node and previous_node
            G.add_edge(previous_node, new_node)
            # set previous_node = new_node
            previous_node = new_node

        # set current position as already visited
        visited.add(current_position)
        coming_from = opposite_direction(going_to)
        current_position = go_to(current_position, going_to)
        going_to = next_directions(coming_from, current_position)

    G.add_node(current_position)
    if not previous_node == current_position:
        # create edges between new_node and previous_node
        G.add_edge(previous_node, current_position)
        nodes.append(current_position)
        visited.add(current_position)

    return nodes


trees = []  # roots of trees
for y in range(height):
    for x in range(width):
        pixel = (x, y)
        if pixel_is_black(pixel) and pixel not in visited:
            trees.append(pixel)
            follow_wall(pixel, Direction.WEST, pixel)

p = {v: v for v in G.nodes}
nx.draw(G, pos=p, with_labels=False, node_size=1, width=0.1, arrows=False, arrowsize=1)
plt.show()

time.sleep(5)
ox, oy = mouse.get_position()
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