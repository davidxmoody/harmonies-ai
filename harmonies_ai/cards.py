from dataclasses import dataclass
from harmonies_ai.tokens import Stack


@dataclass(frozen=True)
class AnimalCard:
    base: Stack
    reqs: tuple[tuple[int, int, Stack], ...]
    rewards: tuple[int, ...]

    @property
    def num_cubes(self):
        return len(self.rewards)

    @classmethod
    def pair(cls, base: Stack, req: Stack, rewards: tuple[int, ...]):
        return cls(base, ((1, 0, req),), rewards)

    @classmethod
    def triangle(cls, base: Stack, req: Stack, rewards: tuple[int, ...]):
        return cls(base, ((1, 0, req), (0, 1, req)), rewards)

    @classmethod
    def spread(cls, base: Stack, req: Stack, rewards: tuple[int, ...]):
        return cls(base, ((1, 0, req), (0, 1, req), (-1, 1, req)), rewards)

    @classmethod
    def boomerang(cls, base: Stack, req: Stack, rewards: tuple[int, ...]):
        return cls(base, ((1, 0, req), (-1, 1, req)), rewards)

    @classmethod
    def line(cls, base: Stack, req1: Stack, req2: Stack, rewards: tuple[int, ...]):
        return cls(base, ((1, 0, req1), (2, 0, req2)), rewards)


M1 = Stack.MOUNT1
M2 = Stack.MOUNT2
M3 = Stack.MOUNT3
B = Stack.BUILD2
T1 = Stack.TREES1
T2 = Stack.TREES2
T3 = Stack.TREES3
W = Stack.WATER1
F = Stack.FIELD1


cards = frozenset(
    {
        AnimalCard.pair(M1, F, (14, 9, 5, 2)),  # Meerkat
        AnimalCard.pair(M1, T3, (15, 10, 6, 3)),  # Bat
        AnimalCard.pair(M3, F, (11, 5)),  # Eagle
        AnimalCard.pair(B, T3, (15, 9, 4)),  # Squirrel
        AnimalCard.pair(T2, B, (13, 8, 4)),  # Boar
        AnimalCard.pair(T2, T1, (15, 10, 6, 3)),  # Koala
        AnimalCard.pair(W, B, (13, 8, 4, 2)),  # Duck
        AnimalCard.pair(W, T1, (15, 10, 6, 4, 2)),  # Frog
        AnimalCard.pair(W, M3, (16, 10, 6, 3)),  # Fish
        AnimalCard.pair(F, T1, (17, 12, 8, 5, 2)),  # Butterfly
        AnimalCard.triangle(M2, W, (11, 5)),  # Monkey
        AnimalCard.triangle(B, T2, (12, 5)),  # Hedgehog
        AnimalCard.triangle(T1, M2, (11, 5)),  # Bear
        AnimalCard.triangle(T2, W, (14, 9, 4)),  # Parrot
        AnimalCard.triangle(T3, F, (16, 10, 4)),  # Wolf
        AnimalCard.triangle(W, M1, (16, 10, 4)),  # Stingray
        AnimalCard.triangle(W, F, (16, 10, 4)),  # Flamingo
        AnimalCard.spread(T2, F, (18, 8)),  # Bee
        AnimalCard.spread(F, W, (12, 6)),  # Racoon
        AnimalCard.boomerang(M1, W, (16, 10, 4)),  # Penguin
        AnimalCard.boomerang(B, W, (17, 10, 5)),  # Peacock
        AnimalCard.boomerang(B, F, (17, 10, 5)),  # Mouse
        AnimalCard.boomerang(T3, W, (18, 11, 5)),  # Kingfisher
        AnimalCard.boomerang(F, T2, (17, 10, 5)),  # White wolf
        AnimalCard.boomerang(F, B, (9, 4)),  # Crow
        AnimalCard.line(M1, M1, F, (16, 9, 4)),  # Fox
        AnimalCard.line(B, F, F, (16, 10, 5)),  # Lizard
        AnimalCard.line(T1, T1, B, (17, 10, 5)),  # Rabbit
        AnimalCard.line(W, T1, T1, (16, 10, 5)),  # Otter
        AnimalCard.line(W, W, T3, (15, 9, 4)),  # Crocodile
        AnimalCard.line(F, T2, T2, (11, 5)),  # Panther
        AnimalCard.line(F, F, M2, (12, 5)),  # Llama
    }
)
