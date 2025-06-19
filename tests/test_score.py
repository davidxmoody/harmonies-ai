import pytest
from harmonies_ai.game_state import GameState
from harmonies_ai.tokens import Stack


test_cases: list[tuple[list[tuple[Stack, int]], int]] = [
    # Empty
    ([], 0),
    # Trees
    ([(Stack.TRUNK1, 0)], 0),
    ([(Stack.TRUNK2, 0)], 0),
    ([(Stack.TREES1, 0)], 1),
    ([(Stack.TREES2, 0)], 3),
    ([(Stack.TREES3, 0)], 7),
    # Mountains
    ([(Stack.MOUNT1, 0)], 0),
    ([(Stack.MOUNT1, 0), (Stack.MOUNT1, 2)], 0),
    ([(Stack.MOUNT1, 0), (Stack.MOUNT1, 1)], 2),
    ([(Stack.MOUNT1, 0), (Stack.MOUNT2, 1)], 4),
    ([(Stack.MOUNT1, 0), (Stack.MOUNT3, 1)], 8),
    # Fields
    ([(Stack.FIELD1, 0)], 0),
    ([(Stack.FIELD1, 0), (Stack.FIELD1, 1)], 5),
    ([(Stack.FIELD1, 0), (Stack.FIELD1, 1), (Stack.FIELD1, 2), (Stack.FIELD1, 3)], 5),
    ([(Stack.FIELD1, 0), (Stack.FIELD1, 1), (Stack.FIELD1, 3), (Stack.FIELD1, 4)], 10),
    # Buildings
    ([(Stack.BUILD2, 0)], 0),
    ([(Stack.BUILD2, 1), (Stack.TRUNK1, 5), (Stack.BUILD1, 6), (Stack.BUILD1, 2)], 0),
    ([(Stack.BUILD2, 1), (Stack.TRUNK1, 5), (Stack.BUILD1, 6), (Stack.MOUNT1, 2)], 5),
    (
        [
            (Stack.BUILD2, 1),
            (Stack.BUILD2, 2),
            (Stack.TRUNK1, 5),
            (Stack.MOUNT1, 6),
            (Stack.TRUNK1, 7),
        ],
        10,
    ),
    # Water
    ([(Stack.WATER1, pos) for pos in [0]], 0),
    ([(Stack.WATER1, pos) for pos in [0, 1]], 2),
    ([(Stack.WATER1, pos) for pos in [0, 1, 2]], 5),
    ([(Stack.WATER1, pos) for pos in [0, 1, 2, 3]], 8),
    ([(Stack.WATER1, pos) for pos in [0, 1, 2, 3, 8]], 11),
    ([(Stack.WATER1, pos) for pos in [0, 1, 2, 3, 8, 12]], 15),
    ([(Stack.WATER1, pos) for pos in [0, 1, 2, 3, 8, 12, 17]], 19),
    ([(Stack.WATER1, pos) for pos in [0, 1, 2, 3, 8, 12, 17, 21]], 23),
    ([(Stack.WATER1, pos) for pos in [0, 1, 5]], 2),
    ([(Stack.WATER1, pos) for pos in [0, 1, 5, 6, 10]], 5),
    ([(Stack.WATER1, pos) for pos in [1, 2, 7, 11, 10, 5]], 8),
]


@pytest.mark.parametrize("stacks, score", test_cases)
def test_score(stacks: list[tuple[Stack, int]], score: int):
    gs = GameState()
    for stack, pos in stacks:
        for token in stack.components:
            gs._place_token(token, pos)
    assert gs.score.total == score
