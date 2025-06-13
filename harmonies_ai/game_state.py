from typing import Counter, NamedTuple
from random import choice, choices
from harmonies_ai.cards import AnimalCard, cards
from harmonies_ai.tokens import Stack, Token, placements

GridPosition = int
Grid = list
grid_size = 23


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
        self.display_tokens = tuple(
            tuple(sorted(self._draw_token() for _ in range(3))) for _ in range(3)
        )
        while len(self.display_cards) < 4:
            self.display_cards.add(self._draw_card())

    def _place_token(self, token: Token, position: GridPosition):
        existing_stack = self.board[position]
        valid_placements = placements.get(existing_stack, None)

        if valid_placements is None or token not in valid_placements:
            raise Exception(f"Cannot place {token} on {existing_stack}")

        self.board[position] = valid_placements[token]

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
