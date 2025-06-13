from typing import Counter
from random import choice, choices
from harmonies_ai.cards import AnimalCard, cards
from harmonies_ai.tokens import Stack, Token


Grid = list
grid_size = 23


class GameState:
    supply_tokens: Counter[Token]
    supply_cards: set[AnimalCard]

    display_tokens: list[list[Token]]
    display_cards: set[AnimalCard]

    cards: dict[AnimalCard, int]
    cubes: Grid[bool]
    board: Grid[Stack]

    def __init__(self):
        self.supply_tokens = Counter(
            {
                Token.GRAY: 23,
                Token.RED: 15,
                Token.BROWN: 21,
                Token.GREEN: 19,
                Token.BLUE: 23,
                Token.YELLOW: 19,
            }
        )

        self.supply_cards = set(cards)
        self.display_cards = set()

        self._refresh_display()

        self.cards = {}
        self.cubes = [False] * grid_size
        self.board = [Stack.EMPTY] * grid_size

    def _draw_token(self):
        token = choices(
            population=list(self.supply_tokens.keys()),
            weights=list(self.supply_tokens.values()),
            k=1,
        )[0]
        self.supply_tokens[token] -= 1
        return token

    def _draw_card(self):
        card = choice(tuple(self.supply_cards))
        self.supply_cards.remove(card)
        return card

    def _refresh_display(self):
        self.display_tokens = [[self._draw_token() for _ in range(3)] for _ in range(3)]
        while len(self.display_cards) < 4:
            self.display_cards.add(self._draw_card())
