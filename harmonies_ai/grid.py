from enum import Enum
from typing import Any

GridPosition = int
Grid = list


grid_columns = (5, 4, 5, 4, 5)
grid_size = sum(grid_columns)


doubled_coords = tuple(
    (y * 2 + int(x % 2 == 1), x)
    for x, column_size in enumerate(grid_columns)
    for y in range(column_size)
)

adjacent_steps = ((-2, 0), (-1, 1), (1, 1), (2, 0), (1, -1), (-1, -1))

# Maps positions to all positions that are adjacent to it
grid_adjacent = tuple(
    tuple(
        adj_pos
        for adj_pos, adj_doubled in enumerate(doubled_coords)
        if (adj_doubled[0] - doubled[0], adj_doubled[1] - doubled[1]) in adjacent_steps
    )
    for doubled in doubled_coords
)

# Maps positions within two steps of origin to 60 degree clockwise rotation
grid_rotations: dict[tuple[int, int], tuple[int, int]] = {
    step: adjacent_steps[(i + 1) % len(adjacent_steps)]
    for i, step in enumerate(adjacent_steps)
}
for i, (key, value) in list(enumerate(grid_rotations.items())):
    ky, kx = key
    vy, vx = value
    grid_rotations[(ky * 2, kx * 2)] = (vy * 2, vx * 2)

    vry, vrx = grid_rotations[value]
    grid_rotations[(ky + vy, kx + vx)] = (vy + vry, vx + vrx)


def rotate(hp: tuple[int, int], steps: int):
    for _ in range(steps):
        hp = grid_rotations[hp]
    return hp


class Shape(Enum):
    positions: dict[tuple[int, int], int]

    PAIR = {(2, 0): 0}
    TRIANGLE = {(2, 0): 0, (1, 1): 0}
    DIAMOND = {(2, 0): 0, (1, 1): 0, (1, -1): 0}
    BOOMERANG = {(1, 1): 0, (1, -1): 0}
    LINE = {(2, 0): 0, (4, 0): 1}

    def __init__(self, positions: dict[tuple[Any, Any], int]):
        self.positions = positions


def _rotate_shape(shape: Shape, pos: GridPosition):
    for steps in range(6):
        rotated = {
            (
                rotate(hp, steps)[0] + doubled_coords[pos][0],
                rotate(hp, steps)[1] + doubled_coords[pos][1],
            ): v
            for hp, v in shape.positions.items()
        }
        if all(hp in doubled_coords for hp in rotated):
            yield rotated


# Maps shape then position to tuple of all rotated shapes that fit in grid
shape_rotations = {
    shape: tuple(tuple(_rotate_shape(shape, pos)) for pos in range(grid_size))
    for shape in Shape
}
