from typing import Counter, NamedTuple
from random import choice, choices, sample
from harmonies_ai.cards import AnimalCard
from harmonies_ai.grid import (
    Grid,
    GridPosition,
    Shape,
    grid_size,
    doubled_coords,
    grid_adjacent,
    shape_rotations,
)
from harmonies_ai.rich_canvas import Pixel, RichCanvas
from harmonies_ai.tokens import Stack, Token


class Score(NamedTuple):
    trees: int
    mountains: int
    fields: int
    buildings: int
    water: int
    cards: tuple[int, ...]

    @property
    def stacks_subtotal(self):
        return self.trees + self.mountains + self.fields + self.buildings + self.water

    @property
    def cards_subtotal(self):
        return sum(self.cards)

    @property
    def total(self):
        return self.stacks_subtotal + self.cards_subtotal


class PlaceTokenAction(NamedTuple):
    token: Token
    pos: GridPosition


class TakeCardAction(NamedTuple):
    card: AnimalCard


class DiscardCardAction(NamedTuple):
    card: AnimalCard


class PlaceCubeAction(NamedTuple):
    card: AnimalCard
    pos: GridPosition


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
    def random(
        cls,
        stack_options=[s for s in Stack if s != Stack.EMPTY0],
        num_stacks=20,
        num_cubes=10,
    ):
        instance = cls()
        for pos in sample(range(grid_size), k=num_stacks):
            instance.board[pos] = choice(stack_options)
        for pos in sample(
            [p for p, s in enumerate(instance.board) if s != Stack.EMPTY0],
            k=num_cubes,
        ):
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

    def _place_token(self, token: Token, pos: GridPosition):
        stack = self.board[pos]
        if token not in stack.placements:
            raise Exception(f"Cannot place {token} on {stack}")
        self.board[pos] = stack.placements[token]

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

    def could_place_cube(self, card: AnimalCard, pos: GridPosition):
        if self.board[pos] != card.base:
            return False

        return any(
            all(self.board[p] == card.reqs[v] for p, v in rotation.items())
            for rotation in shape_rotations[card.shape][pos]
        )

    def _place_cube(self, card: AnimalCard, pos: GridPosition):
        if card not in self.cards:
            raise Exception("Card not in available cards")
        if self.cards[card] == 0:
            raise Exception("No cubes left on that card")
        if self.cubes[pos]:
            raise Exception("Cube already placed at that position")

        if not self.could_place_cube(card, pos):
            raise Exception("Requirements for animal card are not met")

        self.cubes[pos] = True
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
                self._place_token(a.token, a.pos)
            elif isinstance(a, TakeCardAction):
                self._take_card(a.card)
            elif isinstance(a, DiscardCardAction):
                self._discard_card(a.card)
            elif isinstance(a, PlaceCubeAction):
                self._place_cube(a.card, a.pos)

        self._refresh_display()

    def get_adjacent_tokens(self, pos: GridPosition):
        return {
            self.board[adj_pos].components[-1]
            for adj_pos in grid_adjacent[pos]
            if self.board[adj_pos] != Stack.EMPTY0
        }

    def find_groups(self, stack: Stack):
        matching = {pos for pos, s in enumerate(self.board) if s == stack}
        groups: list[set[int]] = []

        while matching:
            first_item = matching.pop()
            current_group = {first_item}
            frontier = {pos for pos in grid_adjacent[first_item] if pos in matching}

            while frontier:
                next_item = frontier.pop()
                current_group.add(next_item)
                matching.remove(next_item)
                frontier.update(
                    pos for pos in grid_adjacent[next_item] if pos in matching
                )

            groups.append(current_group)

        return groups

    def find_longest_river(self):
        longest_river = 0

        for group in self.find_groups(Stack.WATER1):
            for start in group:
                length = 0
                explored = set[int]()
                frontier = {start}

                while frontier:
                    length += 1
                    explored.update(frontier)
                    frontier = {
                        apos
                        for pos in frontier
                        for apos in grid_adjacent[pos]
                        if apos in group and apos not in explored
                    }

                longest_river = max(longest_river, length)

        return longest_river

    @property
    def score(self):
        tree_scoring = {Stack.TREES1: 1, Stack.TREES2: 3, Stack.TREES3: 7}
        trees = sum(
            tree_scoring[stack] for stack in self.board if stack in tree_scoring
        )

        mountain_scoring = {Stack.MOUNT1: 1, Stack.MOUNT2: 3, Stack.MOUNT3: 7}
        mountains = sum(
            mountain_scoring[stack]
            for pos, stack in enumerate(self.board)
            if stack in mountain_scoring and Token.GRY in self.get_adjacent_tokens(pos)
        )

        fields = 5 * sum(len(group) >= 2 for group in self.find_groups(Stack.FIELD1))

        buildings = 5 * sum(
            len(self.get_adjacent_tokens(pos)) >= 3
            for pos, stack in enumerate(self.board)
            if stack == Stack.BUILD2
        )

        water_scoring = [0, 0, 2, 5, 8, 11, 15]
        longest_river = self.find_longest_river()
        water = (
            water_scoring[longest_river]
            if longest_river < len(water_scoring)
            else water_scoring[-1] + 4 * (longest_river - len(water_scoring) + 1)
        )

        return Score(
            trees=trees,
            mountains=mountains,
            fields=fields,
            buildings=buildings,
            water=water,
            cards=(),
        )

    def __rich__(self):
        board_bg = "#997C54"
        board_empty = "#EDCD9C"
        cube_bg = "#E67C20"

        canvas = RichCanvas()

        pattern_templates = {
            Shape.PAIR: [
                "             ",
                "        D    ",
                "   ggg cCc   ",
                "   fff bBb   ",
                "   eee aaa   ",
                "             ",
                "             ",
            ],
            Shape.TRIANGLE: [
                "             ",
                "   fff  D    ",
                "   eee cCc   ",
                "       bBb   ",
                "   fff aaa   ",
                "   eee       ",
                "             ",
            ],
            Shape.DIAMOND: [
                "             ",
                "      C      ",
                "     bBb     ",
                "     aaa     ",
                " eee     eee ",
                "     eee     ",
                "             ",
            ],
            Shape.BOOMERANG: [
                "             ",
                "      D      ",
                "     cCc     ",
                "     bBb     ",
                " fff aaa fff ",
                " eee     eee ",
                "             ",
            ],
            Shape.LINE: [
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
            labels = dict[str, Pixel]({c: board_empty for c in " abcdefghij"})
            labels.update(zip("abc", card.base.components))
            labels.update(zip("efg", card.reqs[0].components))
            if len(card.reqs) > 1:
                labels.update(zip("hij", card.reqs[1].components))
            labels["BCD"[len(card.base.components) - 1]] = cube_bg

            card_left = 3 + 18 * ci

            canvas.draw_template((0, card_left), pattern_templates[card.shape], labels)

            canvas.draw_text(
                (7, card_left), card.name.center(13), bg=board_empty, fg="black"
            )
            canvas.draw_text(
                (8, card_left),
                " ".join(str(r) for r in card.rewards).center(13),
                bg=board_empty,
                fg="black",
            )
            canvas.draw_rect((9, card_left), (1, 13), board_empty)

        canvas.advance_origin(2)

        for gi, group in enumerate(self.display_tokens):
            canvas.draw_rect((0, 2 + gi * 24), (3, 21), board_empty)
            for ti, token in enumerate(group):
                canvas.draw_rect((1, 4 + gi * 24 + ti * 6), (1, 5), token.bg)

        canvas.advance_origin(2)

        hex_template = [
            "  ..........  ",
            " .....DD..... ",
            "....ccCCcc....",
            "....bbBBbb....",
            " ...aaaaaa... ",
            "  ..........  ",
        ]

        hex_height, hex_width = len(hex_template), len(hex_template[0])

        canvas.draw_rect((0, 0), (hex_height * 5 + 6, hex_width * 5 + 8), board_bg)

        for i, (stack, cube) in enumerate(zip(self.board, self.cubes)):
            hex_yd, hex_x = doubled_coords[i]
            start_y = 1 + hex_yd * (hex_height + 1) // 2
            start_x = 2 + hex_x * (hex_width + 1)

            labels = dict[str, Pixel]({c: board_empty for c in ".abcd"})
            labels.update(zip("abc", stack.components))
            if cube:
                labels["BCD"[len(stack.components) - 1]] = cube_bg

            canvas.draw_template((start_y, start_x), hex_template, labels)
            canvas.draw_text(
                (start_y + 5, start_x + 6), str(i).rjust(2, "0"), board_empty, board_bg
            )

        return canvas
