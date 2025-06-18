from typing import Counter, NamedTuple
from random import choice, choices
from harmonies_ai.cards import AnimalCard
from harmonies_ai.rich_canvas import Color, RichCanvas
from harmonies_ai.tokens import Stack, Token

GridPosition = int
Grid = list
grid_size = 23


def to_doubled_coords(position: GridPosition):
    if 0 <= position < 5:
        return (position * 2, 0)
    elif 5 <= position < 9:
        return ((position - 5) * 2 + 1, 1)
    elif 9 <= position < 14:
        return ((position - 9) * 2, 2)
    elif 14 <= position < 18:
        return ((position - 14) * 2 + 1, 3)
    elif 18 <= position < 23:
        return ((position - 18) * 2, 4)
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
    display_cards: list[AnimalCard]

    cards: dict[AnimalCard, int]
    cubes: Grid[bool]
    board: Grid[Stack]

    @classmethod
    def random(cls):
        instance = cls()
        for _ in range(40):
            instance.board[choice(range(grid_size))] = choice(list(Stack))
        for _ in range(15):
            pos = choice(range(grid_size))
            if instance.board[pos] != Stack.EMPTY0:
                instance.cubes[pos] = True
        return instance

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

        self.supply_cards = set(AnimalCard)
        self.display_cards = []

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
            self.display_cards.append(self._draw_card())

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
        board_bg = "#997C54"
        board_empty = "#EDCD9C"
        cube_bg = "#E67C20"

        canvas = RichCanvas()

        pattern_templates = {
            "pair": [
                "             ",
                "        D    ",
                "   ggg cCc   ",
                "   fff bBb   ",
                "   eee aaa   ",
                "             ",
                "             ",
            ],
            "triangle": [
                "             ",
                "   fff  D    ",
                "   eee cCc   ",
                "       bBb   ",
                "   fff aaa   ",
                "   eee       ",
                "             ",
            ],
            "spread": [
                "             ",
                "      C      ",
                "     bBb     ",
                "     aaa     ",
                " eee     eee ",
                "     eee     ",
                "             ",
            ],
            "boomerang": [
                "             ",
                "      D      ",
                "     cCc     ",
                "     bBb     ",
                " fff aaa fff ",
                " eee     eee ",
                "             ",
            ],
            "line": [
                "             ",
                "          D  ",
                " jjj ggg cCc ",
                " iii fff bBb ",
                " hhh eee aaa ",
                "             ",
                "             ",
            ],
        }

        for ci, card in enumerate(self.display_cards):
            labels = dict[str, Color]({c: board_empty for c in " abcdefghij"})
            labels.update(zip("abc", card.reqs[0].components))
            labels.update(zip("efg", card.reqs[1].components))
            if len(card.reqs) > 2:
                labels.update(zip("hij", card.reqs[2].components))
            labels["BCD"[len(card.reqs[0].components) - 1]] = cube_bg

            canvas.draw_template(
                (0, 3 + 18 * ci), pattern_templates[card.shape], labels
            )

        canvas.advance_origin(2)

        for gi, group in enumerate(self.display_tokens):
            for ti, token in enumerate(group):
                canvas.draw_rect((0, 3 + gi * 25 + ti * 6), (1, 5), token.bg)

        canvas.advance_origin(2)

        hex_template = [
            "  #########  ",
            " ####DDD#### ",
            "###ccCCCcc###",
            "###bbBBBbb###",
            " ##aaAAAaa## ",
            "  #########  ",
        ]

        hex_height, hex_width = len(hex_template), len(hex_template[0])

        canvas.draw_rect((0, 0), (hex_height * 5 + 6, hex_width * 5 + 8), board_bg)

        for i, (stack, cube) in enumerate(zip(self.board, self.cubes)):
            hex_yd, hex_x = to_doubled_coords(i)
            start_y = 1 + hex_yd * (hex_height + 1) // 2
            start_x = 2 + hex_x * (hex_width + 1)

            layers = {
                "#": board_empty,
                "a": board_empty,
                "b": board_empty,
                "c": board_empty,
                "d": board_empty,
            }

            for i, token in enumerate(stack.components):
                label = ["a", "b", "c", "d"][i]
                layers[label] = token.bg

            if cube:
                label = ["A", "B", "C", "D"][len(stack.components)]
                layers[label] = cube_bg

            canvas.draw_template((start_y, start_x), hex_template, layers)

        return canvas
