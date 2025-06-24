from enum import Enum
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
    shape: str
    reqs: tuple[Stack, ...]
    rewards: tuple[int, ...]

    MEERKAT = ("pair", (14, 9, 5, 2), (M1, F))
    BAT = ("pair", (15, 10, 6, 3), (M1, T3))
    EAGLE = ("pair", (11, 5), (M3, F))
    SQUIRREL = ("pair", (15, 9, 4), (B, T3))
    BOAR = ("pair", (13, 8, 4), (T2, B))
    KOALA = ("pair", (15, 10, 6, 3), (T2, T1))
    DUCK = ("pair", (13, 8, 4, 2), (W, B))
    FROG = ("pair", (15, 10, 6, 4, 2), (W, T1))
    FISH = ("pair", (16, 10, 6, 3), (W, M3))
    BUTTERFLY = ("pair", (17, 12, 8, 5, 2), (F, T1))
    MONKEY = ("triangle", (11, 5), (M2, W))
    HEDGEHOG = ("triangle", (12, 5), (B, T2))
    BEAR = ("triangle", (11, 5), (T1, M2))
    PARROT = ("triangle", (14, 9, 4), (T2, W))
    WOLF = ("triangle", (16, 10, 4), (T3, F))
    STINGRAY = ("triangle", (16, 10, 4), (W, M1))
    FLAMINGO = ("triangle", (16, 10, 4), (W, F))
    BEE = ("diamond", (18, 8), (T2, F))
    RACOON = ("diamond", (12, 6), (F, W))
    PENGUIN = ("boomerang", (16, 10, 4), (M1, W))
    PEACOCK = ("boomerang", (17, 10, 5), (B, W))
    MOUSE = ("boomerang", (17, 10, 5), (B, F))
    KINGFISHER = ("boomerang", (18, 11, 5), (T3, W))
    WHITE_WOLF = ("boomerang", (17, 10, 5), (F, T2))
    CROW = ("boomerang", (9, 4), (F, B))
    FOX = ("line", (16, 9, 4), (M1, M1, F))
    LIZARD = ("line", (16, 10, 5), (B, F, F))
    RABBIT = ("line", (17, 10, 5), (T1, T1, B))
    OTTER = ("line", (16, 10, 5), (W, T1, T1))
    CROCODILE = ("line", (15, 9, 4), (W, W, T3))
    PANTHER = ("line", (11, 5), (F, T2, T2))
    LLAMA = ("line", (12, 5), (F, F, M2))

    def __init__(self, shape: str, rewards: tuple[int, ...], reqs: tuple[Stack, ...]):
        self.shape = shape
        self.rewards = rewards
        self.reqs = reqs

    @property
    def base(self):
        return self.reqs[0]

    @property
    def num_cubes(self):
        return len(self.rewards)

    # @classmethod
    # def pair(cls, base: Stack, req: Stack, rewards: tuple[int, ...]):
    #     return cls(base, ((1, 0, req),), rewards)

    # @classmethod
    # def triangle(cls, base: Stack, req: Stack, rewards: tuple[int, ...]):
    #     return cls(base, ((1, 0, req), (0, 1, req)), rewards)

    # @classmethod
    # def diamond(cls, base: Stack, req: Stack, rewards: tuple[int, ...]):
    #     return cls(base, ((1, 0, req), (0, 1, req), (-1, 1, req)), rewards)

    # @classmethod
    # def boomerang(cls, base: Stack, req: Stack, rewards: tuple[int, ...]):
    #     return cls(base, ((1, 0, req), (-1, 1, req)), rewards)

    # @classmethod
    # def line(cls, base: Stack, req1: Stack, req2: Stack, rewards: tuple[int, ...]):
    #     return cls(base, ((1, 0, req1), (2, 0, req2)), rewards)
