"""
Circular Array Data Structure (similar to a clock)

NOTE: This class doesn't contain all the methods that the data structure supports, like remove(), set(), etc.
"""
import typing
# Generics
from typing import TypeVar, Generic

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
from itertools import cycle, islice, dropwhile


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

cardinal_directions = cycle(cardinal_directions)


def get_cardinal_points_from(direction: Direction) -> Iterator[Direction]:
    start_index = direction_index[direction]
    end_index = start_index + len(Direction)

    return islice(cardinal_directions, start_index, end_index)


# Testing

for i in get_cardinal_points_from(Direction.WEST):
    print(i)
