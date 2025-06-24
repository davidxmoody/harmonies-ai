from enum import Enum
from harmonies_ai.grid import Shape
from harmonies_ai.tokens import Stack

M1 = Stack.MOUNT1
M2 = Stack.MOUNT2
M3 = Stack.MOUNT3
B = Stack.BUILD2
T1 = Stack.TREES1
T2 = Stack.TREES2
T3 = Stack.TREES3
W = Stack.WATER1
F = Stack.FIELD1


class AnimalCard(Enum):
    rewards: tuple[int, ...]
    base: Stack
    reqs: tuple[Stack, ...]
    shape: Shape

    MEERKAT = ((14, 9, 5, 2), M1, (F,), Shape.PAIR)
    BAT = ((15, 10, 6, 3), M1, (T3,), Shape.PAIR)
    EAGLE = ((11, 5), M3, (F,), Shape.PAIR)
    SQUIRREL = ((15, 9, 4), B, (T3,), Shape.PAIR)
    BOAR = ((13, 8, 4), T2, (B,), Shape.PAIR)
    KOALA = ((15, 10, 6, 3), T2, (T1,), Shape.PAIR)
    DUCK = ((13, 8, 4, 2), W, (B,), Shape.PAIR)
    FROG = ((15, 10, 6, 4, 2), W, (T1,), Shape.PAIR)
    FISH = ((16, 10, 6, 3), W, (M3,), Shape.PAIR)
    BUTTERFLY = ((17, 12, 8, 5, 2), F, (T1,), Shape.PAIR)
    MONKEY = ((11, 5), M2, (W,), Shape.TRIANGLE)
    HEDGEHOG = ((12, 5), B, (T2,), Shape.TRIANGLE)
    BEAR = ((11, 5), T1, (M2,), Shape.TRIANGLE)
    PARROT = ((14, 9, 4), T2, (W,), Shape.TRIANGLE)
    WOLF = ((16, 10, 4), T3, (F,), Shape.TRIANGLE)
    STINGRAY = ((16, 10, 4), W, (M1,), Shape.TRIANGLE)
    FLAMINGO = ((16, 10, 4), W, (F,), Shape.TRIANGLE)
    BEE = ((18, 8), T2, (F,), Shape.DIAMOND)
    RACOON = ((12, 6), F, (W,), Shape.DIAMOND)
    PENGUIN = ((16, 10, 4), M1, (W,), Shape.BOOMERANG)
    PEACOCK = ((17, 10, 5), B, (W,), Shape.BOOMERANG)
    MOUSE = ((17, 10, 5), B, (F,), Shape.BOOMERANG)
    KINGFISHER = ((18, 11, 5), T3, (W,), Shape.BOOMERANG)
    WHITE_WOLF = ((17, 10, 5), F, (T2,), Shape.BOOMERANG)
    CROW = ((9, 4), F, (B,), Shape.BOOMERANG)
    FOX = ((16, 9, 4), M1, (M1, F), Shape.LINE)
    LIZARD = ((16, 10, 5), B, (F, F), Shape.LINE)
    RABBIT = ((17, 10, 5), T1, (T1, B), Shape.LINE)
    OTTER = ((16, 10, 5), W, (T1, T1), Shape.LINE)
    CROCODILE = ((15, 9, 4), W, (W, T3), Shape.LINE)
    PANTHER = ((11, 5), F, (T2, T2), Shape.LINE)
    LLAMA = ((12, 5), F, (F, M2), Shape.LINE)

    def __init__(
        self,
        rewards: tuple[int, ...],
        base: Stack,
        reqs: tuple[Stack, ...],
        shape: Shape,
    ):
        self.rewards = rewards
        self.base = base
        self.reqs = reqs
        self.shape = shape

    @property
    def num_cubes(self):
        return len(self.rewards)
