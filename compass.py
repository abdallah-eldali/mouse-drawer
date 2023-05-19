"""
Circular Array Data Structure (similar to a clock)

NOTE: This class doesn't contain all the methods that the data structure supports, like remove(), set(), etc.
"""
import typing
# Generics
from typing import TypeVar, Generic, Iterator

T = TypeVar('T')


class CircularArray(Generic[T]):
    def __init__(self) -> None:
        self.__circular_array = []

    def __len__(self) -> int:
        return len(self.__circular_array)

    def __getitem__(self, index: int) -> T:
        if index >= len(self):
            raise IndexError("list index out of range")
        return self.__circular_array[index if len(self) == 0 else index % len(self)]

    def append(self, value: T) -> None:
        self.__circular_array.append(value)

    # NOTE: this class method is required since we cannot access __orig_class__ inside the __init__
    #      meaning we cannot have a self.data_type attribute that can be accessed normally
    def get_data_type(self) -> type(T):
        return typing.get_args(self.__orig_class__)[0]

    def __str__(self) -> str:
        return str(self.__circular_array)


from enum import Enum
from itertools import cycle, islice


# NOTE: Maybe it was better (and probably more efficient) to create my own circular array
#      instead of having to rely on cycle iterators


class Direction(Enum):
    NORTH = (0, -1)
    NORTHEAST = (1, -1)
    EAST = (1, 0)
    SOUTHEAST = (1, 1)
    SOUTH = (0, 1)
    SOUTHWEST = (-1, 1)
    WEST = (-1, 0)
    NORTHWEST = (-1, -1)


# 'statically' intialize the class
cardinal_directions = []
direction_index = {}

for index, direction in enumerate(Direction):
    cardinal_directions.append(direction)
    direction_index[direction] = index


def get_cardinal_points_from(cardinal_direction: Direction) -> Iterator[Direction]:
    start_index = direction_index[cardinal_direction]
    end_index = start_index + len(Direction)

    # TODO: Check time complexity for this, it might be faster if I implement it a different way
    return islice(cycle(cardinal_directions), start_index, end_index)


def opposite_direction(a: Direction) -> Direction:
    i_a = direction_index[a]

    # doing a 180 on the index of direction a, and seeing if it matched with direction b's index
    i_b = int((i_a + len(cardinal_directions) / 2) % len(cardinal_directions))

    return cardinal_directions[i_b]


def are_opposite(a: Direction, b: Direction) -> bool:
    return opposite_direction(a) == b