GridPosition = int
Grid = list

grid_columns = (5, 4, 5, 4, 5)
grid_size = sum(grid_columns)


doubled_coords = tuple(
    (y * 2 + int(x % 2 == 1), x)
    for x, column_size in enumerate(grid_columns)
    for y in range(column_size)
)

adjacent_steps = ((2, 0), (-2, 0), (1, 1), (1, -1), (-1, 1), (-1, -1))

grid_adjacent = tuple(
    tuple(
        adj_pos
        for adj_pos, adj_doubled in enumerate(doubled_coords)
        if (adj_doubled[0] - doubled[0], adj_doubled[1] - doubled[1]) in adjacent_steps
    )
    for doubled in doubled_coords
)
