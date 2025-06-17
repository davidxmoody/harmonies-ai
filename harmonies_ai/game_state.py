from typing import Counter, NamedTuple
from random import choice, choices
from harmonies_ai.cards import AnimalCard, cards
from harmonies_ai.tokens import Stack, Token
from rich.text import Text

GridPosition = int
Grid = list
grid_size = 23


def to_doubled_coords(position: GridPosition):
    if 0 <= position < 5:
        return (0, position * 2)
    elif 5 <= position < 9:
        return (1, (position - 5) * 2 + 1)
    elif 9 <= position < 14:
        return (2, (position - 9) * 2)
    elif 14 <= position < 18:
        return (3, (position - 14) * 2 + 1)
    elif 18 <= position < 23:
        return (4, (position - 18) * 2)
    else:
        raise Exception("Position out of bounds")


class PlaceTokenAction(NamedTuple):
    token: Token
    position: GridPosition


class TakeCardAction(NamedTuple):
    card: AnimalCard


class DiscardCardAction(NamedTuple):
    card: AnimalCard


class PlaceCubeAction(NamedTuple):
    card: AnimalCard
    position: GridPosition


Action = PlaceTokenAction | TakeCardAction | PlaceCubeAction


class GameState:
    supply_tokens: Counter[Token]
    supply_cards: set[AnimalCard]

    display_tokens: tuple[tuple[Token, ...], ...]
    display_cards: set[AnimalCard]

    cards: dict[AnimalCard, int]
    cubes: Grid[bool]
    board: Grid[Stack]

    def __init__(self):
        self.supply_tokens = Counter(
            {
                Token.GRY: 23,
                Token.RED: 15,
                Token.BRN: 21,
                Token.GRN: 19,
                Token.BLU: 23,
                Token.YLW: 19,
            }
        )

        self.supply_cards = set(cards)
        self.display_cards = set()

        self._refresh_display()

        self.cards = {}
        self.cubes = [False] * grid_size
        self.board = [Stack.EMPTY0] * grid_size

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
        self.display_tokens = tuple(
            tuple(sorted(self._draw_token() for _ in range(3))) for _ in range(3)
        )
        while len(self.display_cards) < 4:
            self.display_cards.add(self._draw_card())

    def _place_token(self, token: Token, position: GridPosition):
        stack = self.board[position]
        if token not in stack.placements:
            raise Exception(f"Cannot place {token} on {stack}")
        self.board[position] = stack.placements[token]

    def _take_card(self, card: AnimalCard):
        if len(self.cards) >= 4:
            raise Exception("Cannot take more than 4 cards")
        if card not in self.display_cards:
            raise Exception("Card not in display")
        self.cards[card] = card.num_cubes
        self.display_cards.remove(card)

    def _discard_card(self, card: AnimalCard):
        if card not in self.display_cards:
            raise Exception("Card not in display")
        self.display_cards.remove(card)

    def _place_cube(self, card: AnimalCard, position: GridPosition):
        if card not in self.cards:
            raise Exception("Card not in available cards")
        if self.cubes[position]:
            raise Exception("Cube already placed at that position")

        can_be_placed = True  # TODO
        if not can_be_placed:
            raise Exception("Requirements for animal card are not met")

        self.cubes[position] = True
        self.cards[card] -= 1
        if self.cards[card] == 0:
            del self.cards[card]

    def take_turn(self, actions: list[Action]):
        placed_tokens = tuple(
            sorted(a.token for a in actions if isinstance(a, PlaceTokenAction))
        )
        if placed_tokens not in self.display_tokens:
            raise Exception("Tokens not in the display")

        num_card_actions = sum(
            isinstance(a, TakeCardAction) or isinstance(a, DiscardCardAction)
            for a in actions
        )
        if num_card_actions > 1:
            raise Exception("Cannot take or discard more than one animal card per turn")

        for a in actions:
            if isinstance(a, PlaceTokenAction):
                self._place_token(a.token, a.position)
            elif isinstance(a, TakeCardAction):
                self._take_card(a.card)
            elif isinstance(a, DiscardCardAction):
                self._discard_card(a.card)
            elif isinstance(a, PlaceCubeAction):
                self._place_cube(a.card, a.position)

        self._refresh_display()

    def __rich__(self):
        hex_template = [
            " ####### ",
            "##ccccc##",
            "##bbbbb##",
            "##aaaaa##",
            " ####### ",
        ]

        hex_height, hex_width = len(hex_template), len(hex_template[0])

        background = Text(" ", style="on #997C54")

        chars: list[list[str | Text]] = [
            [background for _ in range(hex_width * 5 + 8)]
            for _ in range(hex_height * 5 + 6)
        ]

        for i, (stack, cube) in enumerate(zip(self.board, self.cubes)):
            hex_x, hex_yd = to_doubled_coords(i)
            start_x = 2 + hex_x * (hex_width + 1)
            start_y = 1 + hex_yd * (hex_height + 1) // 2

            empty = Text(" ", style="on #EDCD9C")

            layers = {
                " ": background,
                "#": empty,
                "a": (
                    Text(" ", style=f"on {stack.components[0].bg}")
                    if len(stack.components) > 0
                    else empty
                ),
                "b": (
                    Text(" ", style=f"on {stack.components[1].bg}")
                    if len(stack.components) > 1
                    else empty
                ),
                "c": (
                    Text(" ", style=f"on {stack.components[2].bg}")
                    if len(stack.components) > 2
                    else empty
                ),
            }

            for y in range(hex_height):
                for x in range(hex_width):
                    chars[start_y + y][start_x + x] = layers[hex_template[y][x]]

        return Text("\n").join(Text.assemble(*line) for line in chars)
